import jenkins.*
import jenkins.model.*

class JobInstall extends Script {
    def run() {
        println "${args}"
    }
    static void main(String[] args) {           
        org.codehaus.groovy.runtime.InvokerHelper.runScript(JobInstall, args)     
    }

}