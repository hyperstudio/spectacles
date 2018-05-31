sudo mkdir -p /data/elasticsearch
sudo chown -R elastic: /data/elasticsearch 
sudo cp /etc/elasticsearch/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml.backup
sudo cp ./elasticsearch.yml /etc/elasticsearch/elasticsearch.yml
sudo cp /etc/elasticsearch/jvm.options /etc/elasticsearch/jvm.options.backup
sudo cp ./es_jvm.options /etc/elasticsearch/jvm.options
