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
  <div v-if="resultCount > 0 && resultCount < maxExportSize">
    <h3>Export qaqc results</h3>
    <div class="button-container">
      <a @click="handleExportClickEvent('xlsx')" class="qaqc-download-button">Excel</a>
      <a @click="handleExportClickEvent('csv')" class="qaqc-download-button">CSV</a>
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
      maxExportSize: MAX_API_RESULT_AND_EXPORT_COUNT
    }
  },
  computed: {
    ...mapGetters({
      bounds: 'qaqcBounds',
      params: 'qaqcParams',
      ordering: 'qaqcOrdering',
      resultFilters: 'qaqcResultFilters',
      resultCount: 'qaqcResultCount',
      resultColumns: 'qaqcResultColumns',
      selectedTab: 'qaqcSelectedTab'
    }),
    fullQueryString () {
      const queryParams = {
        ...this.params,
        ordering: this.ordering,
        fields: this.exportFields.join(',')
      }
      if (Object.entries(this.resultFilters).length > 0) {
        queryParams.filter_group = JSON.stringify(this.resultFilters)
      }

      return querystring.stringify(queryParams)
    },
    exportFields () {
      return this.resultColumns.filter(id => this.fieldData[id]).map(id => this.fieldData[id].param)
    },
    csvExportUrl () {
      return this.getExportUrl('csv')
    },
    excelExportUrl () {
      return this.getExportUrl('xlsx')
    },
    exportBaseUrl() {
      // Dynamically set the base URL based on the activeTable prop
      switch (this.selectedTab) {
        case 0: // record compliance
          return `${process.env.VUE_APP_AXIOS_BASE_URL}qaqc/recordcompliance/download`;
        case 1: // mislocated wells
          return `${process.env.VUE_APP_AXIOS_BASE_URL}qaqc/mislocatedwells/download`;
        case 2: // cross referencing
          return `${process.env.VUE_APP_AXIOS_BASE_URL}qaqc/crossreferencing/download`;
        default:
          return `${process.env.VUE_APP_AXIOS_BASE_URL}wells/export`; // Default or fallback URL
      }
  },
  },
  methods: {
    getExportUrl(format) {
      let url = `${this.exportBaseUrl}?format=${format}`;
      if (this.fullQueryString) {
        url = `${url}&${this.fullQueryString}`;
      }
      return url;
    },
    async handleExportClickEvent(format) {

      // Generate the URL for the file download
      const url = this.getExportUrl(format);
      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.blob();

        const downloadUrl = window.URL.createObjectURL(data);

        const link = document.createElement('a');
        link.href = downloadUrl;
        link.setAttribute('download', `search-results.${format}`);
        document.body.appendChild(link);
        link.click();
        link.remove();

      } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
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
.qaqc-download-button {
  padding: 5px 10px;
  width: 60px;
  background-color: transparent; /* Transparent background */
  color: grey; /* Text color */
  text-align: center;
  text-decoration: none;
  display: inline-block;
  border-radius: 5px;
  border: 1px solid grey; /* Border properties */
  cursor: pointer;
  transition: background-color 0.3s; /* Smooth transition for the hover effect */
}

.qaqc-download-button:hover {
  background-color: rgba(0, 0, 0, 0.1); /* Slight grey overlay on hover */
}

.qaqc-download-button:active {
  background-color: rgba(0, 0, 0, 0.2); /* Darker overlay when clicked */
}
</style>
