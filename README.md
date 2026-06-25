# Project Documentation

This repository contains the configuration and source files for a modular web application powered by a Flask backend and an Nginx reverse proxy, fully containerized using Docker.

## Features
* Modular architecture enabling plug-and-play module execution.
* Secure routing and reverse proxy setup via Nginx.
* Access control implemented through HTTP Basic Authentication.
* SSL encryption using self-signed certificates.
* Containerized environment for consistent deployment.

## Architecture Overview
The system isolates the web server layer from the application logic. Nginx handles incoming traffic, authentication, and static file serving, while the underlying REST logic is processed by the Flask API. Docker Compose orchestrates these services and networks them seamlessly.

## Table of Contents
1. [Architecture & Scalability](docs/ARCHITECTURE.md)
2. [Installation Guide](docs/INSTALL.md)
3. [Configuration](docs/CONFIGURATION.md)
4. [Security](docs/SECURITY.md)
5. [Usage & API Endpoints](docs/API_USAGE.md)

## Custom Container Images & Attribution

This project utilizes custom-built Docker images to adapt external open-source tools to our specific network and security architecture.

### Remote Touchpad Service
The `remote-touchpad` service deployed via `compose-touchpad.yml` uses a custom-modified image rather than a standard release.
* **Original Source & Attribution:** The core application was originally developed by [Unrud](https://github.com/Unrud/remote-touchpad). We deeply thank the original developer for their fantastic contribution to the open-source community.
* **Modifications:** To seamlessly integrate with our internal Nginx reverse-proxy gateway and bypass redundant authentication layers, the original `auth` requirements were removed. The application was manually recompiled to directly listen to `/dev/uinput` devices on the host network.
* **Image Location:** This custom image is publicly hosted on GitHub Container Registry (GHCR). Docker Compose automatically pulls it from: 
  `ghcr.io/mehmetercindogan/remote-services-4lan/remote-touchpad-non-auth`

## License

The configuration files, architectural bindings, and custom integration scripts within this repository are released under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

*(Note: Externally integrated services like `remote-touchpad`, `stirling-pdf`, and `nginx` retain their original respective open-source licenses.)*

## Contact & Inquiries:
* **LinkedIn:** [Mehmet Erçin DOĞAN](https://www.linkedin.com/in/MehmetErcinDogan)
* **GitHub:** [@MehmetErcinDogan](https://github.com/MehmetErcinDogan)
