
################
# General Jobs #
################

default: vue

vue: prep
	NPM_CMD=dev docker-compose up

django: prep
	NPM_CMD=watch docker-compose up


###################
# Individual jobs #
###################

prep:
	@	docker-compose pull
	@	docker-compose build

down:
	@	docker-compose down

test: test-node test-django

test-node:
	docker exec -ti gwells_webapp_1 /bin/bash -c "cd /app/frontend/; npm run unit -- --runInBand"

test-django:
	docker exec -ti gwells_webapp_1 /bin/bash -c "cd /app/frontend/; npm run build"
	docker exec -ti gwells_api_1 /bin/bash -c "cd /app/backend/; python manage.py test -c nose.cfg --noinput"
