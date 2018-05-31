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


## Documentation

### Installation
The installation scripts assume that you are installing on Ubuntu 16.04 or higher as the `ubuntu` user with `sudo` capabilities.

```bash
# Clone the repository
sudo apt-get install -y git
cd ~
git clone git@github.com:hyperstudio/spectacles.git

# Install Postgres, Elasticsearch, Node, Yarn, Python, Nginx, and UWSGI
cd ~/spectacles/config
./install.sh

# Install the Node and Python dependencies
cd ~/spectacles
yarn install
### Install python dependencies
pip install -U pip
pip install -r requirements.txt

# Set up Elasticsearch and Postgres for use by Spectacles
### Set up the Postgres tables
./manage.py migrate
### Set up the Elasticsearch indexes
./manage.py search_index --create
### Create a new admin user
./manage.py createsuperuser

# All done! Ready to run the production web server:
killall uwsgi && make prod
```

### Development
Start a local webserver with:
```
./manage.py runserver 8080
```
In another terminal set webpack running in a watch-compile loop:
```
make dev
```
Now any changes made to either a python or javascript file will be automatically picked up.
