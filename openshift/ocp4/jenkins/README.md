# Build Base image
oc -n 26e83e-tools process -f https://raw.githubusercontent.com/BCDevOps/openshift-components/333cd1a7dbe5efe0f692ccd4a65f11561e1cc240/cicd/jenkins-basic/openshift/build.yaml  SOURCE_REPOSITORY_REF=954d913cfa8a0d32bfb57bab62319658454c1d06 SUFFIX=-cv VERSION=v2-cv | jq 'del(.items[] | select(.kind == "BuildConfig") | .spec.triggers)' | oc -n 26e83e-tools apply -f -

oc -n 26e83e-tools start-build jenkins-basic-cv --wait=true


oc -n 26e83e-tools process -f jenkins-main-build.yaml SUFFIX=-cv SOURCE_IMAGE_STREAM_TAG=jenkins-basic:v2-cv VERSION=v2-latest | jq 'del(.items[] | select(.kind == "BuildConfig") | .spec.triggers)' | oc -n 26e83e-tools create -f -

(cd "$(git rev-parse --show-toplevel)" && oc -n 26e83e-tools start-build jenkins-main-cv --wait=true --from-repo=.)


oc -n 26e83e-tools process -f jenkins-deploy.yaml NAME=jenkins SUFFIX=-cv GH_USERNAME=blah GH_PASSWORD=blah | jq 'del(.items[] | select (.kind == "Secret"))' | oc -n 26e83e-tools create -f -
