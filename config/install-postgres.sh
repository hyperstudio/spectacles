sudo chown -R postgres: /data/postgres
sudo chmod -R 0700 /data/postgres
sudo cp /etc/postgresql/9.6/main/postgresql.conf /etc/postgresql/9.6/main/postgresql.conf.bkp
sudo cp ./postgresql.conf /etc/postgresql/9.6/main/postgresql.conf
sudo systemctl restart postgresql.service
sudo systemctl status postgresql.service
