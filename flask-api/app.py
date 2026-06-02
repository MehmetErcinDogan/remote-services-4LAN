from flask import Flask, jsonify, request
from utils import (
    logger, 
    Config, 
    WeylusManager, 
    DockerManager, 
    GracefulShutdownManager
)

# 1. Start Services
app = Flask(__name__)
weylus_mgr = WeylusManager()

# 2. Start Crash/Shutdown Handler
shutdown_manager = GracefulShutdownManager(weylus_mgr)

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        
        "pdf-processor": DockerManager.get_status(
            "pdf-processor", 
            check_url="http://pdf-processor:8080/"
        ),

        "remote-touchpad": DockerManager.get_status(
            "remote-touchpad", 
            check_url="http://remote-touchpad:8080/"
        ),

        "weylus": weylus_mgr.is_alive()
        
    }), 200

@app.route('/api/service/<action>', methods=['POST'])
def manage_service(action):
    data = request.get_json() or {}
    service = data.get('service')

    if not service or action not in ['start', 'stop']:
        return jsonify({"error": "Invalid action or missing service information."}), 400

    if service == "weylus":
        success, message = weylus_mgr.start() if action == "start" else weylus_mgr.stop()
        
    elif service in ["pdf-processor", "remote-touchpad"]:
        success, message = DockerManager.manage_service(service, action)
        
    else:
        return jsonify({"error": "Yetkisiz servis."}), 403

    status_code = 200 if success else 500
    response_key = "message" if success else "error"
    
    return jsonify({"success": success, response_key: message}), status_code

if __name__ == '__main__':
    logger.info("SYSTEM STARTING...")
    
    proxy_success, proxy_msg = DockerManager.manage_service("proxy-gateway", "start")
    if not proxy_success:
        logger.critical(f"Nginx Gateway could not started: {proxy_msg}")
        
    logger.info(f"Flask API is live on {Config.HOST}:{Config.PORT}.")
    
    app.run(host=Config.HOST, port=Config.PORT, debug=False)