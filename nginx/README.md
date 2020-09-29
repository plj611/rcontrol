## How to setup nginx with certbot in docker environment (under development)

1. Before docker-compose up

   1. Put app.conf info nginx/ with the following content

      ```
      server {
          listen 80;
          server_name <example.org>;
      
          location / {
              return 301 https://$host$request_uri;
          }
      
          location /.well-known/acme-challenge/ {
              root /var/www/certbot;
          }
      }`
      ```

2. docker-compose up

   1. Logon certbot container by docker-compose -f webapp.yaml exec certbot /bin/sh

   2. Issue command 

      ```
      certbot certonly --agree-tos --register-unsafely-without-email --webroot -w /var/www/certbot -d <example.org>
      ```

   3. Logon nginx container by docker-compose -f webapp.yaml exec nginx /bin/bash

   4. Issue command

      ```
      openssl dhparam -out /etc/nginx/dhparam.pem 2048
      ```

3. Edit app.conf in nginx/ and put the following block

   ```
   server {
       listen 443 ssl;
       server_name <example.org>;
   
       location / {
           proxy_pass http://rcontrol:5000
       }
   }
   
   ```

   