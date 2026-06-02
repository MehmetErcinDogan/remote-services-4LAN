# Configuration

The application utilizes environment variables to manage its configuration securely.

## Environment Variables
The necessary environment variables must be defined inside the `flask-api/.env` file. These variables control how the Flask application connects to internal services and manages operational states.

## .env.example Setup
You need to create a file named `.env` inside the `flask-api/` directory. Below is a template structure you can use as your starting point:

```env
# flask-api/.env
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your_secure_secret_key_here
```

Note: Ensure that the actual `.env` file is included in your `.gitignore` and never committed to version control.

## Detailed Example Environment File
Below is an extended example block showing potential environment variables for the core application and its modular extensions:

```env

# Flask Configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=8080

# Sistem Configuration
TARGET_USER=<username>

# Weylus Configuration
WEYLUS_BIND_ADDR=172.17.0.1
WEYLUS_DISPLAY=:<display| just run "echo $DISPLAY">
WEYLUS_XAUTH=<path_to_xauth|just run "echo $XAUTHORITY">
