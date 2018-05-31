set -e
sudo adduser spectacles
sudo -u postgres createuser spectacles;
sudo -u postgres psql -c "CREATE DATABASE spectacles WITH OWNER spectacles'"
sudo -u postgres psql -c "ALTER USER spectacles WITH PASSWORD 'password';"
