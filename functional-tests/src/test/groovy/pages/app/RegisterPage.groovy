package pages.app

import geb.Page

class RegisterPage extends Page {
	// NOTE - the title comparison is based on parsed HTML, not an exact character match of the HTML source.  For example "  " becomes " ". 
	// So even though there are currently two spaces after Wells in the page source, we have to compare against a single space after Wells.
    static at = { title == "Groundwater Wells Registry - Province of British Columbia"}
    static url = "gwells/registries"
    
    static content = {
        titletext { $("h2").text() }
        reset { $("#personSearchReset").click() }
        submit { $("#personSearchSubmit").click() }
        search { $("#regTypeInput") }
        firstrow { $("#registry-table-row-0") }
        result { $("#drillersTotalResults").text() }
        selectinstaller { $("#activityInstaller").click() }
        selectdriller { $("#activityDriller").click() }
        noresults { $("div", text:"No results were found.") }
        selectcommunity { $("form",id:"drillerSearchForm").$("#cityOptions") }
    }
}
