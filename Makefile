.DELETE_ON_ERROR:


################
# General Jobs #
################

default: vue down

test: test-node test-django


###################
# Individual jobs #
###################

prep:
	docker-compose pull
	docker-compose build

down:
	docker-compose down --volumes

vue: prep
	NPM_CMD=dev docker-compose up

django: prep
	NPM_CMD=watch docker-compose up

test-node:
	docker exec -ti gwells_frontend_1 /bin/bash -c "cd /app/frontend/; npm run unit -- --runInBand"

test-django:
	docker exec -ti gwells_backend_1 /bin/bash -c "cd /app/backend/; python manage.py test -c nose.cfg --noinput"

admin-django:
	docker exec -ti gwells_backend_1 /bin/bash -c "cd /app/backend; python manage.py createsuperuser"

backend:
	docker-compose pull backend
	docker-compose build backend
	docker-compose up backend
