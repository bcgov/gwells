
################
# General Jobs #
################

default: vue

vue: prep
	NPM_CMD=dev docker-compose up -d

api: prep
	NPM_CMD=build docker-compose up -d

django: prep
	NPM_CMD=watch docker-compose up -d


###################
# Individual jobs #
###################

prep:
	@	docker-compose pull
	@	docker-compose build

down:
	@	docker-compose down

db-clean:
	@	docker-compose down || true
	@	rm -rf ./.tmp/psql-dev
	@	echo
	@	echo "Compose is down and the database folder deleted"
	@	echo
