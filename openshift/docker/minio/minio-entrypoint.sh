#!/bin/sh

mkdir -p /data/aquifer-docs
mkdir -p /data/driller-docs
mkdir -p /data/gwells
mkdir -p /data/well-docs

/usr/bin/docker-entrypoint.sh $@