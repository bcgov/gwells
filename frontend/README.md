# GWELLS web application

## Introduction

This folder houses web applications being developed for the GWELLS project.

## Development

Web applications are developed with the Vue.JS framework and bundled by webpack. Each application gets its own bundle of javascript and css files like ```vendor.js``` and ```[app-name].js```. ```vendor.js``` contains modules and code that is common to every app (dependencies like Vue.JS, axios, etc.), while ```[app-name].js``` contains app-specific code. This is to allow caching of the larger vendor.js file across GWELLS web applications, while keeping application-specific javascript files small.

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

## Qualified Well Driller Registry

The Registry frontend app provides a user interface for accessing the Registry API. This app is loaded at /gwells/registries/ (base dir of the registries urls)

## Serving web apps with Django

To serve the webapps with Django, have ```views.py``` and ```urls.py``` load a template file with the django-webpack-loader tags. For more information, see [https://github.com/ezhome/django-webpack-loader](django-webpack-loader) and the existing template in the ```registries/templates/registries/``` folder.

Run the following commands to build the web app (bundle automatically inserted into Django template):

``` bash
# install dependencies
npm install

# build for production (puts files into Django folders ready to be loaded in templates)
npm run build

```

## Serving web app with hot reload for development

The app can be served with hot reload as follows:

```bash
# serve with hot reload at localhost:8080
npm run dev
```

You may need to edit ```index.html``` and/or ```build/webpack.base.conf.js``` and ```build/webpack.dev.conf.js``` to load your app if you are creating a new one (currently the registries app is loaded).

Please note that using the development server at port 8080 and making API requests to port 8000 will require configuring CORS request headers. See django package django-cors-headers. This is not necessary for serving the javascript apps with Django so this package is not included in the repository.

```
# build for production and view the bundle analyzer report
npm run build --report
```

## Unit tests

```
# run unit tests
npm run unit

# run all tests
npm test
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).
