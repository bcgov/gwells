oc -n csnr-devops-lab-tools new-build .  --name python-36-rhel7-gdal --context-dir=docker-images/python-gdal

(or `oc -n csnr-devops-lab-tools new-build https://github.com/bcgov/gwells.git#feature/python-gdal --name python-36-rhel7-gdal --context-dir=docker-images/python-gdal` to reference a specific branch)

To reset:
oc -n moe-gwells-tools delete bc/tst-python-gdal istag/tst-python-gdal:latest is/tst-python-gdal

oc -n csnr-devops-lab-tools logs -f bc/python-36-rhel7-gdal

oc -n csnr-devops-lab-tools tag python-36-rhel7-gdal:latest python-36-rhel7-gdal:v1


# Docker Images 

Dockerfiles that are the source of GWELLS custom images.

## Python Images with GDAL, GEOS, and PROJ.4 compiled from source
    * [OpenShift, based upon RHEL7](./python-gdal/Dockerfile.rhel7)
    * [Local Development](./python-gdal/Dockerfile.centos)





```
docker build . -f Dockerfile.centos -t python-gis
docker build . -f Dockerfile.centos -t local/python-gis
docker run -it --rm  --user root --entrypoint /bin/bash local/python-gis
 
```


The OpenShift image can only be built on a machine with a valid subscription, so either on OpenShift itself or on a local development workstation with a valid RedHat Subscription:


```
oc -n csnr-devops-lab-tools new-build https://github.com/bcgov/gwells#feature/gis-backend-with-configmap --context-dir=docker-images/python-gdal --name gwells-python 


oc -n moe-gwells-tools tag gwells-python:latest gwells-python:3.6
oc -n moe-gwells-tools tag gwells-python:latest gwells-python:GDAL
oc -n moe-gwells-tools tag gwells-python:latest gwells-python:GEOS
oc -n moe-gwells-tools tag gwells-python:latest gwells-python:PROJ.4



```





```
cd docker-images/python-gdal/
docker build . -f Dockerfile.centos -t gwells-python:gdal

```




## License

Code released under the [Apache License, Version 2.0](https://github.com/bcgov/gwells/blob/master/LICENSE).
