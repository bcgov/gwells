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
	docker-compose up

test-vue:
	docker exec -ti gwells-frontend-1 /bin/bash -c "cd /app/frontend/; npm run test:unit -- --runInBand"

test-vue-update:
	docker exec -ti gwells-frontend-1 /bin/bash -c "cd /app/frontend/; npm run test:unit:update"

vue-coverage:
	docker exec -ti gwells-frontend-1 /bin/bash -c "cd /app/frontend/; npm run coverage:test"

test-django:
	docker exec -ti gwells-backend-1 /bin/bash -c "cd /app/backend/; python -m coverage run manage.py test --noinput"

django-coverage:
	docker exec -ti gwells-backend-1 /bin/bash -c "cd /app/backend/; coverage report"

django-coverage-html:
	docker exec -ti gwells-backend-1 /bin/bash -c "cd /app/backend/; coverage html"

admin-django:
	docker exec -ti gwells-backend-1 /bin/bash -c "cd /app/backend; python manage.py createsuperuser"

backend:
	docker-compose pull backend
	docker-compose build backend
	docker-compose up backend

psql:
	docker-compose exec db /bin/bash -c "psql -U gwells -d gwells"
