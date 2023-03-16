def plugins1=[]
def plugins2=[]


def includePlugin={ plugin ->
    plugins2.add(plugin)
    def updateInfo=plugin.getUpdateInfo()
    if (updateInfo){
        println("${plugin.getShortName()}:${updateInfo.version}")
    }else{
        println("${plugin.getShortName()}:${plugin.getVersion()}")
    }
}

plugins1.addAll(Jenkins.instance.pluginManager.plugins);
plugins1=plugins1.sort({it.getShortName()})

def previousSize=-1;
def step=1;
while (plugins1.size()>0 && previousSize!=plugins1.size()){
    //println "##Step ${step}: ${plugins1.size()} - ${plugins2.size()}"
    previousSize=plugins1.size();
    def it2 = plugins1.iterator();
    while (it2.hasNext()) {
        def plugin = it2.next();
        if ((step ==1 && plugin.getDependencies().size()==0) || plugin.getDependencies().find({dependency -> plugins2.find({dependency.shortName.equals(it.getShortName())})==null})==null){
            it2.remove();
            includePlugin(plugin);
        }
    }
    step++;
}

// add all leftover (if any)
def it2 = plugins1.iterator();
while (it2.hasNext()) {
    def plugin = it2.next();
    it2.remove();
    includePlugin(plugin);
}

return;