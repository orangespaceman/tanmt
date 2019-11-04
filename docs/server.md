# TANMT - Server

[&laquo; Back](../README.md)

## Setup

* Sign up for a new Digital Ocean server
* Initial setup:
    - https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04
    - https://hostadvice.com/how-to/how-to-harden-your-ubuntu-18-04-server/
    - ufw: ssh, http, https
    - fail2ban
* Disable root:
    - https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-16-04
    - Edit sshd_config - `PermitRootLogin no`
* Update/upgrade
    - `sudo apt-get update`
    - `sudo apt-get upgrade -u`
* Auto security updates
    - https://libre-software.net/ubuntu-automatic-updates/
    - https://www.cyberciti.biz/faq/ubuntu-enable-setup-automatic-unattended-security-updates/
    - https://websiteforstudents.com/setup-automatic-security-updates-on-ubuntu-18-04-lts-beta-server/
* Django, Postgres, Nginx, Gunicorn:
    - https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04
* Node, npm
    - https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-18-04
* SSL
    - https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04
* HTTP/2
    - https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-with-http-2-support-on-ubuntu-18-04


## Nginx configs

```
# http redirect
server {
  listen 80;
  listen [::]:80;

  server_name [URL].co.uk www.[URL].co.uk;
  return 301 https://[URL].co.uk$request_uri;
}

# www redirect
server {
  listen 443 ssl http2;
  listen [::]:443 ssl http2;

  ssl_certificate /etc/letsencrypt/live/[URL].co.uk/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/[URL].co.uk/privkey.pem;

  ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

  # https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-with-http-2-support-on-ubuntu-18-04
  ssl_ciphers EECDH+CHACHA20:EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!MD5;

  server_name www.[URL].co.uk;
  return 301 https://[URL].co.uk$request_uri;
}

# server
server {
  listen 443 ssl http2;
  listen [::]:443 ssl http2;

  ssl_certificate /etc/letsencrypt/live/[URL].co.uk/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/[URL].co.uk/privkey.pem;

  ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

  # https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-with-http-2-support-on-ubuntu-18-04
  ssl_ciphers EECDH+CHACHA20:EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!MD5;

  server_name [URL].co.uk;

  location = /favicon.ico { access_log off; log_not_found off; }

  # Django static files
  location /static/ {
    root /home/tanmt/tanmt;
  }

  # Django admin uploads
  location /media/ {
    root /home/tanmt/tanmt;
  }

  # Django
  location / {
    include proxy_params;
    proxy_pass http://unix:/run/gunicorn.sock;
  }
}
```
