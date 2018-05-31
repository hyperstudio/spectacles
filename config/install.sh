set -e
# On AWS, better to use EBS for /data; uncomment this to
# set up two volumes to back /data/elasticsearch and /data/postgres
#./install-fstab.sh
#./mount-volumes.sh

### Install postgres
./install-postgres.sh
### Create the spectacles database
./config/createdb-spectacles
### Install elasticsearch
./install-elasticsearch.sh
### Install nodejs and yarn
./install-yarn.sh
### Install python
./install-python.sh
### Install nginx and letsencrypt
./install-nginx.sh
./install-letsencrypt.sh
### Install uwsgi
./install-uwsgi.sh
