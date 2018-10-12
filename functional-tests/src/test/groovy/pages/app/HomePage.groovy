package pages.app

import geb.Page

class HomePage extends Page {
	// NOTE - the title comparison is based on parsed HTML, not an exact character match of the HTML source.  For example "  " becomes " ". 
	// So even though there are currently two spaces after Wells in the page source, we have to compare against a single space after Wells.
    static at = { title == "Groundwater Wells - Province of British Columbia" }
    static url = "gwells"
}
