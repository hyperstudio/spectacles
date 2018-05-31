set -e
sudo echo "deb https://artifacts.elastic.co/packages/5.x/apt stable main" > /etc/apt/sources.list.d/elastic-5.x.list
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo apt-get update
sudo apt-get install elasticsearch
sudo mkdir -p /data/elasticsearch
sudo chown -R elastic: /data/elasticsearch 
sudo cp /etc/elasticsearch/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml.backup
sudo cp ./elasticsearch.yml /etc/elasticsearch/elasticsearch.yml
sudo cp /etc/elasticsearch/jvm.options /etc/elasticsearch/jvm.options.backup
sudo cp ./es_jvm.options /etc/elasticsearch/jvm.options
sudo service elasticsearch restart
