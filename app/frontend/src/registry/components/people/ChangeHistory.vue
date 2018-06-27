<template>
  <div class="card">
    <div class="card-body">
      <h6 class="card-title" id="changeHistoryTitle">Change History
        <span v-if="history && history.length" class="ml-3">
          <b-button link size="sm" variant="outline-primary" @click="showHistory = !showHistory">{{showHistory ? "Hide":"Show"}}</b-button>
        </span></h6>
      <div id="historyList" ref="history">
        <div class="mt-2" v-if="!history || !history.length">
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
                  {{ key | readable }} changed from {{ version.prev[key] }}<span v-if="!version.prev[key]">none</span> to {{ value }}<span v-if="!value">none</span>
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
      showHistory: false
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
      ApiService.history(this.endpoint, this.id).then((response) => {
        this.history = response.data
      })
    }
  },
  filters: {
    readable (val) {
      return val ? val.split('_').map((word) => {
        return word.charAt(0).toUpperCase() + word.substring(1)
      }).join(' ') : ''
    }
  },
  created () {
    this.update()
  }
}
</script>

<style>

</style>
