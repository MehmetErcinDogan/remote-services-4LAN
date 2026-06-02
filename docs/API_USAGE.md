# Usage & API Endpoints
## Nginx Routing and Front-End
The Nginx server acts as the primary gateway. It serves the user interface directly from the nginx/mainPage/ directory:

- The core layout is provided by nginx/mainPage/index.html.

- Visual styling is handled by nginx/mainPage/style.css.

- Client-side interactions are managed by nginx/mainPage/script.js.

## Flask API
The backend application logic is maintained within the Flask service, primarily located in flask-api/app.py. Additional modular functions are stored in flask-api/utils.py.

The API relies on standard dependencies defined in flask-api/requirements.txt, specifically Flask==3.0.2 and python-dotenv==1.2.2. These packages are installed automatically during the build phase dictated by the flask-api/Dockerfile.

All external HTTP requests are received by the Nginx gateway via nginx/conf.d/gateway.conf. Nginx then evaluates the URL paths and proxies the traffic to the corresponding internal Flask API endpoints.
