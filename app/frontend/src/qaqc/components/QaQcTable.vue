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
  <div id="qaqcResults">
    <b-col sm="4"></b-col>
    <b-row align-h="between" class="mb-2">
      <b-col sm="4">
        <!-- Date Range Filter specifically for createDate -->
        <div><b>Created Date Range</b></div>
        <div :class="`qaqc-filters-${dateColumn.type}`">
          <qaqc-filters
            v-if="dateColumn"
            :type="dateColumn.type"
            :id="`${dateColumn.id}ResultFilter`"
            :errors="resultErrors[dateColumn.param]"
            :param-names="dateColumn.params"
            :options="dateColumn.options || filterSelectOptions[dateColumn.id]"
            :value="filterParams[dateColumn.id]"
            :text-field="dateColumn.textField"
            @input="applyFilter(dateColumn, $event)" />
        </div>
      </b-col>
      <b-col sm="4" class="form-inline">
        Show <b-form-select class="mx-1" :value="limit" @input="setLimit($event)" :options="limitOptions" /> results
      </b-col>
    </b-row>
    <div class="table-responsive">
      <table id="qaqcTable" class="table table-striped" aria-describedby="qaqcTableDesc">
        <thead>
          <tr>
            <th
              v-for="column in columns"
              :key="column.id"
              class="text-nowrap"
              scope="col">
              {{ columnLabels(column.id) }}
              <b-button
                v-if="column.sortParam !== 'latitude' && column.sortParam !== 'longitude'"
                class="sort-button px-0"
                :class="{active: column.sortParam === orderingParam}"
                variant="link"
                @click="sortResults({ param: column.sortParam || column.sortParam, desc: (column.sortParam === orderingParam) ? !orderingDesc : false })">
                {{ (column.sortParam === orderingParam) ? orderingDesc ? '&#x2191;' : '&#x2193;' : '&#x2195;' }}
              </b-button>
              <div 
                v-if="column.sortParam === 'latitude' || column.sortParam === 'longitude'"
                class="py-1 px-0"
              ></div>
              <!-- Only show the badge and popover if there is tooltip content -->
              <template v-if="getTooltipContent(column.id)">
                <b-badge pill variant="primary" :id="`${column.id}-tooltip`" tabindex="0" class="ml-1">
                  <i class="fa fa-question fa-sm"></i>
                </b-badge>
                <b-popover :target="`${column.id}-tooltip`" placement="bottom" triggers="hover focus" :content="getTooltipContent(column.id)"></b-popover>
              </template>
            </th>
          </tr>
          <tr class="filters">
            <th v-for="column in columns" :key="column.id" :class="`qaqc-filters-${column.type}`" scope="col">
              <qaqc-filters
                v-if="!excludedFilterColumns.includes(column.id)"
                :type="column.type"
                :id="`${column.id}ResultFilter`"
                :errors="resultErrors[column.param]"
                :param-names="column.params"
                :options="column.options || filterSelectOptions[column.id]"
                :value-field="column.valueField"
                :text-field="column.textField"
                :value="filterParams[column.id]"
                @input="applyFilter(column, $event)" />
            </th>
          </tr>
        </thead>
        <tbody role="rowgroup" v-if="(isBusy || isEmpty || isReset)">
          <tr :class="{loading: isBusy}">
            <td :colspan="columnCount">
              <div class="position-relative my-1 mx-1">
                <div v-if="isBusy" class="d-flex">
                  <div class="spinner-border m-3" role="status" aria-hidden="true"></div>
                  <strong class="align-middle my-3 pt-1">
                    Loading...
                  </strong>
                </div>
                <strong v-else-if="hasResultErrors" class="text-danger align-middle my-3 pt-1">
                  An error occurred processing the search.
                </strong>
                <strong v-else-if="isReset" class="align-middle my-3 pt-1">
                  Enter some criteria in the form above to search.
                </strong>
                <strong v-else-if="isEmpty" class="align-middle my-3 pt-1">
                  No results matched your search criteria.
                </strong>
              </div>
            </td>
          </tr>
        </tbody>
        <tbody role="rowgroup" v-else>
          <tr v-for="row in results" :key="row.well_tag_number" @mousedown="searchResultsRowClicked(row)">
            <td v-for="column in columns" :key="column.id" class="data">
              <template v-if="column.param === 'well_tag_number'">
                <a :href="safeUrl(row.well_tag_number)" @click.prevent="openInNewTab(row.well_tag_number)">{{ row.well_tag_number }}</a>
              </template>
              <template v-else-if="column.param === 'natural_resource_region'">
                {{ removeRegionSuffix(row[column.param]) }}
              </template>
              <template v-else-if="column.param === 'street_address'">
                {{ row | streetAddressFormat }}
              </template>
              <template v-else-if="column.type === 'select' && Array.isArray(row[column.param])">
                <template v-for="(value, index) in row[column.param]">
                  <span :key="`${row.well_tag_number}-${column.param}-${index}`">
                    {{ value | selectOptionFormat(column, filterSelectOptions[column.id]) }}<span v-if="index < row[column.param].length - 1">, </span>
                  </span>
                </template>
              </template>
              <template v-else-if="column.type === 'select' || column.type === 'radio'">
                {{ row[column.param] | selectOptionFormat(column, filterSelectOptions[column.id]) }}
              </template>
              <template v-else-if="column.param === 'legal_pid'">
                {{ row[column.param] }}
              </template>
              <template v-else>
                {{ row[column.param] | defaultFormat }}
              </template>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="my-3" v-if="resultCount > 0">
      <div>Showing {{ currentRecordsCountStart }} to {{ currentRecordsCountEnd }} of {{ resultCount }} {{ resultCount === 1 ? 'record' : 'records'}}.</div>
      <qaqc-exports class="my-3" :field-data="searchFields" />
    </div>
    <b-pagination
      class="mt-3"
      size="md"
      :disabled="isBusy"
      :total-rows="resultCount"
      :value="currentPage"
      :per-page="limit"
      @input="changePage($event)"/>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { QAQC_SEARCH } from '@/qaqc/store/actions.types.js'
import {
  SET_QAQC_LIMIT,
  SET_QAQC_OFFSET,
  SET_QAQC_ORDERING,
  SET_QAQC_RESULT_FILTERS
} from '@/qaqc/store/mutations.types.js'
import { FILTER_TRIGGER } from '@/qaqc/store/triggers.types.js'
import QaQcFilters from '@/qaqc/components/QaQcFilters.vue'
import QaQcExports from '@/qaqc/components/QaQcExports.vue'
import filterMixin from '@/wells/components/mixins/filters.js'
import { sanitizeUrl } from '@braintree/sanitize-url'

export default {
  mixins: [filterMixin],
  components: {
    'qaqc-filters': QaQcFilters,
    'qaqc-exports': QaQcExports
  },
  data () {
    return {
      limitOptions: [
        { value: 10, text: '10' },
        { value: 25, text: '25' },
        { value: 50, text: '50' }
      ],
      // Object mapping column IDs to tooltip content
      tooltipContent: {
        'diameterNull': 'Diameter in the last line of the Casing Details table on the Well Summary page. It is used to check if the casing information is missing',
        'aquiferLithologyNull': 'Raw Data in the last line of the Lithology table on the Well Summary page; It is used to check if lithology information is missing',
        'wellActivityType': 'Activity in the Well Activity table on the Well Summary page',
        'workStartDateNull': 'Work Start Date in the Well Activity Table on the Well Summary page',
        'workEndDateNull': 'Work End Date in the Well Activity Table on the Well Summary page',
        'createDate': 'When the well record was entered/created in UTC time',
        'geocodeDistance': 'The distance from well to location determined by the BC Address Geocoder API.',
        'distanceToPid': 'The distance from well to BC Parcel Fabric Polygon with matching Parcel Identifier (PID). A higher value indicates higher probability of a location error. NULL indicates no matching PID found.',
        'scoreAddress': 'Token Set Ratio score for matching wells address to reverse geocoded address (street number/name/direction). A lower score indicates a higher probability of a location error.',
        'scoreCity': 'Token Set Ratio score for matching wells city to reverse geocoded locality. A lower score indicates a higher probability of a location error.'
      }
    }
  },
  computed: {
    ...mapGetters({
      limit: 'qaqcLimit',
      errors: 'qaqcErrors',
      params: 'qaqcParams',
      offset: 'qaqcOffset',
      ordering: 'qaqcOrdering',
      pending: 'qaqcPendingSearch',
      resultFilters: 'qaqcResultFilters',
      resultColumns: 'qaqcResultColumns',
      resultCount: 'qaqcResultCount',
      results: 'qaqcResults'
      // selectedWells: 'selectedWells'
    }),
    currentPage () {
      return Math.ceil(this.offset / this.limit) + 1
    },
    dateColumn () {
      return this.columns.find(column => column.param === 'create_date')
    },
    columns () {
      return this.getFilterFields(this.resultColumns)
    },
    excludedFilterColumns () {
      return ['latitude', 'longitude']
    },
    // currentRecordsCountEnd is the last visible record number in the table of wells
    // (e.g. the 10 in 'showing 1 to 10 of 25 records')
    currentRecordsCountEnd () {
      if (this.results === null) {
        return 0
      }
      return (this.currentPage - 1) * this.limit + this.results.length
    },
    // currentRecordsCountStart is the starting record number in the table of wells
    // (e.g. the 1 in 'showing 1 to 10 of 25 records')
    currentRecordsCountStart () {
      return (this.currentPage - 1) * this.limit + 1
    },
    columnLabels () {
      // Define a mapping for updated labels
      const labelMapping = {
        'wellTagNumber': 'WTN',
        'identificationPlateNumber': 'WIDP',
        'wellClass': 'Class of well',
        'wellSubclass': 'Well subclass',
        'latitudeNull': 'Lat',
        'longitudeNull': 'Lon',
        'finishedWellDepthNull': 'Finished well depth (feet)',
        'diameterNull': 'Casing Diameter (inches)',
        'surfaceSealDepthNull': 'Seal Depth (feet)',
        'surfaceSealThicknessNull': 'Seal Thickness (inches)',
        'aquiferLithologyNull': 'Lithology',
        'wellActivityType': 'Work/Report Type',
        'workStartDateNull': 'Work Start Date',
        'workEndDateNull': 'Work End Date',
        'personResponsible': 'Person Responsible',
        'orgResponsible': 'Company that did the work',
        'naturalResourceRegion': 'Natural Resource Region',
        'createDate': 'Created Date',
        'createUser': 'Created By',
        'updateDate': 'Updated Date',
        'updateUser': 'Updated By',
        'crossReferencedBy': 'X-ref\' By',
        'crossReferencedDate': 'X-ref\' Date',
        'internalOfficeComments': 'Internal Office Comments',
        'internalComments': 'Internal Comments',
        'comments': 'Comments',
        'geocodeDistance': 'Geocode Distance',
        'distanceToPid': 'Distance to Matching PID',
        'scoreAddress': 'Score Address',
        'scoreCity': 'Score City'
      }
      return (columnId) => labelMapping[columnId] || columnId
    },
    orderingParam () {
      if (this.orderingDesc) {
        return this.ordering.substr(1)
      } else {
        return this.ordering
      }
    },
    columnCount () {
      return this.resultColumns.length
    },
    orderingDesc () {
      return this.ordering.startsWith('-')
    },
    hasResultErrors () {
      return Object.entries(this.resultErrors).length > 0
    },
    resultErrors () {
      return this.errors.filter_group || {}
    },
    isReset () {
      return (!this.isBusy && this.results === null)
    },
    isEmpty () {
      return (!this.isBusy && this.results !== null && this.resultCount === 0)
    },
    isBusy () {
      return (this.pending !== null)
    }
  },
  methods: {
    setLimit (limit) {
      this.$store.commit(SET_QAQC_LIMIT, limit)
      this.$emit('limit-changed', limit)

      this.$store.dispatch(QAQC_SEARCH, { trigger: FILTER_TRIGGER })
    },
    changePage (page) {
      const offset = this.limit * (page - 1)
      this.$store.commit(SET_QAQC_OFFSET, offset)
      this.$emit('page-changed', page)

      this.$store.dispatch(QAQC_SEARCH, { trigger: FILTER_TRIGGER })
    },
    sortResults ({ param, desc }) {
      const sort = `${desc ? '-' : ''}${param}`
      this.$store.commit(SET_QAQC_ORDERING, sort)
      this.$emit('sort-changed', sort)

      this.$store.dispatch(QAQC_SEARCH, { trigger: FILTER_TRIGGER })
    },
    applyFilter ({ id }, values) {
      this.filterParams[id] = values
      const filterGroup = { ...this.searchQueryParams }
      this.$store.commit(SET_QAQC_RESULT_FILTERS, filterGroup)
      this.$emit('filter-changed', filterGroup)

      this.$store.dispatch(QAQC_SEARCH, { trigger: FILTER_TRIGGER })
    },
    initFilterParams () {
      const filterParams = { ...this.emptyFilterParams }

      Object.entries(this.resultFilters).forEach(([param, value]) => {
        this.columns.forEach(column => {
          if (column.params.includes(param)) {
            filterParams[column.id] = { [param]: value }
          }
        })
      })

      this.filterParams = filterParams
    },
    searchResultsRowClicked (data) {
      this.$emit('rowClicked', data)
    },
    getTooltipContent(columnId) {
      // Return the tooltip content if it exists, or null if it doesn't
      return this.tooltipContent[columnId] || null;
    },
    removeRegionSuffix(value) {
      if (!value || typeof value !== 'string') return '';
      // Define the suffixes to check for and remove, ordered by specificity and length
      const suffixes = [' Natural Resource Region', ' Region', ' region'];
      // Check each suffix to see if the value ends with it
      for (const suffix of suffixes) {
        if (value.endsWith(suffix)) {
          // If value ends with suffix, remove it and return
          return value.substring(0, value.length - suffix.length);
        }
      }
      // If no suffix matches, return the original value
      return value;
    },
    openInNewTab(wellTagNumber) {
      const path = sanitizeUrl(`/well/${wellTagNumber}`)
      const { href } = this.$router.resolve(path);
      window.open(href, '_blank');
    },
    safeUrl(wellTagNumber) {
      const url = sanitizeUrl(`/gwells/well/${wellTagNumber}`)
      return encodeURI(url)
    }
  },
  filters: {
    selectOptionFormat (value, column, options = null) {
      if (value === undefined || value === null || value === '') {
        return ''
      }

      const valueProp = column.valueField || 'value'
      const textProp = column.textField || 'text'
      const selectOptions = column.options || options
      const optionsMatch = selectOptions.find(option => option[valueProp] === value.toString())
      if (optionsMatch) {
        return optionsMatch[textProp]
      }

      return value
    },
    defaultFormat: (value) => {
      if (value === null) {
        return ''
      }
      return value
    },
    streetAddressFormat (row) {
      if (row.city !== undefined && row.city !== null && row.city.toString().trim() !== '') {
        return `${row.street_address}, ${row.city}`
      } else {
        return row.street_address
      }
    }
  },
  watch: {
    resultFilters (newFilters) {
      // on reset (empty filters), clear state
      if (Object.entries(newFilters).length === 0 && newFilters.constructor === Object) {
        this.clearFilterParams()
      }
    },
    resultColumns (newColumns, oldColumns) {
      const removedColumnIds = oldColumns.filter(colId => !newColumns.includes(colId))
      const removedWithFilters = removedColumnIds.filter(columnId => {
        return this.filterParams[columnId] !== undefined && Object.entries(this.filterParams[columnId]).length > 0
      })
      if (removedWithFilters.length > 1) {
        removedWithFilters.forEach(columnId => {
          this.filterParams[columnId] = {}
        })
      }
      if (removedWithFilters.length > 0) {
        const lastFilterRemoved = removedWithFilters.slice(-1)[0]
        // Call applyFilter to trigger reload
        this.applyFilter({ id: lastFilterRemoved }, {})
      }
    }
  },
  created () {
    this.initFilterParams()
  }
}
</script>

<style lang="scss">

#qaqcTable {
  min-height: 36rem;

  td.data {
    white-space: nowrap;
    overflow-wrap: break-word;
  }

 .sort-button {
    opacity: 0.4;

    &:hover,
    &:active,
    &:visited,
    &:focus {
      text-decoration: none;
    }
  }

  .sort-button.active {
    opacity: 1;
  }
}

/* Sticky first column for headers and cells */
#qaqcTable th:first-child, #qaqcTable td:first-child {
  position: sticky;
  left: 0;
  background-color: white;
  z-index: 2; /* Higher than the z-index for the sticky headers */
}

/* Sticky headers */
#qaqcTable thead {
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 3; /* Ensures the header is above tbody content */
}

.table-responsive {
  /* Ensure the container allows the sticky positioning to work */
  overflow-y: auto;
  height: 400px;
}

td.data {
  max-width: 200px;
  max-height: 100px;
  overflow: auto; // Introduces a scrollbar when the content overflows
  word-wrap: break-word; // Ensures that long words can break and wrap to the next line
  white-space: normal; // Overrides the existing nowrap to allow text wrapping
}

/* Spinner styles — these can be removed when moving to bootstrap 4.3 */

$spinner-width:         2rem !default;
$spinner-height:        $spinner-width !default;
$spinner-border-width:  .25em !default;

$spinner-width-sm:        1rem !default;
$spinner-height-sm:       $spinner-width-sm !default;
$spinner-border-width-sm: .2em !default;

@keyframes spinner-border {
  to { transform: rotate(360deg); }
}

.spinner-border {
  display: inline-block;
  width: $spinner-width;
  height: $spinner-height;
  vertical-align: text-bottom;
  border: $spinner-border-width solid currentColor;
  border-right-color: transparent;
  // stylelint-disable-next-line property-blacklist
  border-radius: 50%;
  animation: spinner-border .75s linear infinite;
}

.spinner-border-sm {
  width: $spinner-width-sm;
  height: $spinner-height-sm;
  border-width: $spinner-border-width-sm;
}
</style>
