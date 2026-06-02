# Installation Guide

## Prerequisites
Ensure the following dependencies are installed on your system before proceeding:
* Docker (Engine version 20.10+ recommended)
* Docker Compose (V2 syntax supported)

## Deployment Steps

### 1. Automated Installation
The repository includes an installation script to automate the initial setup of the core environment. Run the following commands:
```bash
chmod +x install.sh
./install.sh
```
### 2. Running Specific Modules
The architecture supports a modular approach. To launch specific optional services alongside the core infrastructure, pass the respective compose files using the -f configuration flag:

```bash
docker-compose -f docker-compose.yml -f compose-pdf.yml -f compose-touchpad.yml up -d
```

## Teardown and Uninstallation
To completely stop all active containers, remove networks, and clean up application resources, execute the uninstallation script:
```bash
chmod +x uninstall.sh
./uninstall.sh
```

