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
  <b-form @submit.prevent>
    <b-button
      variant="dark"
      @click="showModal">
      Add/remove columns
    </b-button>
    <b-modal
      ref="column-select-modal"
      id="columnSelectModal"
      title="Column Display"
      footer-class="justify-content-start">
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
              <b-form-checkbox
                :id="`${column.id}ColumnSelect`"
                :checked="localSelectedColumnIds.includes(column.id)"
                @input="$event ? selectColumn(column.id) : deselectColumn(column.id)"
              />
            </td>
            <td>
              <b-form-select
                :id="`${column.id}ColumnOrder`"
                :options="columnOrderRange"
                :value="columnOrders[column.id]"
                @input="setColumnOrder(column.id, $event)" />
            </td>
          </tr>
        </tbody>
      </table>
      <div slot="modal-footer">
        <div class="d-flex justify-content-start">
          <b-button variant="primary" @click="applyChanges()" :disabled="!validation" class="mr-2">Apply</b-button>
          <b-button variant="dark" @click="cancelChanges()">Cancel</b-button>
        </div>
      </div>
    </b-modal>
  </b-form>
</template>

<script>
import { mapGetters } from 'vuex'
import { SET_SEARCH_RESULT_COLUMNS } from '@/wells/store/mutations.types.js'

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
  'wellOrientation',
  'surfaceSealMaterial',
  'surfaceSealDepth',
  'surfaceSealThickness',
  'surfaceSealMethod',
  'backfillAboveSurfaceSeal',
  'backfillDepth',
  'linerMaterial',
  'linerDiameter',
  'linerThickness',
  'linerRange',
  'screenIntakeMethod',
  'screenType',
  'screenMaterial',
  'otherScreenMaterial',
  'screenOpening',
  'screenBottom',
  'screenInformation',
  'filterPackRange',
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
  'waterQualityOdor',
  'ems',
  'finalCasingStickUp',
  'bedrockDepth',
  'staticWaterLevel',
  'wellYield',
  'artesianFlow',
  'artesianPressure',
  'wellCapType',
  'wellDisinfected',
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
  'storativity',
  'transmissivity',
  'hydraulicConductivity',
  'specificStorage',
  'specificYield',
  'testingMethod',
  'testingDuration',
  'analyticSolutionType',
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
  'decomissionEndDate'
]

export default {
  props: {
    columnData: Object
  },
  data () {
    return {
      localSelectedColumnIds: [],
      columnOrders: {}
    }
  },
  computed: {
    ...mapGetters({ selectedColumnIds: 'searchResultColumns' }),
    availableColumnIds () {
      return RESULT_COLUMNS.filter(
        columnId => this.columnData[columnId] !== undefined)
    },
    unselectedColumnIds () {
      return this.availableColumnIds.filter(id => !this.selectedColumnIds.includes(id))
    },
    columns () {
      const columns = this.availableColumnIds.map((columnId) => {
        return {
          id: columnId,
          label: this.columnData[columnId].label
        }
      })
      return Object.freeze(columns)
    },
    columnOrderRange () {
      return Array.from(Array(this.availableColumnIds.length).keys()).map(i => i + 1)
    },
    validation () {
      return this.localSelectedColumnIds.length > 0
    }
  },
  methods: {
    showModal () {
      this.$refs['column-select-modal'].show()
    },
    hideModal () {
      this.$refs['column-select-modal'].hide()
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
      this.$store.commit(SET_SEARCH_RESULT_COLUMNS, columnIds)
      this.hideModal()
    },
    cancelChanges () {
      this.localSelectedColumnIds = [...this.selectedColumnIds]
      this.initColumnOrders()
      this.hideModal()
    }
  },
  created () {
    this.localSelectedColumnIds = [...this.selectedColumnIds]
    this.initColumnOrders()
  }
}
</script>

<style>
</style>
