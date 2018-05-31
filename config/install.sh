set -e
### On AWS, better to use EBS for /data; uncomment this to set up two
### volumes to back /data/elasticsearch and /data/postgres
#./install-fstab.sh
#./mount-volumes.sh

### Elasticsearch
./install-elasticsearch.sh
### Postgres
./install-postgres.sh
##### Create the spectacles database
./config/createdb-spectacles
### Elasticsearch
./install-elasticsearch.sh
### Nodejs, Yarn
./install-yarn.sh
### Python
./install-python.sh
### Nginx, Letsencrypt
./install-nginx.sh
./install-letsencrypt.sh
### UWSGI
./install-uwsgi.sh
