
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
	docker-compose down

vue: prep
	NPM_CMD=dev docker-compose up || true

django: prep
	NPM_CMD=watch docker-compose up || true

test-node:
	docker exec -ti gwells_frontend_1 /bin/bash -c "cd /app/frontend/; npm run unit -- --runInBand"

test-django:
	docker exec -ti gwells_frontend_1 /bin/bash -c "cd /app/frontend/; npm run build"
	docker exec -ti gwells_backend_1 /bin/bash -c "cd /app/backend/; python manage.py test -c nose.cfg --noinput"

admin-django:
	docker exec -ti gwells_backend_1 /bin/bash -c "cd /app/backend; python manage.py createsuperuser"