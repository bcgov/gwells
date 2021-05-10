FROM BuildConfig
ARG NODE_VERSION=v10.16.0
ARG SONAR_VERSION=3.3.0.1492
USER 0
RUN fix_permission() { while [[ $# > 0 ]] ; do chgrp -R 0 "$1" && chmod -R g=u "$1"; shift; done } && \
    set -x && \
    curl -sSL -o /tmp/sonar-scanner-cli.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_VERSION}-linux.zip && \
    unzip -q /tmp/sonar-scanner-cli.zip -d /tmp/sonar-scanner-cli && \
    mv /tmp/sonar-scanner-cli/sonar-scanner-${SONAR_VERSION}-linux /opt/sonar-scanner && \
    ln -s /opt/sonar-scanner/bin/sonar-scanner /usr/local/bin && \
    rm -rf /tmp/sonar-scanner-cli.zip && \
    rm -rf /tmp/sonar-scanner-cli && \
    mkdir /opt/node && \
    curl -sSL https://nodejs.org/dist/${NODE_VERSION}/node-${NODE_VERSION}-linux-x64.tar.gz | tar zxf - --strip-components=1 -C /opt/node && \
    fix_permission '/opt/sonar-scanner' '/opt/node' && \
    find  $JENKINS_REF_HOME -maxdepth 1 -type f -name '*.xml' -delete

ENV NODE_HOME=/opt/node \
    PATH=$PATH:/opt/node/bin \
    CASC_JENKINS_CONFIG=/var/lib/jenkins/casc_configs

COPY ./contrib/jenkins $JENKINS_REF_HOME

USER 1001
