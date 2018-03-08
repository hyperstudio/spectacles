.PHONY: dev clean js

default: dev

clean:
	find . -type f -name "*.pyc" -delete

server:
	./manage.py runserver 8080

dev:
	./node_modules/webpack/bin/webpack.js -w

js:
	./node_modules/webpack/bin/webpack.js

prod:
	PRODUCTION=1 uwsgi --ini ./config/spectacles.pw_uwsgi.ini
