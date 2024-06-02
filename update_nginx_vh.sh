sudo cp ./*.nginx.host /etc/nginx/sites-available
sudo cp ./*.nginx.host /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl reload nginx
