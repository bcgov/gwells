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

import pages.SubmissionsPage
import pages.SubmissionsPreviewPage
import pages.SubmissionsConfirmSubmitModal

import spock.lang.Title
import spock.lang.Narrative
import spock.lang.Stepwise

@Stepwise
@Title('Groundwater Well Submissions Tests')
@Narrative('''As a submission user, I want to create a new well submission report.''')
class SubmissionsSpecs extends LoggedInSpec {

  void 'Creating a new well construction submission report'() {
    given: 'I am logged in as a submission user'
      logInAsSubmissionUser()
      to SubmissionsPage
    and: 'I populate all required fields for a new well construction submission report'
      clickSinglePageButton()
      // Report Type
      setConstructionReportType('Construction')
      // Class
      setStartDateOfWork('01', '02', '2010')
      setEndDateOfWork('24', '11', '2017')
      setPersonResponsibleForDrilling('Pump Installer')
      // Owner
      setOwnerName('owner')
      setOwnerAddress('123 Owner St')
      setOwnerCity('OwnerCity')
      setOwnerPostalCode('A1A1A1')
      setOwnerProvince('British Columbia')
      // Owner
      setLocationAddress('123 Location St')
      setLocationCity('Victoria')
      // Method of Drilling
      setDrillingMethod('Auger')
      // Casing
      setCasingFrom('1', 0)
      setCasingTo('2', 0)
      setCasingType('Surface casing', 0)
      setCasingMaterial('Steel', 0)
      setCasingDiameter('3', 0)
      setCasingWallThickness('4', 0)
      setCasingDriveShoe('True', 0)
      removeCasingRow(1)
      removeCasingRow(1)
      // Liner Perforation
      setLinerPerforationFrom('5', 0)
      setLinerPerforationTo('6', 0)
      removeLinerPerforationRow(1)
      removeLinerPerforationRow(1)
      // Screen
      setScreenFrom('7', 0)
      setScreenTo('8', 0)
      setScreenDiameter('9', 0)
      setScreenAssemblyType('Screen', 0)
      setScreenSlotSize('10', 0)
      removeScreenRow(1)
      removeScreenRow(1)
      // Comment
      setComment('Creating a new well construction submission report')
    when: 'I save the report'
      clickPreviewButton()
      at SubmissionsPreviewPage
      clickSubmitButton()
      page(SubmissionsConfirmSubmitModal)
      confirmSubmit()
    then: 'The well construction submission report is submitted and a success alert is displayed'
      page(SubmissionsPreviewPage)
      submitReportSuccessAlertDisplayed()
  }
}
