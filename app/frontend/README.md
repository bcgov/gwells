# GWELLS web applications

## Introduction

This folder houses web applications being developed for the GWELLS project.

## Qualified Well Driller Registry

The Registry frontend app provides a user interface for accessing the Registry API. This app is located at /gwells/registries/ (base dir of the registries urls)

## Development

The GWELLS frontend web applications are developed with the Vue.JS framework and are organized/bundled by webpack.

Upon building, each application gets a bundle of javascript and css files. ```vendor.js``` contains dependencies that are common to each app (like Vue.JS and axios), while ```[app-name].js``` contains app-specific code. This is to allow caching of the larger vendor.js file across all apps, while keeping application-specific javascript files small.

### Adding new applications
To add a new application, make a new folder in the ```src``` directory. Then go into ```build/webpack.base.conf.js``` and find the ```entry``` object of ```module.exports```:

``` javascript
...
module.exports = {
  context: path.resolve(__dirname, '../'),
  entry: {
    registry: './src/registry/main.js'
  },
...
```

Add another line to the ```entry``` object with a string containing the entry point ```main.js``` to your new app. For example:
```javascript
...
module.exports = {
  context: path.resolve(__dirname, '../'),
  entry: {
    registry: './src/registry/main.js',
    aquifers: './src/aquifers/main.js'
  },
...
```
Note: don't use vue init to create new apps. This frontend folder was already created with the vue-cli webpack template.

## Serving web apps with Django

To serve the webapps with Django, have ```urls.py``` load a template file (you can use the TemplateView class) with the django-webpack-loader tags. For more information, see [https://github.com/ezhome/django-webpack-loader](django-webpack-loader) and the existing template in the ```registries/templates/registries/``` folder.

Run the following commands to build the web app (bundle automatically inserted into Django template):

``` bash
# install dependencies
npm install

# build for production (puts files into Django folders ready to be loaded in templates)
npm run build

```

## Serving the web apps with Django and hot reloading

Start webpack in listening mode (Django will listen to changes)

```bash
# Listen for file changes
npm run watch
```

Start python in debug mode.
```
# Django MUST be run in debug mode to point to the correct static files.
DJANGO_DEBUG=True python manage.py runserver
```

## Serving web app with hot reload for development

The app can be served with hot reload as follows:

```bash
# serve with hot reload at localhost:8080
APPLICATION_ROOT="/" AXIOS_BASE_URL="http://localhost:8000/gwells/api/v1/" npm run dev
```

You may need to edit ```index.html``` and/or ```build/webpack.base.conf.js``` and ```build/webpack.dev.conf.js``` to load your app if you are creating a new one (currently the registries app is loaded).

Please note that using the development server at port 8080 and making API requests to port 8000 will require configuring CORS request headers. See django package django-cors-headers. This is not necessary for serving the javascript apps with Django so this package is not included in the repository.

```
# build for production and view the bundle analyzer report
npm run build --report
```

## Unit tests

Unit tests use the jest testing framework and vue-test-utils. ```npm run test``` runs the tests and outputs coverage information to the ```test/unit/coverage``` folder.

```
# run unit tests
npm run unit

# run all tests
npm test

# auto-run tests with watcher
npm run unit -- --watch
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).
