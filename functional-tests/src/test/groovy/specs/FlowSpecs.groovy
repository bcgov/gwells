/*
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/

package specs

import pages.HomePage
import pages.AquifersPage
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
class FlowSpecs extends BaseSpec {

  @Unroll
  void 'Navigate Page from: HomePage, click header Link: #TextSelector, Assert Page: #AssertPage'() {
    given: 'I start on the HomePage'
      to HomePage
    when: 'I click on the header link with label: #TextSelector'
      headerModule.clickMenuItem(TextSelector)
    then: 'I arrive on the #AssertPage.getSimpleName()'
      at AssertPage
    where:
      TextSelector              || AssertPage
      'Well Search'             || HomePage
      'Aquifers'                || AquifersPage
      'Groundwater Information' || InformationPage
      'Registry'                || RegistryPage
      //TODO requires being logged - move to auth flow specs? 'Submit Report'           || SubmissionsPage
  }

  @Unroll
  void 'Navigate Page from: HomePage, click page Link: #TextSelector, Assert Page: #AssertPage'() {
    given: 'I start on the HomePage'
      to HomePage
    when: 'I click on the page link with label: #TextSelector'
      commonModule.clickPageLink(TextSelector, bodyContent)
    then: 'I arrive on the #AssertPage.getSimpleName()'
      at AssertPage
    where:
      TextSelector                || AssertPage
      'B.C. Water Resource Atlas' || new ExternalLinkPage('WRBC', 'maps\\.gov\\.bc\\.ca.*wrbc')
      'iMapBC'                    || new ExternalLinkPage('iMapBC', 'maps\\.gov\\.bc\\.ca.*imap4m')
  }

  @Unroll
  void 'Navigate Page from: InformationPage, click page Link: #TextSelector, Assert Page: #AssertPage'() {
    given: 'I start on the InformationPage'
      to InformationPage
    when: 'I click on the page link with label: #TextSelector'
      commonModule.clickPageLink(TextSelector, bodyContent)
    then: 'I arrive on the #AssertPage.getSimpleName()'
      at AssertPage
    where:
      TextSelector                || AssertPage
      'groundwater wells in B.C.' || new ExternalLinkPage('Groundwater Wells & Aquifers - Province of British Columbia',
                                                          'www2\\.gov\\.bc\\.ca.*groundwater-wells-aquifers')
      'Aquifers and the provincial observation well network' || new ExternalLinkPage(
                                                                'Understanding Aquifers - Province of British Columbia',
                                                                'www2\\.gov\\.bc\\.ca.*understanding-aquifers')
      'Data and mapping tools'    || new ExternalLinkPage('Water Data & Tools - Province of British Columbia',
                                                          'www2\\.gov\\.bc\\.ca.*water-data-tools')
      'B.C. Water Resource Atlas' || new ExternalLinkPage('WRBC', 'maps\\.gov\\.bc\\.ca.*wrbc')
      'iMapBC'                    || new ExternalLinkPage('iMapBC', 'maps\\.gov\\.bc\\.ca.*imap4m')
      'DataBC datasets'           || new ExternalLinkPage('Datasets - Data Catalogue',
                                                          'catalogue\\.data\\.gov\\.bc\\.ca.*dataset.*groundwater')
      'FrontCounterBC location'   || new ExternalLinkPage('Locations - Natural Resource Online Services',
                                                          'portal\\.nrs\\.gov\\.bc\\.ca.*locations')
  }

  @Unroll
  void 'Navigate Page from: RegistryPage, click page Link: #TextSelector, Assert Page: #AssertPage'() {
    given: 'I start on the RegistryPage'
      to RegistryPage
    when: 'I click on the page link with label: #TextSelector'
      commonModule.clickPageLink(TextSelector, bodyContent)
    then: 'I arrive on the #AssertPage.getSimpleName()'
      at AssertPage
    where:
      TextSelector                                                                    || AssertPage
      'Learn more about registering as a well driller or well pump installer in B.C.' || new ExternalLinkPage(
                            'Register as a Water Well Driller or Pump Installer in B.C. - Province of British Columbia',
                            'www2\\.gov\\.bc\\.ca.*what-you-need-to-practice-in-bc')
  }

  @Unroll
  void 'Navigate Page from: HomePage, click footer Link: #TextSelector, Assert Page: #AssertPage'() {
    given: 'I start on the HomePage'
      to HomePage
    when: 'I click on the footer link with label: #TextSelector'
      footerModule.clickMenuItem(TextSelector)
    then: 'I arrive on the #AssertPage.getSimpleName()'
      at AssertPage
    where:
      TextSelector      || AssertPage
      'Home'            || new ExternalLinkPage('B\\.C\\. Homepage - Province of British Columbia',
                                                'www2\\.gov\\.bc\\.ca')
      'About gov.bc.ca' || new ExternalLinkPage('About gov.bc.ca - Province of British Columbia',
                                                'www2\\.gov\\.bc\\.ca.*about')
      'Disclaimer'      || new ExternalLinkPage('Disclaimer - Province of British Columbia',
                                                'www2\\.gov\\.bc\\.ca.*disclaimer')
      'Privacy'         || new ExternalLinkPage(
                                        'B\\.C\\. Government Website Privacy Statement - Province of British Columbia',
                                        'www2\\.gov\\.bc\\.ca.*privacy')
      'Accessibility'   || new ExternalLinkPage('Web Accessibility - Province of British Columbia',
                                                'www2\\.gov\\.bc\\.ca.*accessibility')
      'Copyright'       || new ExternalLinkPage('Copyright - Province of British Columbia',
                                                'www2\\.gov\\.bc\\.ca.*copyright')
      'Contact Us'      || new ExternalLinkPage('Contact Us - Province of British Columbia',
                                                'www2\\.gov\\.bc\\.ca.*contact')
  }
}
