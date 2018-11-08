
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

fixtures:
	@	docker exec -ti gwells_api_1 bash -c " \
			cd /app/backend; \
			python manage.py migrate; \
			python manage.py loaddata gwells-codetables.json; \
			python manage.py loaddata wellsearch-codetables.json registries-codetables.json; \
			python manage.py loaddata wellsearch.json registries.json; \
			python manage.py loaddata aquifers.json; \
			python manage.py createinitialrevisions \
		" || \
			echo "Failed.  Please make sure the API container has had time to start."

down:
	@	docker-compose down

db-clean:
	@	docker-compose down || true
	@	rm -rf ./.tmp/psql-dev
	@	echo
	@	echo "Compose is down and the database folder deleted"
	@	echo
