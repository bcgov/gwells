import java.util.regex.Pattern

class JenkinsInstall extends Script {
    def run() {
        println "Running ${args[0]}"
        File jenkinsHomeDir = new File(args[0]).getAbsoluteFile().getParentFile().getParentFile()
        File configXmlFile = new File(jenkinsHomeDir, 'jenkins.model.JenkinsLocationConfiguration.xml')
        File configXmlTemplateFile = new File(jenkinsHomeDir, 'jenkins.model.JenkinsLocationConfiguration.xml.template')
        String jenkinsURL = System.getenv()['JENKINS_URL']
        if ( !( jenkinsURL   ==~ /^https?:\/\/.*\/$/) ){
            throw new RuntimeException("Invalid JENKINS_URL. Expected to match '^https?://.*/\$'")
        }
        configXmlFile.withWriter { w ->
            configXmlTemplateFile.eachLine { line ->
                w << line.replaceAll(Pattern.quote('#{JENKINS_URL}'), jenkinsURL) + System.getProperty("line.separator")
            }
        }
    }

    static void main(String[] args) {           
        org.codehaus.groovy.runtime.InvokerHelper.runScript(JenkinsInstall, args)     
    }

}