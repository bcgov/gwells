package pages.external

import geb.Page

class AquiferReport extends Page {
    static String aquiferNumber
    static at = { title == "Groundwater" }
    static url = "http://a100.gov.bc.ca/pub/wells/aquiferDetail.do?aquiferNumber=" + aquiferNumber + "&docType=adr"
}



