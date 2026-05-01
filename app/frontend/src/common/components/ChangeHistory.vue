<template>
  <div class="flex items-center justify-between mb-2">
    <h6 class="text-sm font-semibold" id="changeHistoryTitle">Change History</h6>
    <Button size="small" variant="outlined" :label="showHistory ? 'Hide' : 'Show'" @click="toggleHistory"/>
  </div>

  <div id="historyList">
    <div v-if="loading" class="text-sm text-gray-500">
      Loading history...
    </div>
    <div v-else>
      <div class="mt-2" v-if="showHistory && (!history || !history.length)">
        No history for this record.
      </div>
      <div class="mt-2" v-if="history && history.length && showHistory">
        <div class="mt-3" v-for="(version, index) in history" :key="`history-version ${index}`" :id="`history-version-${index}`">

          <div class="text-sm">
            <span class="font-semibold">{{ version.user }}</span>
                  {{ version.created ? "created" : "edited" }}
                  {{ version.name ? version.name : 'record' }}
                  ({{ moment(version.date, "MMMM Do YYYY [at] LT") }}){{ version.created ? "." : ":" }}
          </div>
          <div class="ml-4">
                  <!-- compare current value to prev value, ignoring insignificant type changes (null to empty string) -->
                  <div
                      v-for="(value, key) in version.diff"
                      v-if="!(value === '' && version.prev[key] === null)"
                      :key="`history-item-${key}-in-version ${index}`">
                    <div v-if="isTable(value)" class="mt-2">
                <div>
                  <span class="font-medium">
                    {{ readable(formatKey(key)) }} changed to:
                  </span>
                </div>
                <div v-if="value != null && value.length > 0">
                  <DataTable
                    :value="value"
                    responsiveLayout="scroll"
                    size="small"
                    stripedRows
                    class="border"
                  >
                    <Column
                      v-for="(col, i) in Object.keys(value[0])"
                      :key="i"
                      :field="col"
                      :header="readable(col)"
                    />
                  </DataTable>
                </div>
                <div v-else>
                  None
                </div>
                <div class="mt-2">
                  From:
                  <div v-if="version.prev[key] != null && version.prev[key].length > 0">
                    <DataTable
                      :value="version.prev[key]"
                      responsiveLayout="scroll"
                      size="small"
                      stripedRows
                      class="border mt-1"
                    >
                      <Column
                        v-for="(col, i) in Object.keys(version.prev[key][0])"
                        :key="i"
                        :field="col"
                        :header="readable(col)"
                      />
                    </DataTable>
                  </div>
                  <div v-else class="text-gray-500">None</div>
                </div>
              </div>
              <div v-else>
                {{ readable(key) }} changed from {{ formatValue(booleanToYesNo(version.prev[key])) }} to {{ formatValue(booleanToYesNo(value)) }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import moment from 'moment';

export default {
  name: 'ChangeHistory',

  /**
   * This component accepts props 'resource' and 'id'.
   * resource: the name of the API/DB resource that the record belongs to e.g. "organization", "person"
   * id: the record id to request history for
   */
  props: ['resource', 'id'],
  data () {
    return {
      history: [],
      showHistory: false,
      loading: false
    }
  },
  computed: {
    endpoint () {
      // convert resource name into api endpoint
      const endpointMap = {
        organization: 'organizations',
        person: 'drillers'
      }
      return endpointMap[this.resource] || this.resource
    }
  },
  watch: {
    id: function () {
      this.update()
    }
  },
  methods: {
    moment,
    update () {
      if (!this.showHistory) { return }

      this.loading = true
      ApiService.history(this.endpoint, this.id).then((response) => {
        this.history = response.data
        this.loading = false
      }).catch(() => {
        this.loading = false
      })
    },
    toggleHistory () {
      this.showHistory = !this.showHistory

      if (this.showHistory) {
        this.update()
      }
    },
    isTable (arr) {
      return Array.isArray(arr) && arr.length > 0
    },
    readable (val) {
      val = val || ''

      // some GIS data is returned in field 'geom' by default.
      // for the history view, we can translate that to 'Location'
      if (val.toLowerCase() === 'geom') {
        return 'Location'
      }

      return val.split('_').map((word) => {
        return word.charAt(0).toUpperCase() + word.substring(1)
      }).join(' ')
    },
    formatKey (val) {
      return val
    },
    formatValue (val) {
      // takes a single value and returns a string in a human readable format.
      // if val started as something that would be displayed as an empty space,
      // we return 'none' instead so we can form a complete sentence.
      // e.g. Province changed from none to British Columbia
      if (val === undefined || val === null || val === '') {
        return 'none'
      }
      return val
    }
  },
  created () {
    this.update()
  }
}
</script>

<style>

</style>
