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
