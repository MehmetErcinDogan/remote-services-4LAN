import os
import subprocess
import socket
import signal
import sys
import logging.config
import urllib.request
import urllib.error
from typing import Tuple, Dict, Any
from dotenv import load_dotenv

# Import environment variables 
# Reads, if there are .env file otherwise uses from os's env variables
load_dotenv()

# ==========================================
# 1. CONFIGURATION VE LOGGİNG
# ==========================================
class Config:
    HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    PORT = int(os.getenv("FLASK_PORT", 8080))
    TARGET_USER = os.getenv("TARGET_USER", "username")
    
    WEYLUS_BIND_ADDR = os.getenv("WEYLUS_BIND_ADDR", "172.17.0.1")
    WEYLUS_DISPLAY = os.getenv("WEYLUS_DISPLAY", ":1")
    WEYLUS_XAUTH = os.getenv("WEYLUS_XAUTH", "/run/user/1000/gdm/Xauthority")

def setup_logger(name: str = "orchestrator") -> logging.Logger:
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s (%(funcName)s:%(lineno)d) - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            }
        },
        "root": {"handlers": ["console"], "level": "INFO"},
    }
    logging.config.dictConfig(logging_config)
    return logging.getLogger(name)

logger = setup_logger()

# ==========================================
# 2. SYSTEM AND NETWORK HELPERS
# ==========================================
class SystemUtils:    
    @staticmethod
    def execute_cmd(cmd: str) -> Tuple[bool, str]:
        logger.debug(f"Command is running: {cmd}")
        try:
            result = subprocess.run(
                cmd, shell=True, check=False, 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            is_success = result.returncode == 0
            output = result.stdout.strip() if is_success else result.stderr.strip()
            
            if not is_success:
                logger.warning(f"Command error (Error code: {result.returncode}): {output}")
            return is_success, output
        except Exception as e:
            logger.exception(f"Command running failed: {cmd}")
            return False, str(e)

    @staticmethod
    def is_http_ok(url: str, timeout: float = 3.0) -> bool:
        # This function returns true if http return code is 200, otherwise returns false.
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.getcode() == 200
        except urllib.error.HTTPError as e:
            logger.debug(f"[{url}] Health check is failed. HTTP Code: {e.code}")
            return False
        except Exception as e:
            logger.debug(f"[{url}] Can not reach to server: {str(e)}")
            return False

# ==========================================
# 3. WEYLUS MANAGER
# ==========================================
class WeylusManager:    
    def __init__(self):
        self._pid: str | None = None

    def _build_start_cmd(self) -> str:
        return (f"nsenter -t 1 -m -u -i -n su - {Config.TARGET_USER} -c "
                f"'DISPLAY={Config.WEYLUS_DISPLAY} XAUTHORITY={Config.WEYLUS_XAUTH} "
                f"weylus --bind-address {Config.WEYLUS_BIND_ADDR} --no-gui --try-nvenc --try-vaapi > /dev/null 2>&1 & echo $!'")

    def is_alive(self) -> bool:
        if not self._pid:
            return False
            
        success, _ = SystemUtils.execute_cmd(f"nsenter -t 1 -m -u -i -n kill -0 {self._pid}")
        if not success:
            self._pid = None
        return success

    def start(self) -> Tuple[bool, str]:
        if self.is_alive():
            return False, "Weylus already running."
            
        cmd = self._build_start_cmd()
        success, output = SystemUtils.execute_cmd(cmd)
        
        if success and output.isdigit():
            self._pid = output
            logger.info(f"Weylus started. Assigned PID: {self._pid}")
            return True, f"Started. PID: {self._pid}"
            
        logger.error(f"Weylus başlatılamadı: {output}")
        return False, f"Başlatma hatası: {output}"

    def stop(self) -> Tuple[bool, str]:
        if not self.is_alive():
            self._pid = None
            return False, "There are not any active weylus."
            
        success, output = SystemUtils.execute_cmd(f"nsenter -t 1 -m -u -i -n kill {self._pid}")
        if success:
            logger.info(f"Weylus (PID: {self._pid}) has been stopped.")
            self._pid = None
            return True, "Stopped."
            
        return False, f"Stopping Error: {output}"

# ==========================================
# 4. DOCKER CONTAINER MANAGER
# ==========================================
class DockerManager:   
    @staticmethod
    def get_status(container_name: str, check_url: str = None) -> bool:
        """Konteynerin çalışıp çalışmadığını, opsiyonel olarak HTTP 200 URL kontrolü ile denetler."""
        success, inspect_out = SystemUtils.execute_cmd(f"docker inspect -f '{{{{.State.Running}}}}' {container_name}")
        is_running = (success and inspect_out == "true")
        
        if check_url and is_running:
            return SystemUtils.is_http_ok(check_url)
            
        return is_running

    @staticmethod
    def manage_service(container_name: str, action: str) -> Tuple[bool, str]:
        if action not in ["start", "stop"]:
            return False, "Undefined action (just start/stop available)."
            
        success, output = SystemUtils.execute_cmd(f"docker {action} {container_name}")
        if success:
            logger.info(f"Docker service ({container_name}) '{action}'ed.")
        else:
            logger.error(f"Docker service ({container_name}) the action ({action}) failed: {output}")
        return success, output

# ==========================================
# 5. LIFE CYCLE (CLEANUP/SHUTDOWN) MANAGER
# ==========================================
class GracefulShutdownManager:    
    def __init__(self, weylus_mgr: WeylusManager):
        self.weylus_mgr = weylus_mgr
        signal.signal(signal.SIGTERM, self._shutdown_handler)
        signal.signal(signal.SIGINT, self._shutdown_handler)

    def _shutdown_handler(self, signum, frame):
        logger.info(f"[SİNYAL {signum}] System shutdown detected. Cleaning is starting...")
        
        if self.weylus_mgr.is_alive():
            logger.info("The weylus process is stopping...")
            self.weylus_mgr.stop()
            
        logger.info("Dependent services stopping...")
        DockerManager.manage_service("pdf-processor", "stop")
        DockerManager.manage_service("remote-touchpad", "stop")
        DockerManager.manage_service("proxy-gateway", "stop")
        
        logger.info("System sucessfully shutdowned.")
        sys.exit(0)
