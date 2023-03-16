function generate_passwd_file() {
  USER_ID=$(id -u)
  GROUP_ID=$(id -g)

  if [ x"$USER_ID" != x"0" -a x"$USER_ID" != x"997" ]; then
    echo "default:x:${USER_ID}:${GROUP_ID}:Default Application User:${HOME}:/sbin/nologin" >> /etc/passwd
  fi
}

function generate_jenkins_user() {
    local username="$1"
    local password="$2"

local password_hash=`java -classpath "$(find $JENKINS_WEBROOT_DIR/WEB-INF/lib/ -name acegi-security-*.jar):$(find $JENKINS_WEBROOT_DIR/WEB-INF/lib/ -name commons-codec-*.jar):/opt/openshift/password-encoder.jar" com.redhat.openshift.PasswordEncoder superSecret pvKndZ`

cat >$JENKINS_HOME/users/$username/config.xml <<EOF
<?xml version='1.0' encoding='UTF-8'?>
<user>
  <fullName>${username}</fullName>
  <properties>
    <hudson.model.MyViewsProperty>
      <views>
        <hudson.model.AllView>
          <owner class="hudson.model.MyViewsProperty" reference="../../.."/>
          <name>All</name>
          <filterExecutors>false</filterExecutors>
          <filterQueue>false</filterQueue>
          <properties class="hudson.model.View$PropertyList"/>
        </hudson.model.AllView>
      </views>
    </hudson.model.MyViewsProperty>
    <hudson.security.HudsonPrivateSecurityRealm_-Details>
      <passwordHash>${password_hash}</passwordHash>
    </hudson.security.HudsonPrivateSecurityRealm_-Details>
    <hudson.tasks.Mailer_-UserProperty>
      <emailAddress>changeme@changeme.com</emailAddress>
    </hudson.tasks.Mailer_-UserProperty>
  </properties>
</user>
EOF
}
