#!/bin/sh

mkdir /data/aquifer-docs
mkdir /data/driller-docs
mkdir /data/gwells
mkdir /data/well-docs

/usr/bin/docker-entrypoint.sh $@