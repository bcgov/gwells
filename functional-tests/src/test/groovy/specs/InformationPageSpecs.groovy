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

import pages.InformationPage
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
class InformationPageSpecs extends BaseSpec {

  @Unroll
  void 'Navigate Page from: InformationPage, click page Link: #TextSelector, Assert Page: #AssertPage'() {
    given: 'I start on the InformationPage'
      to InformationPage
    when: 'I click on the page link with label: #TextSelector.text'
      commonModule.clickPageLink(TextSelector, bodyContent)
    then: 'I arrive on the #AssertPage.getSimpleName()'
      at AssertPage
    where:
      TextSelector                                                    || AssertPage
      // TODO this page link is borken [ text:'groundwater wells in B.C.' ]                            || new ExternalLinkPage('WRBC', 'maps\\.gov\\.bc\\.ca.*wrbc')
      [ text:'Aquifers and the provincial observation well network' ] || new ExternalLinkPage('Understanding Aquifers - Province of British Columbia', 'www2\\.gov\\.bc\\.ca.*understanding-aquifers')
      [ text:'Data and mapping tools' ]                               || new ExternalLinkPage('Water Data & Tools - Province of British Columbia', 'www2\\.gov\\.bc\\.ca.*water-data-tools')
      [ text:'B.C. Water Resource Atlas' ]                            || new ExternalLinkPage('WRBC', 'maps\\.gov\\.bc\\.ca.*wrbc')
      [ text:'iMapBC' ]                                               || new ExternalLinkPage('iMapBC', 'maps\\.gov\\.bc\\.ca.*imap4m')
      [ text:'DataBC datasets' ]                                      || new ExternalLinkPage('Datasets - Data Catalogue', 'catalogue\\.data\\.gov\\.bc\\.ca')
      [ text:'FrontCounterBC location' ]                              || new ExternalLinkPage('Locations - Natural Resource Online Services', 'portal\\.nrs\\.gov\\.bc\\.ca.*locations')
  }
}
