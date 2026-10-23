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
<template>
  <Form>
    <Button label="Add/remove columns" severity="contrast" @click="showModal"/>
    <Dialog v-model:visible="modalShown" header="Column Display" id="columnSelectModal" centered modal>
      <table class="table">
        <thead>
          <tr>
            <th scope="col">Column Name</th>
            <th scope="col">Display</th>
            <th scope="col">Order</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(column, index) in localColumns" :key="column.id">
            <td>{{ column.label }}</td>
            <td>
              <Checkbox
                :id="`${column.id}ColumnSelect`"
                binary
                v-model="column.selected"/>
            </td>
            <td>
              <Select
                :id="`${column.id}ColumnOrder`"
                :options="columnOrderRange"
                optionLabel="label"
                optionValue="value"
                v-model="columnOrderRange[index].value"
                @change="setColumnOrder(index, $event.value)"/>
            </td>
          </tr>
        </tbody>
      </table>
      <template #footer>
        <div class="flex justify-start">
          <Button label="Apply" @click="applyChanges()" :disabled="!validation" class="mr-2"/>
          <Button label="Cancel" severity="secondary" @click="cancelChanges()"/>
        </div>
      </template>
    </Dialog>
  </Form>
</template>

<script>
import { useWellsStore } from '@/stores/wells.js'

const RESULT_COLUMNS = [
  'wellTagNumber',
  'identificationPlateNumber',
  'ownerName',
  'streetAddress',
  'legalLot',
  'legalPlan',
  'legalDistrictLot',
  'landDistrict',
  'legalPid',
  'diameter',
  'finishedWellDepth',
  'publicationStatus',
  'wellStatus',
  'licencedStatus',
  'personResponsible',
  'orgResponsible',
  'wellDepth',
  'aquiferNr',
  'wellClass',
  'wellSubclass',
  'intendedWaterUse',
  'wellIdPlateAttached',
  'idPlateAttachedBy',
  'waterSupplySystemName',
  'waterSupplyWellName',
  'drillerName',
  'consultantName',
  'consultantCompany',
  'ownerMailingAddress',
  'ownerCity',
  'ownerProvince',
  'ownerPostalCode',
  'legalBlock',
  'legalSection',
  'legalTownship',
  'legalRange',
  'locationDescription',
  'coordinateAcquisitionCode',
  'groundElevation',
  'groundElevationMethod',
  'drillingMethods',
  'wellOrientationStatus',
  'surfaceSealMaterial',
  'surfaceSealDepth',
  'surfaceSealThickness',
  'surfaceSealMethod',
  'backfillAboveSurfaceSeal',
  'backfillDepth',
  'linerMaterial',
  'linerDiameter',
  'linerThickness',
  'linerFrom',
  'linerTo',
  'screenIntakeMethod',
  'screenType',
  'screenMaterial',
  'otherScreenMaterial',
  'screenOpening',
  'screenBottom',
  'screenInformation',
  'filterPackFrom',
  'filterPackTo',
  'filterPackMaterial',
  'filterPackMaterialSize',
  'developmentMethods',
  'developmentHours',
  'developmentNotes',
  'yieldEstimationMethod',
  'yieldEstimationRate',
  'yieldEstimationDuration',
  'staticLevelBeforeTest',
  'hydroFracturingPerformed',
  'hydroFracturingYieldIncrease',
  'drawdown',
  'recommendedPumpDepth',
  'recommendedPumpRate',
  'waterQualityCharacteristics',
  'waterQualityColour',
  'waterQualityOdour',
  'ems',
  'finalCasingStickUp',
  'bedrockDepth',
  'staticWaterLevel',
  'wellYield',
  'artesianConditions',
  'wellCapType',
  'wellDisinfectedStatus',
  'observationWellNumber',
  'observationWellStatus',
  'decommissionReason',
  'decommissionMethod',
  'decommissionSealantMaterial',
  'decommissionBackfillMaterial',
  'decommissionDetails',
  'comments',
  'alternativeSpecsSubmitted',
  'internalComments',
  'aquiferLithology',
  'aquiferVulnerabilityIndex',
  'startDatePumpingTest',
  'storativity',
  'transmissivity',
  'hydraulicConductivity',
  'specificStorage',
  'specificYield',
  'specificCapacity',
  'pumpingTestDescription',
  'boundaryEffect',
  'createUser',
  'createDate',
  'updateUser',
  'updateDate',
  'constructionStartDate',
  'constructionEndDate',
  'alterationStartDate',
  'alterationEndDate',
  'decomissionStartDate',
  'decomissionEndDate',
  'licenceNumber'
]

export default {
  props: {
    columnData: Object
  },
  data () {
    return {
      localColumns: [],
      modalShown: false,
    }
  },
  computed: {
    selectedColumnIds () {
      return this.wells ? this.wells.searchResultColumns : []
    },
    availableColumnIds () {
      return RESULT_COLUMNS.filter(
        columnId => this.columnData[columnId] !== undefined)
    },
    columnOrderRange () {
      return Array.from({ length: this.localColumns.length }, (_, i) => ({ label: i + 1, value: i }))
    },
    validation () {
      return this.localColumns.some((column) => column.selected)
    }
  },
  methods: {
    handleReset () {
      this.$emit('reset')
    },
    showModal () {
      this.modalShown = true
    },
    hideModal () {
      this.modalShown = false
    },
    initColumns () {
      let columns = this.selectedColumnIds.map((columnId) => {
        const columnData = this.columnData[columnId]
        return {
          id: columnId,
          label: columnData.resultLabel ? columnData.resultLabel : columnData.label,
          selected: true,
        }
      })
      this.availableColumnIds.forEach((columnId) => {
        if (this.selectedColumnIds.includes(columnId)) return
        const columnData = this.columnData[columnId]
        columns.push({
          id: columnId,
          label: columnData.resultLabel ? columnData.resultLabel : columnData.label,
          selected: false,
        })
      })
      this.localColumns = columns
    },
    setColumnOrder (prevIndex, nextIndex) {
      // Don't think this is possible, but including just-in-case
      if (nextIndex === prevIndex) return

      const column = this.localColumns[prevIndex]
      // Remove the column and reinsert it
      this.localColumns.splice(prevIndex, 1)
      this.localColumns.splice(nextIndex, 0, column)
    },
    applyChanges () {
      let newColumnIds = []
      this.localColumns.forEach((column) => {
        if (column.selected) {
          newColumnIds.push(column.id)
        }
      })
      localStorage.setItem('userColumnPreferences', JSON.stringify(newColumnIds))
      this.wells.setSearchResultColumns(newColumnIds)
      this.hideModal()
    },
    cancelChanges () {
      this.initColumns()
      this.hideModal()
    }
  },
  created () {
    this.wells = useWellsStore()
    this.initColumns()
    // listen for reset wells search so we can adjust our selected search columns
    if (this.wells.$onAction) {
      this.unsubscribeAction = this.wells.$onAction(({ name }) => {
        if (name === 'resetWellsSearch') {
          this.$nextTick(() => { this.handleReset() })
        }
      })
    }
  }
  ,
  beforeUnmount () {
    if (this.unsubscribeAction) {
      this.unsubscribeAction()
    }
  }
}
</script>

<style>
</style>
