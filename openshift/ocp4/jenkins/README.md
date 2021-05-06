
# Build Base image
```
export OC_P_SUFFIX='-1790' OC_P_VERSION='v2-1790'
oc -n 26e83e-tools process -f https://raw.githubusercontent.com/BCDevOps/openshift-components/333cd1a7dbe5efe0f692ccd4a65f11561e1cc240/cicd/jenkins-basic/openshift/build.yaml  SOURCE_REPOSITORY_REF=954d913cfa8a0d32bfb57bab62319658454c1d06 SUFFIX=${OC_P_SUFFIX} VERSION=${OC_P_VERSION} | jq '(.items[] | .metadata.labels) += {"app.kubernetes.io/part-of": "jenkins"}' |  jq --arg instance "jenkins${OC_P_SUFFIX}" '(.items[] | select(.kind != "ImageStream") | .metadata.labels) += {"app.kubernetes.io/instance": $instance}' | jq 'del(.items[] | select(.kind == "BuildConfig") | .spec.triggers)' | oc -n 26e83e-tools apply -f -

oc -n 26e83e-tools start-build "jenkins-basic${OC_P_SUFFIX}" --wait=true
```

# Build Final image

oc -n 26e83e-tools process -f jenkins-main-build.yaml SUFFIX=${OC_P_SUFFIX} SOURCE_IMAGE_STREAM_TAG=jenkins-basic:${OC_P_VERSION} VERSION=${OC_P_VERSION} | jq '(.items[] | .metadata.labels) += {"app.kubernetes.io/part-of": "jenkins"}' |  jq --arg instance "jenkins${OC_P_SUFFIX}" '(.items[] | select(.kind != "ImageStream") | .metadata.labels) += {"app.kubernetes.io/instance": $instance}' | jq 'del(.items[] | select(.kind == "BuildConfig") | .spec.triggers)' | oc -n 26e83e-tools apply -f -

(cd "$(git rev-parse --show-toplevel)" && oc -n 26e83e-tools start-build jenkins-main${OC_P_SUFFIX} --wait=true --from-repo=.)

# Deploy
oc -n 26e83e-tools process -f jenkins-deploy.yaml NAME=jenkins SUFFIX= "JENKINS_IMAGE_STREAM_NAME=jenkins-main:${OC_P_VERSION}" GH_USERNAME=blah GH_PASSWORD=blah | jq 'del(.items[] | select (.kind == "Secret" or .kind == "PersistentVolumeClaim"))' | jq '(.items[] | .metadata.labels) += {"app.kubernetes.io/part-of": "jenkins"}' |  jq --arg instance "jenkins-prod" '(.items[] | select(.kind != "ImageStream") | .metadata.labels) += {"app.kubernetes.io/instance": $instance}'  | oc -n 26e83e-tools apply -f - --dry-run=client
