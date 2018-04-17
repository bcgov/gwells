import geb.spock.GebReportingSpec
import spock.lang.*

@Title("Migrate Existing Data from MS Access into GWELLS")
@Narrative("""As the Deputy Comptroller and groundwater data specialist , I need the existing well driller and well pump installer registry information 
to be imported into the GWELLS database in order to ensure a smooth transition between the systems and to ensure that the information 
is available to the public in a timely manner.""")
@See("https://trello.com/c/4alSc2bU")
class MigrateDataSpecs extends GebReportingSpec {

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/4alSc2bU")
    def "Scenario: 1 - Migrate Data"(){
        given "that I have data related to the registry of well drillers and well pump installers in an existing MS Access table"
        and "I want that data imported into the GWELLS database"
        when "I import the data based on the column mapping spreadsheet"
        then "the appropriate columns should be populated."
     }
}
