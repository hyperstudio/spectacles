.PHONY: webpack-dev clean js

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
	PRODUCTION=1 nohup ./manage.py runserver 0.0.0.0:8091 >stdout.log 2>stderr.log&
