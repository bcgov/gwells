package specs

import pages.HomePage
import pages.InformationPage
import pages.RegistryPage
import pages.SubmissionsPage
import pages.ExternalLinkPage

import spock.lang.Timeout
import spock.lang.Title
import spock.lang.Narrative
import spock.lang.Unroll

@Timeout(60)
@Title('Groundwater wells Flow Tests')
@Narrative('''
As a developer, I want to ensure all page links work, have the correct text, and direct to the correct page.
''')
class FlowSpecs extends LoggedInSpec {

  void setup() {
    logInAsAdminUser()
  }

  @Unroll
  void 'Navigate Page from: HomePage, click header Link: #TextSelector, Assert Page: #AssertPage'() {
    given: 'I start on the HomePage'
      to HomePage
    when: 'I click on the header link with label: #TextSelector.text'
      headerModule.clickMenuItem(TextSelector)
    then: 'I arrive on the #AssertPage.getSimpleName()'
      at AssertPage
    where:
      TextSelector                       || AssertPage
      [ text:'Well Search' ]             || HomePage
      [ text:'Groundwater Information' ] || InformationPage
      [ text:'Registry' ]                || RegistryPage
      [ text:'Submit Report' ]           || SubmissionsPage
  }

  @Unroll
  void 'Navigate Page from: HomePage, click footer Link: #TextSelector, Assert Page: #AssertPage'() {
    given: 'I start on the HomePage'
      to HomePage
    when: 'I click on the footer link with label: #TextSelector.text'
      footerModule.clickMenuItem(TextSelector)
    then: 'I arrive on the #AssertPage.getSimpleName()'
      at AssertPage
    where:
      TextSelector               || AssertPage
      [ text:'Home' ]            || new ExternalLinkPage('B\\.C\\. Homepage - Province of British Columbia',
                                                         'www2\\.gov\\.bc\\.ca')
      [ text:'About gov.bc.ca' ] || new ExternalLinkPage('About gov.bc.ca - Province of British Columbia',
                                                         'www2\\.gov\\.bc\\.ca.*about')
      [ text:'Disclaimer' ]      || new ExternalLinkPage('Disclaimer - Province of British Columbia',
                                                         'www2\\.gov\\.bc\\.ca.*disclaimer')
      [ text:'Privacy' ]         || new ExternalLinkPage('B\\.C\\. Government Website Privacy Statement - Province of \
                                                          British Columbia', 'www2\\.gov\\.bc\\.ca.*privacy')
      [ text:'Accessibility' ]   || new ExternalLinkPage('Web Accessibility - Province of British Columbia',
                                                         'www2\\.gov\\.bc\\.ca.*accessibility')
      [ text:'Copyright' ]       || new ExternalLinkPage('Copyright - Province of British Columbia',
                                                         'www2\\.gov\\.bc\\.ca.*copyright')
      [ text:'Contact Us' ]      || new ExternalLinkPage('Contact Us - Province of British Columbia',
                                                         'www2\\.gov\\.bc\\.ca.*contact')
  }
}
