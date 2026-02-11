# GWELLS web applications

## Introduction

This folder houses web applications being developed for the GWELLS project.

## Qualified Well Driller Registry

The Registry frontend app provides a user interface for accessing the Registry API. This app is located at /gwells/registries/ (base dir of the registries urls)

## Development

The GWELLS frontend web applications are developed with the Vue.JS framework.

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

## Serving the web app

### Project setup

At the root folder, run:

```
docker compose up
```

And one of containers will establish the frontend at "localhost:8080"

Environment variables will be set at image build time, following defaults or values placed in the ".env" file.

## Unit tests

Unit tests use the jest testing framework and vue-test-utils. `npm run test` runs the tests and outputs coverage information to the `test/unit/coverage` folder.

```bash
# run unit tests
npm run test:unit

# auto-run tests with watcher
npm run test:unit -- --watch
```

## Lints and fixes files

```bash
npm run lint
```
