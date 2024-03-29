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
  <b-form @submit.prevent="handleSubmit()" @reset.prevent="handleReset()">
    <div v-for="section in defaultFilterSections" :key="section.header">
      <b-row class="mt-1">
        <b-col>
          <h3>{{ section.header }}</h3>
        </b-col>
      </b-row>
      <search-filter
        v-for="field in getFilterFields(section.fields)"
        :key="field.id"
        :type="field.type"
        :id="`${field.id}Filter`"
        :param-names="field.params"
        :label="field.label"
        :errors="errors[field.param]"
        :options="field.options || filterSelectOptions[field.id]"
        :value-field="field.valueField"
        :text-field="field.textField"
        :any-value-checkbox="field.anyValueBoolean"
        v-model="filterParams[field.id]" />
    </div>
    <b-row>
      <b-col class="my-3">
        <b-btn variant="primary" type="submit" :disabled="searchInProgress">Search</b-btn>
        <b-btn variant="dark" type="reset" :disabled="searchInProgress" class="mx-2">Reset</b-btn>
      </b-col>
    </b-row>
    <b-row class="mt-1">
      <b-col>
        <h3>Additional Fields</h3>
      </b-col>
    </b-row>
    <search-filter
      v-for="field in selectedAdditionalFilters"
      :key="field.id"
      :type="field.type"
      :id="`${field.id}Filter`"
      :param-names="field.params"
      :label="field.label"
      :errors="errors[field.param]"
      :options="field.options || filterSelectOptions[field.id]"
      :value-field="field.valueField"
      :text-field="field.textField"
      :any-value-checkbox="field.anyValueBoolean"
      v-model="filterParams[field.id]"
      @remove="removeSelectedFilter(field.id)"
      removable />
    <b-row>
      <b-col sm="9" class="mb-1">
        <b-form-select id="additionalFilterInput" v-model="selectedFilterId">
          <option :value="null">Select a field</option>
          <optgroup v-for="optGroup in additionalFilterSelectOptions" :key="optGroup.label" :label="optGroup.label">
            <option v-for="option in optGroup.options" :key="option.id" :value="option.value" :disabled="option.disabled">{{ option.text }}</option>
          </optgroup>
        </b-form-select>
      </b-col>
      <b-col sm="3" class="mb-1">
        <b-button block variant="primary" @click="addSelectedFilter" :disabled="selectedFilterId === null">Add Field</b-button>
      </b-col>
    </b-row>
  </b-form>
</template>

<script>
import { mapGetters } from 'vuex'
import { FETCH_CODES } from '@/submissions/store/actions.types.js'
import {
  FETCH_DRILLER_NAMES,
  FETCH_ORGANIZATION_NAMES,
  RESET_WELLS_SEARCH,
  SEARCH_WELLS
} from '@/wells/store/actions.types.js'
import { SET_SEARCH_PARAMS } from '@/wells/store/mutations.types.js'
import { SEARCH_TRIGGER } from '@/wells/store/triggers.types.js'
import AdvancedSearchFilter from '@/wells/components/AdvancedSearchFilter.vue'
import filterMixin from '@/wells/components/mixins/filters.js'

const ADDITIONAL_FILTER_SECTIONS = [
  { header: 'Well Class',
    fields:
     [ 'wellClass',
       'wellSubclass',
       'intendedWaterUse',
       'wellIdPlateAttached' ] },
  { header: 'Person responsible for work',
    fields: [ 'drillerName', 'consultantName', 'consultantCompany' ] },
  { header: 'Well owner',
    authenticated: true,
    fields:
     [ 'ownerMailingAddress',
       'ownerCity',
       'ownerProvince',
       'ownerPostalCode' ] },
  { header: "Licence Information",
    fields:
     [ 'licenceNumber'] },
  { header: 'Well location',
    fields:
     [ 'legalBlock',
       'legalSection',
       'legalTownship',
       'legalRange',
       'locationDescription' ] },
  { header: 'Geocoordinates',
    fields: [ 'coordinateAcquisitionCode' ] },
  { header: 'Method of drilling',
    fields:
     [ 'groundElevation',
       'groundElevationMethod',
       'drillingMethods',
       'wellOrientationStatus' ] },
  { header: 'Surface seal and backfill material',
    fields:
     [ 'surfaceSealMaterial',
       'surfaceSealDepth',
       'surfaceSealThickness',
       'surfaceSealMethod',
       'backfillAboveSurfaceSeal',
       'backfillDepth' ] },
  { header: 'Liner information',
    fields:
     [ 'linerMaterial',
       'linerDiameter',
       'linerThickness',
       'linerRange' ] },
  { header: 'Screen information',
    fields:
     [ 'screenIntakeMethod',
       'screenType',
       'screenMaterial',
       'otherScreenMaterial',
       'screenOpening',
       'screenBottom',
       'screenInformation' ] },
  { header: 'Filter pack',
    fields:
     [ 'filterPackRange',
       'filterPackMaterial',
       'filterPackMaterialSize' ] },
  { header: 'Well development',
    fields:
     [ 'developmentMethods', 'developmentHours' ] },
  { header: 'Yield',
    fields:
     [ 'yieldEstimationMethod',
       'yieldEstimationRate',
       'yieldEstimationDuration',
       'staticLevelBeforeTest',
       'hydroFracturingPerformed',
       'hydroFracturingYieldIncrease',
       'drawdown',
       'recommendedPumpDepth',
       'recommendedPumpRate' ] },
  { header: 'Water quality',
    fields:
     [ 'waterQualityCharacteristics',
       'waterQualityColour',
       'waterQualityOdour',
       'ems' ] },
  { header: 'Well completion data',
    fields:
     [ 'finalCasingStickUp',
       'bedrockDepth',
       'staticWaterLevel',
       'wellYield',
       'artesianConditions',
       'wellCapType',
       'wellDisinfectedStatus' ] },
  { header: 'Observation well information',
    fields: [ 'observationWellNumber', 'observationWellStatus' ] },
  { header: 'Decommission',
    fields:
     [ 'finishedWellDepth',
       'decommissionReason',
       'decommissionMethod',
       'decommissionSealantMaterial',
       'decommissionBackfillMaterial',
       'decommissionDetails' ] },
  { header: 'Comments',
    fields:
     [ 'comments', 'alternativeSpecsSubmitted', 'internalComments' ] },
  { header: 'Aquifer Parameters',
    fields:
     [ 'storativity',
       'transmissivity',
       'hydraulicConductivity',
       'specificYield',
       'specificCapacity',
       'pumpingTestDescription',
       'startDatePumpingTest' ] },
  { header: 'Record maintenance',
    authenticated: true,
    fields: [ 'createUser', 'createDate', 'updateUser', 'updateDate' ] } ]

const reduceSections = (sectionsArray) => {
  return sectionsArray.map(section => section.fields).reduce((a, b) => a.concat(b), [])
}

export default {
  mixins: [filterMixin],
  components: {
    'search-filter': AdvancedSearchFilter
  },
  data () {
    return {
      selectedFilterId: null,
      selectedFilterIds: [],
      defaultFilterSections: [
        { header: 'Search By', fields: ['matchAny', 'well', 'streetOrCity', 'ownerName', 'publicationStatus'] },
        { header: 'Location', fields: ['legal', 'landDistrict'] },
        { header: 'Well Details', fields: ['wellStatus', 'licencedStatus', 'personResponsibleGuid', 'orgResponsibleGuid', 'dateOfWork', 'wellDepth', 'wellDocumentType'] },
        { header: 'Aquifer', fields: ['aquiferNr'] }
      ],
      additionalFilterSections: ADDITIONAL_FILTER_SECTIONS
    }
  },
  computed: {
    ...mapGetters({
      errors: 'searchErrors',
      searchParams: 'searchParams',
      searchInProgress: 'searchInProgress'
    }),
    defaultFilterIds () {
      return reduceSections(this.defaultFilterSections)
    },
    defaultFilterFields () {
      return this.getFilterFields(this.defaultFilterIds)
    },
    additionalFilterIds () {
      return reduceSections(this.additionalFilterSections)
    },
    additionalFilterFields () {
      return this.getFilterFields(this.additionalFilterIds)
    },
    additionalFilterSelectOptions () {
      const selectOptions = this.additionalFilterSections.map(section => {
        const fieldData = this.getFilterFields(section.fields)
        return {
          label: section.header,
          options: fieldData.map(field => {
            return {
              key: field.id,
              value: field.id,
              text: field.label,
              disabled: this.selectedFilterIds.includes(field.id)
            }
          })
        }
      }).filter(optGroup => optGroup.options.length > 0)

      return selectOptions
    },
    selectedAdditionalFilters () {
      return this.getFilterFields(this.selectedFilterIds)
    }
  },
  methods: {
    handleSubmit () {
      this.$store.commit(SET_SEARCH_PARAMS, { ...this.searchQueryParams })

      this.$store.dispatch(SEARCH_WELLS, { trigger: SEARCH_TRIGGER, constrain: true })

      this.$emit('search', this.searchQueryParams)
    },
    handleReset () {
      this.$emit('reset')
    },
    filterParamsReset () {
      const filterParams = { ...this.emptyFilterParams }
      filterParams.matchAny = { match_any: true }
      this.filterParams = filterParams
    },
    initSelectedFilterIds () {
      const activeFields = this.additionalFilterFields.filter((field) => {
        const fieldFilterParams = this.filterParams[field.id]
        return field.params.some(param => param in fieldFilterParams)
      })
      this.selectedFilterIds = activeFields.map(field => field.id)
    },
    addSelectedFilter () {
      if (this.selectedFilterId) {
        this.selectedFilterIds.push(this.selectedFilterId)
      }

      this.selectedFilterId = null
    },
    removeSelectedFilter (filterId) {
      const index = this.selectedFilterIds.indexOf(filterId)
      this.selectedFilterIds.splice(index, 1)
      this.filterParams[filterId] = {}
    },
    initFilterParams () {
      const filterParams = { ...this.emptyFilterParams }

      Object.entries(this.searchParams).forEach(([param, value]) => {
        [...this.defaultFilterFields, ...this.additionalFilterFields].forEach(field => {
          if (field.params.includes(param)) {
            filterParams[field.id] = { [param]: value }
          }
        })
      })

      if (filterParams.matchAny.match_any === undefined) {
        filterParams.matchAny.match_any = true
      }

      this.filterParams = filterParams
    }
  },
  created () {
    this.$store.dispatch(FETCH_CODES)
    this.$store.dispatch(FETCH_DRILLER_NAMES)
    this.$store.dispatch(FETCH_ORGANIZATION_NAMES)

    this.initFilterParams()
    this.initSelectedFilterIds()

    // On reset, clear local params
    this.$store.subscribeAction((action, state) => {
      if (action.type === RESET_WELLS_SEARCH ||
          (action.type === SEARCH_WELLS && state.wellsStore.searchParams.search !== undefined && state.wellsStore.searchParams.search !== null)) {
        this.filterParamsReset()
        this.selectedFilterIds = []
      }
    })
  }
}
</script>

<style>
</style>
