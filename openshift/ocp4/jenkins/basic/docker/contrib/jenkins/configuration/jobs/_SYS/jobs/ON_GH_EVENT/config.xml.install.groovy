import java.util.regex.Pattern

class JobInstall extends Script {
static Map exec(List args, Appendable stdout=null, Appendable stderr=null, Closure stdin=null){
    ProcessBuilder builder = new ProcessBuilder(args)
    def proc = builder.start()

    if (stdin!=null) {
        OutputStream out = proc.getOutputStream();
        stdin(out)
        out.flush();
        out.close();
    }

    if (stdout == null ){
        stdout = new StringBuffer()
    }

    proc.waitForProcessOutput(stdout, stderr)
    int exitValue= proc.exitValue()

    Map ret = ['out': stdout, 'err': stderr, 'status':exitValue, 'cmd':args]

    return ret
}

    def run() {
        println "Running ${args[0]}"

        String secretToken = UUID.randomUUID()
        Map ocGetSecretToken = exec(['sh', '-c', "set -x; oc get \"secret/\$(cat /var/run/secrets/github/metadata.name)\" \"--output=jsonpath={.data['generic-hook\\.token']}\" | base64 --decode"])

        if (ocGetSecretToken.status != 0 || ocGetSecretToken.out.toString().trim() == ""){
            println "Updating/Creating token"
            exec(['sh', '-c', "oc patch \"secret/\$(cat /var/run/secrets/github/metadata.name)\" -p '{\"stringData\": {\"generic-hook.token\": \"${secretToken}\"}}'" as String])
        }else{
            println "Using existing token"
            secretToken = ocGetSecretToken.out.toString().trim()
        }

        def installFile = args[0]
        def configXmlFile = installFile.substring(0, installFile.length() - '.install.groovy'.length())
        def configXmlTemplateFile = configXmlFile + '.template'

        //println "configXmlFile:${configXmlFile}"
        //println "configXmlTemplateFile:${configXmlTemplateFile}"

        new File( configXmlFile ).withWriter { w ->
            new File(configXmlTemplateFile).eachLine { line ->
                w << line.replaceAll(Pattern.quote('#{TOKEN}'), secretToken ) + System.getProperty("line.separator")
            }
        }

        return null
    }

    static void main(String[] args) {           
        org.codehaus.groovy.runtime.InvokerHelper.runScript(JobInstall, args)     
    }

}