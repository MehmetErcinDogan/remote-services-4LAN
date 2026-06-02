# Security

The system implements security measures at the proxy layer, primarily managed by Nginx.

## Basic Authentication (.htpasswd)
Access to the application interfaces is restricted using HTTP Basic Authentication. The user credentials are encrypted and stored in the nginx/.htpasswd file.

The current configuration includes a pre-defined user named ercin.

### Generating a New Credentials File
To create a new credentials file or to add a different user, use the Apache htpasswd utility:

htpasswd -c nginx/.htpasswd your_username

The command prompt will ask you to define and confirm a password. Omit the -c flag if you are appending a new user to an existing file rather than overwriting it.

## SSL Certificates
Traffic to and from the server is encrypted using self-signed certificates. These files are stored in the nginx/ssl/ directory:
* Certificate: nginx/ssl/nginx-selfsigned.crt
* Private Key: nginx/ssl/nginx-selfsigned.key

For public production deployments, replace these self-signed files with verified certificates issued by a trusted Certificate Authority (CA).
### Generating a New Self-Signed Certificate
If the certificates are missing or expired, you can generate a new self-signed pair using OpenSSL by executing the following command from the project root directory:
```bash
mkdir -p nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx/ssl/nginx-selfsigned.key -out nginx/ssl/nginx-selfsigned.crt
```
