set -e
# Fstab
sudo mkfs -t ext4 /dev/xvdb
sudo mkfs -t ext4 /dev/xvdc
./install-fstab.sh
./mount-volumes.sh
# Elasticsearch
./install-elasticsearch.sh
# Postgres
./install-postgres.sh
