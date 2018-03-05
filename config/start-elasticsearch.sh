sudo chown -R elasticsearch: /data/elasticsearch
sudo systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service
sudo systemctl status elasticsearch.service
