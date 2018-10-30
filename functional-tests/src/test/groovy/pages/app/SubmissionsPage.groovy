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

package pages

import org.openqa.selenium.Keys

class SubmissionsPage extends BaseAppPage {
  static at = { (pageTitle.text() =~ 'Well Activity Submission') as Boolean }
  static url = 'submissions'
  static content = {
    pageTitle { $('main .card-title') } // TODO improve this selector

    // General

    singlePageRadioButton { $('#singleSubmissionPage') }
    multiPageRadioButton { $('#multiSubmissionPage') }
    nextButton { $('#nextSubmissionStep') }

    previewButton { $('#formPreviewButton') }

    // Report Type

    reportTypeRadioButtons { $('#reportType') }

    // Class

    wellClassGroup { $('#wellClass') }
    wellSubClassGroup { $('#wellSubclass') }
    startDateOfWork { $('#workStartDateInputInput') }
    endDateOfWork { $('#workEndDateInputInput') }
    personResponsibleForDrilling { $('#personResponsibleSelect') }

    // Owner

    ownerName { $('#ownerFullNameInput') }
    ownerAddress { $('#ownerMailingAddressInput') }
    ownerCity { $('#ownerCityInput') }
    ownerPostalCode { $('#ownerPostalCodeInput') }
    ownerProvinceGroup { $('#ownerProvince') }

    // Location

    locationAddress { $('#wellStreetAddressInput') }
    locationCity { $('#wellCityInput') }

    // Method of Drilling

    drillingMethod { $('#drillingMethodInput') }

    // Casing

    casingTable { $('#casingTable') }
    addCasingButton { $('#addCasingRowBtn') }

    // Liner Perforations

    addLinerPerforationButton { $('#addlinerPerforationRowBtn') }

    // Screen

    addScreenButton { $('#addScreenRowButton') }

    // Comment

    commentField { $('#commentsEntry') }
  }

  // General

  void clickSinglePageButton() {
    singlePageRadioButton.parent().click()
  }

  void clickMultiPageButton() {
    multiPageRadioButton.parent().click()
  }

  void clickNextButton() {
    nextButton.click()
  }

  void clickPreviewButton() {
    previewButton.click()
  }

  // Report Type

  void setConstructionReportType(String type) {
    reportTypeRadioButtons.$('label', text:type).click()
  }

  // Class

  void setWellClass(String wellClass) {
    wellClassGroup.$('option', text:wellClass).click()
  }

  void setWellSubClass(String wellSubClass) {
    // note: the well sub class dropdown is not populated until the well class is chosen
    wellSubClassGroup.$('option', text:wellSubClass).click()
  }

  void setStartDateOfWork(String day, String month, String year) {
    // This is a workaround for an issue where calling: effectiveDateField.value('2018-10-10') appears to correctly set
    // the date, but as soon as another element is interacted with the effective date 'unsets' to be empty again.
    // Calling .value() should work according to the doc, assuming no other javascript is messing with the field.
    startDateOfWork << day
    startDateOfWork << month
    // Setting the day value auto advances to the month, but setting the month does not auto advance to the year.
    // Simulate the user clicking the right arrow to move to the next field.
    startDateOfWork << Keys.ARROW_RIGHT
    startDateOfWork << year
  }

  void setEndDateOfWork(String day, String month, String year) {
    // This is a workaround for an issue where calling: effectiveDateField.value('2018-10-10') appears to correctly set
    // the date, but as soon as another element is interacted with the effective date 'unsets' to be empty again.
    // Calling .value() should work according to the doc, assuming no other javascript is messing with the field.
    endDateOfWork << day
    endDateOfWork << month
    // Setting the day value auto advances to the month, but setting the month does not auto advance to the year.
    // Simulate the user clicking the right arrow to move to the next field.
    endDateOfWork << Keys.ARROW_RIGHT
    endDateOfWork << year
  }

  void setPersonResponsibleForDrilling(String person) {
    // Enter the name of the desired driller in the search
    personResponsibleForDrilling.$('input').value(person)
    interact {
      waitFor {
        // wait for the dropdown to populate and click the element in the list with the matching text
        moveToElement(personResponsibleForDrilling.$('.dropdown-menu').$('li', text:~"$person")).click()
      }
    }
  }

  // Owner

  void setOwnerName(String name) {
    ownerName.value(name)
  }

  void setOwnerAddress(String address) {
    ownerAddress.value(address)
  }

  void setOwnerCity(String city) {
    ownerCity.value(city)
  }

  void setOwnerPostalCode(String postalCode) {
    ownerPostalCode.value(postalCode)
  }

  void setOwnerProvince(String province) {
    ownerProvinceGroup.$('option', text:province).click()
  }

  // Location

  void setLocationAddress(String address) {
    locationAddress.value(address)
  }

  void setLocationCity(String city) {
    locationCity.value(city)
  }

  // Method of Drilling

  void setDrillingMethod(String method) {
    drillingMethod.$('option', text:method).click()
  }

  // Casing

  void setCasingFrom(String casingFrom, int rowNumber) {
    $("#casingFrom_${rowNumber}Input").value(casingFrom)
  }

  void setCasingTo(String casingFrom, int rowNumber) {
    $("#casingTo_${rowNumber}Input").value(casingFrom)
  }

  void setCasingType(String casingType, int rowNumber) {
    $("#casingCode_${rowNumber}").$('option', text:casingType).click()
  }

  void setCasingMaterial(String casingMaterial, int rowNumber) {
    $("#casingMaterial_${rowNumber}").$('option', text:casingMaterial).click()
  }

  void setCasingDiameter(String diameter, int rowNumber) {
    $("#casingDiameter_${rowNumber}Input").value(diameter)
  }

  void setCasingWallThickness(String thickness, int rowNumber) {
    $("#casingWallThickness_${rowNumber}Input").value(thickness)
  }

  void setCasingDriveShoe(String value, int rowNumber) {
    // initially find the element based on the input value
    // but because this field is obstructed, click the sibling label element instead
    $("#casingDriveShoe_${rowNumber}").$('input', value:value).siblings('label').click()
  }

  void addCasingRow(int rowNumber) {
    addCasingButton.click()
  }

  void removeCasingRow(int rowNumber) {
    $("#removeCasingRowBtn${rowNumber}").click()
  }

  // Liner Perforations

  void setLinerPerforationFrom(String perforationFrom, int rowNumber) {
    $("#liner_perforated_from_${rowNumber}Input").value(perforationFrom)
  }

  void setLinerPerforationTo(String perforationTo, int rowNumber) {
    $("#liner_perforated_to_${rowNumber}Input").value(perforationTo)
  }

  void addLinerPerforationRow(int rowNumber) {
    addLinerPerforationButton.click()
  }

  void removeLinerPerforationRow(int rowNumber) {
    $("#removeLinerPerfRowBtn${rowNumber}").click()
  }

  // Screen

  void setScreenFrom(String perforationFrom, int rowNumber) {
    $("#screenDepthFrom_${rowNumber}Input").value(perforationFrom)
  }


  void setScreenTo(String screenTo, int rowNumber) {
    $("#screenDepthTo_${rowNumber}Input").value(screenTo)
  }

  void setScreenDiameter(String screenFrom, int rowNumber) {
    $("#screenDiameter_${rowNumber}Input").value(screenFrom)
  }

  void setScreenAssemblyType(String screenAssemblyType, int rowNumber) {
    $("#screenAssemblyType_${rowNumber}Input").$('option', text:screenAssemblyType).click()
  }

  void setScreenSlotSize(String screenSlotSize, int rowNumber) {
    $("#screenSlotSize_${rowNumber}Input").value(screenSlotSize)
  }

  void addScreenRow(int rowNumber) {
    addLinerPerforationButton.click()
  }

  void removeScreenRow(int rowNumber) {
    $("#removeScreenRowButton${rowNumber}").click()
  }

  // Comment

  void setComment(String comment) {
    commentField.value(comment)
  }
}
