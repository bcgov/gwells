<template>
  <div class="card">
    <div class="card-body">
      <h6 class="card-title mb-0" id="changeHistoryTitle">
        Change History
        <span class="ml-3">
          <b-button link size="sm" variant="outline-primary" v-on:click="toggleShow">{{showHistory ? "Hide":"Show"}}</b-button>
        </span>
      </h6>
      <div v-if="loading">
        <div class="loader" style="margin-right: 5px"></div>Loading...
      </div>
      <div id="historyList" ref="history" v-if="loaded && !loading">
        <div class="mt-2" v-if="displayHistory">
          <div class="mt-3" v-for="(history_item, index) in cleanHistory" :key="`history-version ${index}`" :id="`history-version-${index}`">
            <div class="font-weight-bold">
              {{history_item[0].user}}
              Edited this Well on
              <time :datetime="history_item[0].date">
                {{history_item[0].date | moment("MMMM Do YYYY [at] LT")}}
              </time>
              <div
                style="margin-left:20px; width: 75%;"
                class="font-weight-light"
                v-for="(item, key) in history_item"
                :key="`history-item-${key}-in-version ${index}`">
                <div v-if="isTable(item)" class="mt-2">
                  {{ item.type | formatKey | readable }} changed to:
                  <div v-if="item.diff != null && item.diff.length > 0">
                    <b-table
                      responsive
                      striped
                      small
                      fixed
                      bordered
                      :items="item.diff"/>
                  </div>
                  <div v-else>
                    None
                  </div>
                  <div style="margin-bottom:10px;">
                    From:
                    <div v-if="item.prev != null && item.prev.length > 0">
                      <b-table
                        responsive
                        striped
                        small
                        fixed
                        bordered
                        :items="item.prev"/>
                    </div>
                    <div v-else>
                      None
                    </div>
                  </div>
                </div>
                <div class="mt-2" v-else>
                  {{ item.type | formatKey | readable }}
                  {{ item.action == 'Added' ? 'set' : 'changed'}} to {{ item.diff | booleanToYesNo | formatValue }}
                  <span v-if="item.action != 'Added'">from {{ item.prev | booleanToYesNo | formatValue }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="font-weight-bold mt-3" v-if="showHistory">
          {{create_user}}
          created this well on
          {{create_date | moment("MMMM Do YYYY [at] LT")}}
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
    wellTagNumber: {
      type: Number,
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
  computed: {
    displayHistory () {
      return this.history.length > 0 && this.showHistory
    },
    cleanHistory () {
      // Drop the last history item as it is the initial construction submission or legacy record.
      // If it is kept in the list of history items then the user will see a lot of repeating "x
      // changed from none". It is a given that the history starts at something - not from nothing.
      return this.history.slice(0, -1)
    }
  },
  methods: {
    toggleShow (e) {
      this.showHistory = !this.showHistory
      if (this.showHistory && !this.loading && (!this.loaded || e.ctrlKey)) {
        this.update()
      }
    },
    update () {
      this.loading = true
      ApiService.history('wells', this.wellTagNumber).then((response) => {
        this.history = response.data.history || []
        this.create_user = response.data.create_user
        this.create_date = response.data.create_date
        this.loading = false
        this.loaded = true
      }).catch(() => {
        this.loading = false
      })
    },
    isTable ({ diff, prev }) {
      return (Array.isArray(diff) && diff.length > 0) || (Array.isArray(prev) && prev.length > 0)
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
        if (this.showHistory) {
          this.update()
        }
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
