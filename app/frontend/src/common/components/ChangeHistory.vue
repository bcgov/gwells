<template>
  <div class="card">
    <div class="card-body">
      <h6 class="card-title mb-0" id="changeHistoryTitle">Change History
        <span class="ml-3">
          <b-button link size="sm" variant="outline-primary" @click="toggleHistory">{{showHistory ? "Hide":"Show"}}</b-button>
        </span>
      </h6>
      <div id="historyList">
        <div v-if="!loading">
          <div class="mt-2" v-if="showHistory && (!history || !history.length)">
            <b-row><b-col>No history for this record.</b-col></b-row>
          </div>
          <div class="mt-2" v-if="history && history.length && showHistory">
            <div class="mt-3" v-for="(version, index) in history" :key="`history-version ${index}`" :id="`history-version-${index}`">
                <span class="font-weight-bold">{{ version.user }}</span>
                  {{ version.created ? "created" : "edited" }}
                  {{ version.name ? version.name : 'record' }}
                  ({{ version.date | moment("MMMM Do YYYY [at] LT") }}){{ version.created ? "." : ":" }}
                <div class="ml-4">
                  <!-- compare current value to prev value, ignoring insignificant type changes (null to empty string) -->
                  <div
                      v-for="(value, key) in version.diff"
                      v-if="!(value === '' && version.prev[key] === null)"
                      :key="`history-item-${key}-in-version ${index}`">
                    <div v-if="isTable(value)" class="mt-2">
                      {{ key | formatKey | readable }} changed to:
                      <div v-if="value != null && value.length > 0">
                        <b-table
                          responsive
                          striped
                          small
                          fixed
                          bordered
                          :items="value"/>
                      </div>
                      <div v-else>
                        None
                      </div>
                      <div style="margin-bottom:10px;">
                        From:
                        <div v-if="version.prev[key] != null && version.prev[key].length > 0">
                          <b-table
                            responsive
                            striped
                            small
                            fixed
                            bordered
                            :items="version.prev[key]"/>
                        </div>
                        <div v-else>
                          None
                        </div>
                      </div>
                    </div>
                    <div v-else>
                      {{ key | readable }} changed from {{ version.prev[key] | booleanToYesNo | formatValue }} to {{ value | booleanToYesNo | formatValue }}
                    </div>
                  </div>
                </div>
            </div>
          </div>
        </div>
        <div v-else>
          Loading history...
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
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
    }
  },
  filters: {
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
