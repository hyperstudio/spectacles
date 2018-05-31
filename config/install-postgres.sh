set -e
sudo add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-9.6
mkdir /etc/postgresql/9.6/main/conf.d
sudo mkdir /data/postgres
sudo chown -R postgres: /data/postgres
sudo -u postgres rsync -av /var/lib/postgresql /data/postgres
sudo chown -R postgres: /data/postgres
sudo chmod -R 0700 /data/postgres
sudo cp /etc/postgresql/9.6/main/postgresql.conf /etc/postgresql/9.6/main/postgresql.conf.bkp
sudo cp ./postgresql.conf /etc/postgresql/9.6/main/postgresql.conf
sudo systemctl restart postgresql.service
sudo systemctl status postgresql.service
