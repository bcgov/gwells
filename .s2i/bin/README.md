### Adding the NPM Build for our VUE components

Insert the build actions just before `python manage.py collectstatic` so that the solution has the opportunity to download the needed node modules, build and integrate itself into the solution.
