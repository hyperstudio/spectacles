set -e
sudo mkfs -t ext4 /dev/xvdb
sudo mkfs -t ext4 /dev/xvdc
sudo cp /etc/fstab /etc/fstab.backup
sudo cp ./fstab /etc/fstab
