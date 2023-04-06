import groovy.json.*

class OnStartup extends Script {
    def run() {
        println "On Startup"
        return null;
    } //end run
    
    static void main(String[] args) {
        org.codehaus.groovy.runtime.InvokerHelper.runScript(OnStartup, args)     
    }
}