# To Rebuild Jenkins:

1. Navigate to openshift/ocp4/jenkins

2. Replace the PR_NUMBER environment variable value below by your PR number and run
```
export PR_NUMBER='your-pr-number'
```

3. Replace the GH_BRANCH environment variable value below by your GitHub branch name and run
```
export GH_BRANCH='your-branch-name' 
```

4. Set other required environment variables
```
export OC_P_SUFFIX='-'${PR_NUMBER} OC_P_VERSION='v2-'${PR_NUMBER} 
```

5. Create build config for Jenkins Basic
```
oc -n 26e83e-tools process -f ./basic/jenkins-basic-build.yaml SOURCE_REPOSITORY_REF=${GH_BRANCH}  SUFFIX=${OC_P_SUFFIX} VERSION=${OC_P_VERSION} |
      jq '(.items[] | .metadata.labels) += {"app.kubernetes.io/part-of": "jenkins"}' | 
      jq --arg instance "jenkins${OC_P_SUFFIX}" '(.items[] | select(.kind != "ImageStream") | .metadata.labels) += {"app.kubernetes.io/instance": $instance}' |
      jq 'del(.items[] | select(.kind == "BuildConfig") | .spec.triggers)' | 
      oc -n 26e83e-tools apply -f - 
```

6. Build Jenkins Basic image
```
oc -n 26e83e-tools start-build "jenkins-basic${OC_P_SUFFIX}" --wait=true  
```

7. Create build config for Jenkins Main
```
oc -n 26e83e-tools process -f jenkins-main-build.yaml SOURCE_REPOSITORY_REF=${GH_BRANCH} SUFFIX=${OC_P_SUFFIX} SOURCE_IMAGE_STREAM_TAG=jenkins-basic:${OC_P_VERSION} VERSION=${OC_P_VERSION} | 
jq '(.items[] | .metadata.labels) += {"app.kubernetes.io/part-of": "jenkins"}' | 
jq --arg instance "jenkins${OC_P_SUFFIX}" '(.items[] | select(.kind != "ImageStream") | .metadata.labels) += {"app.kubernetes.io/instance": $instance}' | 
jq 'del(.items[] | select(.kind == "BuildConfig") | .spec.triggers)' | 
jq 'del(.items[] | select (.kind == "ImageStream"))' | 
oc -n 26e83e-tools apply -f - 
```

8. Build Jenkins Main image
```
oc -n 26e83e-tools start-build jenkins-main${OC_P_SUFFIX} --wait=true 
```

9. Set values of GH_USERNAME and GH_PASSWORD environment variables
10. Run Jenkins deployment. To persist changes in OpenShift remove "--dry-run=client -o yaml"
```
oc -n 26e83e-tools process -f jenkins-deploy.yaml NAME=jenkins SUFFIX=${OC_P_SUFFIX} "JENKINS_IMAGE_STREAM_NAME=jenkins-main:${OC_P_VERSION}" GH_USERNAME=blah GH_PASSWORD=blah | 
jq 'del(.items[] | select (.kind == "Secret" or .kind == "PersistentVolumeClaim"))' | 
jq '(.items[] | .metadata.labels) += {"app.kubernetes.io/part-of": "jenkins"}' |  
jq --arg instance "jenkins-prod" '(.items[] | select(.kind != "ImageStream") | 
.metadata.labels) += {"app.kubernetes.io/instance": $instance}'  | oc -n 26e83e-tools apply -f - --dry-run=client -o yaml
```

11. Create role binding for the new service account in the Test namespace.
```
cat <<EOF | oc -n 26e83e-test create -f -
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: jenkins_${PR_NUMBER}_edit
  namespace: 26e83e-test
roleRef:
  apiGroup: rbac.authorization.k8s.io
  name: edit
  kind: ClusterRole
subjects:
  - kind: ServiceAccount
    name: jenkins-${PR_NUMBER}
    namespace: 26e83e-tools
EOF
```

12. Create role binding for the new service account in the Prod namespace.
```
cat <<EOF | oc -n 26e83e-prod create -f -
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: jenkins_${PR_NUMBER}_edit
  namespace: 26e83e-prod
roleRef:
  apiGroup: rbac.authorization.k8s.io
  name: edit
  kind: ClusterRole
subjects:
  - kind: ServiceAccount
    name: jenkins-${PR_NUMBER}
    namespace: 26e83e-tools
EOF
```
