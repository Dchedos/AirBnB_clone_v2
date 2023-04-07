#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static

# Update servers repository and install nginx
sudo apt update
sudo apt -y install nginx

# create project directories
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

# create initial html
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# create a symlink to ..release/test/ dir
ln -sf /data/web_static/releases/test/ /data/web_static/current

# give ownership of /data/ to the current user and group
chown -R ubuntu:ubuntu /data/

# set up nginx server configuration
sed -i '/listen 80 default_server/a location /hbnb_static/ { alias /data/web_static/current/;}' /etc/nginx/sites-available/default
sudo service nginx restart
