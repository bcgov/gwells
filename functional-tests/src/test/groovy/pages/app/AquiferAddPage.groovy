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

class AquiferAddPage extends BaseAppPage {
  static at = { pageTitle.text() == 'Add new Aquifer' }
  static url = 'aquifers/new'
  static content = {
    pageTitle { $('main h4') }

    nameField { $('#aquifer-name') }
    locationDescriptionField { $('#aquifer-location-description') }
    materialDropdown { $('#aquifer-material') }
    qualityConcernDropdown { $('#aquifer-quality-concern') }
    sizeField { $('#aquifer-area') }
    knownWaterUseDropdown { $('#aquifer-known-water-use') }
    commentField { $('#aquifer-notes') }
    yearOfMappingField { $('#aquifer-mapping-year') }
    lithoStratigraphicUnitField { $('#aquifer-litho-stratigraphic-unit') }
    vulnerabilityDropdown { $('#aquifer-vulnerability') }
    subtypeDropdown { $('#aquifer-subtype') }
    productivityDropdown { $('#aquifer-productivity') }
    demandDropdown { $('#aquifer-demand') }

    saveButton { $('button', text:'Save') }
  }

  void setName(String name) {
    nameField.value(name)
  }

  void setLocationDescription(String description) {
    locationDescriptionField.value(description)
  }

  void setMaterial(String material) {
    materialDropdown.$('option', text:material).click()
  }

  void setQualityConcern(String qualityConcern) {
    qualityConcernDropdown.$('option', text:qualityConcern).click()
  }

  void setSize(double size) {
    sizeField.value(size)
  }

  void setKnownWaterUse(String knownWaterUse) {
    knownWaterUseDropdown.$('option', text:knownWaterUse).click()
  }

  void setComment(String comment) {
    commentField.value(comment)
  }

  void setYearOfMapping(int yearOfMapping) {
    yearOfMappingField.value(yearOfMapping)
  }

  void setLithoStratigraphicUnit(String lithoStratigraphicUnit) {
    lithoStratigraphicUnitField.value(lithoStratigraphicUnit)
  }

  void setVulnerability(String vulnerability) {
    vulnerabilityDropdown.$('option', text:vulnerability).click()
  }

  void setSubtype(String subtype) {
    subtypeDropdown.$('option', text:subtype).click()
  }

  void setProductivity(String productivity) {
    productivityDropdown.$('option', text:productivity).click()
  }

  void setDemand(String demand) {
    demandDropdown.$('option', text:demand).click()
  }

  void clickSaveButton() {
    saveButton.click()
  }
}
