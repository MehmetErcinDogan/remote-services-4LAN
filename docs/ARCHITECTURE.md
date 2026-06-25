# Architecture and Modular Scalability

The system is designed module-based architecture. Rather than relying on a single monolithic configuration, independent features are separated into distinct Docker Compose files.

## Modular Design
This plug-and-play approach allows you to deploy only the services you actively need, optimizing resource usage. The available modules include:
* **Core API:** Managed by the main `docker-compose.yml` file.
* **Nginx Router:** Deployed via `compose-nginx.yml`.
* **PDF Processor:** Deployed via `compose-pdf.yml`.
* **Touchpad Controller:** Deployed via `compose-touchpad.yml`.*(Utilizes a custom, non-auth modified image hosted on GHCR, derived from [Unrud/remote-touchpad](https://github.com/Unrud/remote-touchpad)).*
* **General Controller:** Deployed via `compose-controller.yml`.

## Adding New Features
To introduce a new feature to the system, you do not need to rewrite the core application. You simply create a new `compose-<feature>.yml` file and launch it alongside the existing containers. The Nginx gateway, configured within `nginx/conf.d/gateway.conf`, manages the traffic routing to the newly integrated services.
