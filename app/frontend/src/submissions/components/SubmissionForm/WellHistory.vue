<template>
  <div class="card">
    <div class="card-body">
      <h6 class="card-title" id="changeHistoryTitle">Change History
        <span class="ml-3">
          <b-button link size="sm" variant="outline-primary" v-on:click="toggleShow">{{showHistory ? "Hide":"Show"}}</b-button>
        </span></h6>
      <div v-if="loading">
        <div class="loader" style="margin-right: 5px"></div>Loading...
      </div>
      <div id="historyList" ref="history" v-if="loaded && !loading">
        <div class="mt-2" v-if="!history || !history.length">
          <b-row><b-col>No history for this record.</b-col></b-row>
        </div>
        <div class="mt-2" v-if="history && history.length && showHistory">
          <div class="mt-3" v-for="(history_item, index) in history" :key="`history-version ${index}`" :id="`history-version-${index}`">
            <div class="font-weight-bold">
<!--              {{history_item[0].user}}-->
              edited well
<!--              {{history_item[0].action}}-->
<!--              {{history_item[0].type}}-->
              on
<!--              {{history_item[0].date | moment("MMMM Do YYYY [at] LT")}}-->
              <div
                style="margin-left:20px;"
                class="font-weight-light"
                v-for="(item, key) in history_item"
                :key="`history-item-${key}-in-version ${index}`">

                  <div v-if="Array.isArray(item.diff) && item.diff.length > 0 ||
                              Array.isArray(item.prev) && item.prev.length > 0">
                    <div v-for="(dv, d) in item.diff"
                         :key="`history-dv-${d}-in-version ${index}`">
                      <b-table
                        responsive
                        striped
                        small
                        bordered
                        :items="Object.values(dv)"
                        show-empty/>
                    </div>
                    to
                    <div v-for="(pv, p) in item.diff"
                         :key="`history-pv-${p}-in-version ${index}`">
                      <b-table
                        responsive
                        striped
                        small
                        bordered
                        :items="Object.values(pv)"
                        show-empty/>
                    </div>
                  </div>
                  <div v-else>
                    {{ item.type | formatKey }} changed from {{ item.prev | formatValue }} to {{ item.diff | formatValue }}
                  </div>

              </div>
            </div>
          </div>
          <div class="font-weight-bold mt-3">
            {{create_user}}
            Created this well on
            {{create_date | moment("MMMM Do YYYY [at] LT")}}
          </div>
        </div>
        <div v-if="loading">
          <b-row><b-col>Loading history...</b-col></b-row>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import ApiService from '@/common/services/ApiService.js'

export default {
  name: 'WellHistory',
  props: {
    id: {
      type: String,
      isInput: false
    },
    events: {
      type: Vue
    }
  },
  data () {
    return {
      history: [],
      showHistory: false,
      loading: false,
      loaded: false
    }
  },
  watch: {
    id: function () {
      this.update()
    }
  },
  methods: {
    toggleShow () {
      this.showHistory = true
      // if (this.showHistory && !this.loading && !this.loaded) {
        this.update()
      // }
    },
    update () {
      return
      this.loading = true
      ApiService.history('wells', this.id).then((response) => {
        this.history = response.data.diff
        this.create_user = response.data.create_user
        this.create_date = response.data.create_date
        this.loading = false
        this.loaded = true
      }).catch(() => {
        this.loading = false
      })
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
      if (val === 'Geom[0]') {
        return 'Longitude'
      } else if (val === 'Geom[1]') {
        return 'Latitude'
      } else if (val === 'Geom') {
        return 'Longitude, Latitude'
      } else {
        return val
      }
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
    if (this.events) {
      this.events.$on('well-edited', () => {
        this.update()
      })
    }
  }
}
</script>

<style>
  .loader {
    border: 5px solid #f3f3f3;
    border-top: 5px solid #5b7b9c;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    display: inline-block;
    text-align: center;
    vertical-align: middle;
    animation: spin 2s linear infinite;
  }
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>
