# Spectacles (alpha)

Spectacles is open source software for creating active archives of digital
texts. It allows for user-created rich media annotations of those texts, as
well as fuzzy search over both texts and annotations. Additionally it uses
natural language processing techniques to allow users to browse annotations and
texts similar to those they've found relevant to their research needs. These
tools work together to support speculative analysis of the texts in the
archive.

You can view an active archive created with spectacles at our website,
[http://spectacles.pw](http://spectacles.pw).

**Spectacles is currently still under development** and should be considered to
be alpha-version software. Read and run the code at your own risk. Please feel
free to submit issues or contact the authors directly with any questions.

## Todo List
- [ ] Hosting
  - [ ] Document install scripts
- [ ] Data import script based on US-IRAN
  - [ ] Document this
- [ ] Website Styles
  - [X] Hide bookmarking
  - [X] Style user page
- [ ] Functionality
  - [X] Avoid recommending source ann/doc in results
  - [ ] User registration
  - [ ] Better home page
  - [X] Deeplinking to a fragment on a page
  - [X] Implement auth for all the different annotations
  - [X] Show document titles in annotation links
  - [ ] Logout links in dropdown under username in upper right
  - [ ] Single archive, name included in templates
  - [ ] Remove "recommended documents" view
  - [ ] Allow scoping document and annotation elasticsearch by user ID
- [ ] Code
  - [ ] Frontend cleanup
  - [ ] Backend cleanup
  - [ ] Merge multiple packages
  - [ ] Publish fork of annotator.js on github

## Documentation

### Dependencies
```bash
sudo apt-get install -y git
```

### Installation

```bash
# Clone the repository
cd ~
git clone git@github.com:hyperstudio/spectacles.git
cd ./spectacles/config
# Install elasticsearch
sudo echo "deb https://artifacts.elastic.co/packages/5.x/apt stable main" > /etc/apt/sources.list.d/elastic-5.x.list
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo apt-get update
sudo apt-get install elasticsearch
./install-elasticsearch.sh
sudo service elasticsearch start
# Install postgres
sudo add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-9.6
mkdir /etc/postgresql/9.6/main/conf.d
sudo mkdir /data/postgres
sudo chown -R postgres: /data/postgres
sudo -u postgres rsync -av /var/lib/postgresql /data/postgres
./install-postgres.sh
# Install nodejs and yarn
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt-get update
udo apt-get install -y nodejs yarn
# Install js dependencies
yarn install
# Install python
cd ..
sudo apt-get install python python-pip libssl-dev
pip install -U pip
pip install -r requirements.txt
# Install nginx
cd config
./install-nginx.sh
./configure-nginx.sh
# Install letsencrypt
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install python-certbot-nginx
sudo certbot --nginx -d spectacles.pw
# Install uwsgi
./install_uwsgi.sh
# Create the spectacles database
cd ..
sudo adduser spectacles
sudo -u postgres createuser spectacles;
sudo -u postgres psql -c "CREATE DATABASE spectacles WITH OWNER spectacles'"
sudo -u postgres psql -c "ALTER USER spectacles WITH PASSWORD 'password';"
# Set up the Postgres tables
./manage.py migrate
# Set up the Elasticsearch indexes
./manage.py search_index --create
# Create a new admin user
./manage.py createsuperuser
# Run the production web server
make prod
```
