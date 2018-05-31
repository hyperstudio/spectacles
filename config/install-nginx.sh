set -e
SITE_NAME="spectacles.pw"
sudo apt-get install nginx
sudo update-rc.d nginx defaults
sudo cp "./$SITE_NAME" "/etc/nginx/sites-available/$SITE_NAME"
sudo ln -f -s "/etc/nginx/sites-available/$SITE_NAME" "/etc/nginx/sites-enabled/$SITE_NAME"
