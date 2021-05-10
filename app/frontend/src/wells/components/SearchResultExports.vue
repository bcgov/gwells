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
  <div v-if="resultCount > 0 && resultCount < maxExportSize">
    <h3>Export search results</h3>
    <div>
      <ul>
        <li>
          <a :href="excelExportUrl" download="search-results.xlsx" @click="handleExportClickEvent('Excel')">Excel</a>
        </li>
        <li>
          <a :href="csvExportUrl" download="search-results.csv" @click="handleExportClickEvent('CSV')">CSV</a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import querystring from 'querystring'

import { mapGetters } from 'vuex'
import { MAX_API_RESULT_AND_EXPORT_COUNT } from '@/common/constants'

export default {
  props: {
    fieldData: Object
  },
  data () {
    return {
      exportBaseUrl: `${process.env.VUE_APP_AXIOS_BASE_URL}wells/export`,
      maxExportSize: MAX_API_RESULT_AND_EXPORT_COUNT
    }
  },
  computed: {
    ...mapGetters({
      bounds: 'searchBounds',
      constrain: 'constrainSearch',
      params: 'searchParams',
      ordering: 'searchOrdering',
      resultFilters: 'searchResultFilters',
      resultCount: 'searchResultCount',
      resultColumns: 'searchResultColumns'
    }),
    exportFields () {
      return this.resultColumns.filter(id => this.fieldData[id]).map(id => this.fieldData[id].param)
    },
    fullQueryString () {
      const queryParams = {
        ...this.params,
        ordering: this.ordering,
        fields: this.exportFields.join(',')
      }
      if (Object.entries(this.resultFilters).length > 0) {
        queryParams.filter_group = JSON.stringify(this.resultFilters)
      }
      if (this.constrain) {
        Object.assign(queryParams, this.bounds)
      }

      return querystring.stringify(queryParams)
    },
    excelExportUrl () {
      return this.getExportUrl('xlsx')
    },
    csvExportUrl () {
      return this.getExportUrl('csv')
    }
  },
  methods: {
    getExportUrl (format) {
      let url = `${this.exportBaseUrl}?format=${format}`
      if (this.fullQueryString) {
        url = `${url}&${this.fullQueryString}`
      }

      return url
    },
    handleExportClickEvent (format) {
      if (window.ga) {
        window.ga('send', {
          hitType: 'event',
          eventCategory: 'Button',
          eventAction: 'WellSearchResultsExtract',
          eventLabel: format
        })
      }
    }
  }
}
</script>

<style lang="scss">
</style>
