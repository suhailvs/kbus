## KBUS.IN

## production deployment

```bash
pip install gunicorn
chown www-data:www-data mysite
chmod 777 mysite/db.sqlite3
```

```ini
$ vim /etc/systemd/system/kbus.socket

[Unit]
Description=Kbus socket

[Socket]
ListenStream=/run/kbus.sock

[Install]
WantedBy=sockets.target
```

```ini
$ vim /etc/systemd/system/kbus.service
[Unit]
Description=Kbus daemon for Django
Requires=kbus.socket
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/kbus
ExecStart=/var/www/kbus/env/bin/gunicorn \
    --workers 2 \
    --bind unix:/run/kbus.sock \
    mysite.wsgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable kbus
sudo systemctl start kbus
sudo systemctl status kbus
```

nginx settings:
```
$ vim /etc/nginx/sites-available/kbus
server {
    listen 80;
    server_name kbus.stackschools.com;
    location /static/ {
        alias /var/www/kbus/staticfiles/;
    }
    location / {
        proxy_pass http://unix:/run/kbus.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable it:
```
sudo ln -s /etc/nginx/sites-available/kbus /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```
**lets encrypt for HTTPS**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d kbus.stackschools.com
```