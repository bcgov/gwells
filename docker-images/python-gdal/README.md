oc -n csnr-devops-lab-tools new-build .  --name python-36-rhel7-gdal --context-dir=docker-images/python-gdal

(or `oc -n csnr-devops-lab-tools new-build https://github.com/bcgov/gwells.git#feature/python-gdal --name python-36-rhel7-gdal --context-dir=docker-images/python-gdal` to reference a specific branch)

To reset:
oc -n moe-gwells-tools delete bc/tst-python-gdal istag/tst-python-gdal:latest is/tst-python-gdal

oc -n csnr-devops-lab-tools logs -f bc/python-36-rhel7-gdal

oc -n csnr-devops-lab-tools tag python-36-rhel7-gdal:latest python-36-rhel7-gdal:v1
