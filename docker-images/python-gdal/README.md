oc -n csnr-devops-lab-tools new-build .  --name python-36-rhel7-gdal --context-dir=docker-images/python-gdal

(or `oc -n csnr-devops-lab-tools new-build https://github.com/bcgov/gwells.git#feature/python-gdal --name python-36-rhel7-gdal --context-dir=docker-images/python-gdal` to reference a specific branch)

To reset:
oc -n moe-gwells-tools delete bc/tst-python-gdal istag/tst-python-gdal:latest is/tst-python-gdal

oc -n csnr-devops-lab-tools logs -f bc/python-36-rhel7-gdal

oc -n csnr-devops-lab-tools tag python-36-rhel7-gdal:latest python-36-rhel7-gdal:v1


# Docker Images 

Dockerfiles that are the source of GWELLS Builds.

## Python Images with GDAL, GEOS, and PROJ.4 compiled from source
    * [OpenShift, based upon RHEL7](./python-gdal/Dockerfile.rhel7)
    * [Local Development](./python-gdal/Dockerfile.alpine)


```
docker build . -f Dockerfile.alpine -t python-gis
docker build . -f Dockerfile.alpine -t local/python-gis
docker run -it --rm  --user root --entrypoint /bin/bash local/python-gis


 
```


The OpenShift image can only be built on a machine with a valid subscription, so either on OpenShift itself or on a local development workstation logged in via `oc` and then via:
```
docker login -u garywong-bc -p `oc whoami -t` docker-registry.pathfinder.gov.bc.ca
docker login -u garywong-bc -p `oc whoami -t` registry.access.redhat.com
```

```
docker build . -f Dockerfile.rhel7 -t python-gdal-rhel7

s2i build https://github.com/sclorg/s2i-python-container.git --context-dir=3.6/test/setup-test-app/ centos/python-36-centos7 python-sample-app

```



```
docker build . -f Dockerfile.centos -t python-gdal24-centos


```




## License

Code released under the [Apache License, Version 2.0](https://github.com/bcgov/gwells/blob/master/LICENSE).
