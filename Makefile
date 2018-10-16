
################
# General Jobs #
################

default: vue

vue: prep
	NPM_CMD=dev docker-compose up; docker-compose down

api: prep
	NPM_CMD=build docker-compose up; docker-compose down

django: prep
	NPM_CMD=watch docker-compose up; docker-compose down


###################
# Individual jobs #
###################

prep:
	@	docker-compose pull
	@	docker-compose build

db-clean:
	@	docker-compose down || true
	@	rm -rf ./.tmp/psql-dev
	@	echo
	@	echo "Compose is down and the database folder deleted"
	@	echo
