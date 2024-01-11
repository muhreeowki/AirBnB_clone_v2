#!/usr/bin/env bash
# Script that sets up your web servers for the deployment.

# Install nginx if its not already installed
apt-get -y update
apt-get -y install nginx
ufw allow 'Nginx HTTP'

# Create necessary folders
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create html file
echo "Hello World!" >/data/web_static/releases/test/index.html

# Create symbolic link
ln -sF /data/web_static/releases/test/ /data/web_static/current

# Change ownership of the /data/ folder
chown -R ubuntu:ubuntu /data/

# Change the nginx config file
printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
      alias /data/web_static/current/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" >/etc/nginx/sites-available/default

# Start Nginx
service nginx restart
