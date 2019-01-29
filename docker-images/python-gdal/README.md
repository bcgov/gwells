oc -n csnr-devops-lab-tools new-build .  --name python-36-rhel7-gdal --context-dir=docker-images/python-gdal

oc -n csnr-devops-lab-tools logs -f bc/python-36-rhel7-gdal

oc -n csnr-devops-lab-tools tag python-36-rhel7-gdal:latest python-36-rhel7-gdal:v1
