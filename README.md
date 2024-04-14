# Central
Central hub to deliver notifications and monitor services

- [Features](#features)
- [Deployment](#deployment)
  - [Web apps](#web-apps)
  - [Central backend](#central-backend-and-APIs)
- [Config](#config)

## Features

- Forward notifications to single or multiple subscribers via telegram
- Monitor http services
    - Setup to launch http requests constantly
    - Allow: Send notification upon http response codes
    - Allow: Post message to task queue upon http response codes
- Monitor redis keys
    - Setup to constantly read value of a redis key
    - Allow: Send notification when value changes
    - Allow: Post message to task queue when value changes

## Deployment

### Web apps

Deploy through docker compose

```yaml
services:
  central-web:
    image: giobyte8/central-web:1.0.0
    container_name: central-web
    restart: unless-stopped
```

Container will expose web content at port `80` by default. Then, you can use a [reverse proxy](#reverse-proxy-setup) to route requests to it or to backend API

### Central backend and APIs

Setup **central** environment

```shell
wget -O central.env https://raw.githubusercontent.com/giobyte8/central/main/template.env
vim central.env

# Enter right values for each variable
```

Deploy through docker compose

> Make sure to enter your local volume for logs

```yaml
services:
	central:
    image: giobyte8/central:1.0.0
    container_name: central
    env_file:
      - central.env
    volumes:
      - "<local_logs>:/opt/central/logs"
```

Container will expose rest API at port `5000` by default. Then you can use a [reverse proxy](#reverse-proxy-setup) to route requests to it.

### Reverse proxy setup

You can use a reverse proxy to route requests to web container `/` and backend API `/api`. Use following nginx config as an example

```properties
server {
    listen 443 ssl;
    listen [::]:443 ssl;

    server_name central.giovanniaguirre.me;
    access_log /var/log/nginx/central.giovanniaguirre.me.access.log;
    error_log /var/log/nginx/central.giovanniaguirre.me.error.log;

    # Load SSL certificate files
    ssl_certificate         /etc/letsencrypt/live/central/fullchain.pem;
    ssl_certificate_key     /etc/letsencrypt/live/central/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/central/chain.pem;

    location / {
        proxy_pass              http://central-web;
        proxy_set_header        Host $host;
        proxy_set_header        X-Real-IP $remote_addr;
        proxy_buffering         off;
        proxy_request_buffering off;

	      # Websockets support
    	  proxy_http_version 1.1;
      	proxy_set_header Upgrade $http_upgrade;
      	proxy_set_header Connection "upgrade";
    }

    # Route /api/* requests to the 'central' container on port 80
    location /api/ {
        proxy_pass              http://central:5000;
        proxy_set_header        Host $host;
        proxy_set_header        X-Real-IP $remote_addr;
        proxy_buffering         off;
        proxy_request_buffering off;
   
        proxy_http_version 1.1;
    }
}

```

## Config

