/*
    Licensed under the Apache License, Version 2.0 (the "License")
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
  <div v-if="qaqcStore.resultCount > 0 && qaqcStore.resultCount < maxExportSize">
    <h3>Export qaqc results</h3>
    <div class="button-container">
      <ul>
        <li>
          <Button
            label="Excel"
            outlined
            type="download"
            download="search-results.xlsx"
            @click="exportHandler('xlsx')"/>
        </li>
        <li>
          <Button
            label="CSV"
            outlined
            type="download"
            download="search-results.csv"
            @click="exportHandler('csv')"/>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import querystring from 'querystring-es3' // Using ES module compatible version
import ApiService from '@/common/services/ApiService.js'
import { useQAQCStore } from '@/stores/qaqc'
import { MAX_API_RESULT_AND_EXPORT_COUNT } from '@/common/constants'

export default {
  props: {
    fieldData: Object
  },
  data () {
    return {
      maxExportSize: MAX_API_RESULT_AND_EXPORT_COUNT
    }
  },
  computed: {
    qaqcStore () { return useQAQCStore() },
    fullQueryString () {
      const queryParams = {
        ...this.qaqcStore.params,
        ordering: this.qaqcStore.ordering,
        fields: this.exportFields.join(',')
      }
      if (Object.entries(this.qaqcStore.resultFilters).length > 0) {
        queryParams.filter_group = JSON.stringify(this.qaqcStore.resultFilters)
      }

      return querystring.stringify(queryParams)
    },
    exportFields () {
      return this.qaqcStore.resultColumns.filter(id => this.fieldData[id]).map(id => this.fieldData[id].param)
    },
    exportBaseUrl () {
      // Dynamically set the base URL based on the activeTable prop
      switch (this.qaqcStore.selectedTab) {
        case 0: // record compliance
          return `${import.meta.env.VITE_AXIOS_BASE_URL}qaqc/recordcompliance/download`
        case 1: // mislocated wells
          return `${import.meta.env.VITE_AXIOS_BASE_URL}qaqc/mislocatedwells/download`
        case 2: // cross referencing
          return `${import.meta.env.VITE_AXIOS_BASE_URL}qaqc/crossreferencing/download`
        default:
          return `${import.meta.env.VITE_AXIOS_BASE_URL}wells/export` // Default or fallback URL
      }
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
    async exportHandler (format) {
      const exportUrl = this.getExportUrl(format)
      try {
        ApiService.download(exportUrl)
      } catch (error) {
        console.error('There was a problem with the fetch operation:', error)
      }
    }
  }
}
</script>
<style scoped>
  .button-container {
    margin-left: 5px;
    display: flex;
    justify-content: start; /* Aligns items to the start */
    gap: 5px; /* Adjust the gap as needed */
  }
  ul {
    display: flex;
    list-style-type: none;
    padding: 0;
  }
  ul > li:first-child { margin-right: 1em; }
</style>
