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
  <Form @submit.prevent>
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
          <tr v-for="column in columns" :key="column.id">
            <td>{{ column.label }}</td>
            <td>
              <Checkbox
                :id="`${column.id}ColumnSelect`"
                binary
                v-model="localSelectedColumnIdsDict[column.id]"
                @input="$event ? selectColumn(column.id) : deselectColumn(column.id)"/>
            </td>
            <td>
              <Select
                :id="`${column.id}ColumnOrder`"
                :options="columnOrderRange"
                v-model="columnOrders[column.id]"
                @input="setColumnOrder(column.id, $event)"/>
            </td>
          </tr>
        </tbody>
      </table>
      <template #footer>
        <div class="flex justify-start">
          <Button label="Apply" @click="applyChanges()" :disabled="!validation" class="mr-2"/>
          <Button label="Cancel" severity="contrast" @click="cancelChanges()"/>
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
      localSelectedColumnIds: [],
      columnOrders: {},
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
    unselectedColumnIds () {
      return this.availableColumnIds.filter(id => !this.selectedColumnIds.includes(id))
    },
    columns () {
      const columns = this.availableColumnIds.map((columnId) => {
        const columnData = this.columnData[columnId]
        const label = columnData.resultLabel ? columnData.resultLabel : columnData.label
        return {
          id: columnId,
          label: label
        }
      })
      return Object.freeze(columns)
    },
    columnOrderRange () {
      return Array.from(Array(this.availableColumnIds.length).keys()).map(i => i + 1)
    },
    validation () {
      return this.localSelectedColumnIds.length > 0
    },
    localSelectedColumnIdsDict () {
      return this.columns.reduce((dict, column) => {
        dict[column.id] = this.localSelectedColumnIds.includes(column.id)
        return dict
      }, {})
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
    selectColumn (columnId) {
      this.localSelectedColumnIds.push(columnId)
    },
    deselectColumn (columnId) {
      const index = this.localSelectedColumnIds.indexOf(columnId)

      if (index >= 0) {
        this.localSelectedColumnIds.splice(index, 1)
      }
    },
    setColumnOrder (columnId, order) {
      const oldColumnOrder = this.columnOrders[columnId]
      const newColumnOrders = {}
      newColumnOrders[columnId] = order
      Object.entries(this.columnOrders).forEach(([entryId, entryOrder]) => {
        if (entryId === columnId) {
          newColumnOrders[entryId] = order
        } else if (entryOrder >= order && entryOrder < oldColumnOrder) {
          newColumnOrders[entryId] = entryOrder + 1
        } else {
          newColumnOrders[entryId] = entryOrder
        }
      })
      this.columnOrders = newColumnOrders
    },
    initColumnOrders () {
      const orderedColumns = [...this.selectedColumnIds, ...this.unselectedColumnIds]
      orderedColumns.forEach((columnId, index) => {
        this.columnOrders[columnId] = index + 1
      })
    },
    applyChanges () {
      const columnIds = [...this.localSelectedColumnIds]
      columnIds.sort((columnA, columnB) => {
        return this.columnOrders[columnA] - this.columnOrders[columnB]
      })
      localStorage.setItem('userColumnPreferences', JSON.stringify(columnIds))
      this.wells.setSearchResultColumns(columnIds)
      this.hideModal()
    },
    cancelChanges () {
      this.localSelectedColumnIds = [...this.selectedColumnIds]
      this.initColumnOrders()
      this.hideModal()
    }
  },
  created () {
    if (localStorage && localStorage.getItem('userColumnPreferences')) {
      this.localSelectedColumnIds = JSON.parse(localStorage.getItem('userColumnPreferences'))
    } else {
      this.localSelectedColumnIds = [...this.selectedColumnIds]
    }
    this.initColumnOrders()
    // listen for reset wells search so we can adjust our selected search columns
    this.wells = useWellsStore()
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
