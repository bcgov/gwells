<template>
  <div>
    <div class="table-responsive">
      <table class="table table-striped" id="registry-table">
        <thead>
          <th v-for="field in fields"
              :key="field.name"
              :class="field.class"
              v-if="(field.visible === 'public' || user) && (field.activity === activity || field.activity == 'all')">
            {{field.name}} <i class="fa fa-sort" v-if="field.sortable && field.sortCode" @click="sortBy(field.sortCode)"></i>
          </th>
        </thead>
        <tbody>
          <tr v-if="drillers.results && drillers.results.length"
              v-for="(driller, index) in drillers.results"
              :key="driller.person_guid" :id="`registry-table-row-${index}`">
            <td>
              <div><b>{{ driller.first_name }} {{ driller.surname }}</b></div>
              <div v-if="driller.registrations && driller.registrations.length">
                <div
                    v-for="(reg, regIndex) in driller.registrations"
                    v-if="reg.activity === activity"
                    :key="`reg no ${driller.person_guid} ${regIndex}`">
                  {{ reg.registration_no }}</div>
              </div>
            </td>
            <td>
              <div v-if="driller.organization">{{ driller.organization.name }}</div></td>
            <td>
              <div v-if="driller.organization">{{ driller.organization.street_address }}
                <div>
                  <span>{{ driller.organization.city }}</span><span
                    v-if="driller.organization.city && driller.organization.province_state">, </span><span
                      v-if="driller.organization.province_state">{{ driller.organization.province_state }}</span>
                </div>
              </div>
            </td>
            <td>
              <div v-if="driller.contact_tel">Phone: {{ driller.contact_tel }}</div>
              <div v-if="driller.contact_email">Email: {{ driller.contact_email }}</div>
            </td>
            <td v-if="activity === 'DRILL'">
              <div v-if="driller.registrations && driller.registrations.length">
                <div
                    v-for="(reg, regIndex) in driller.registrations"
                    v-if="reg.activity === 'DRILL'"
                    :key="`reg quals ${driller.person_guid} ${regIndex}`">
                  <div
                      v-if="reg.applications && reg.applications.length"
                      v-for="(app, appIndex) in reg.applications"
                      :key="`app quals ${driller.person_guid} ${app.application_guid} ${appIndex}`">
                    <div
                        v-if="app.subactivity &&
                              app.subactivity.qualification_set &&
                              app.subactivity.qualification_set.length"
                        v-for="(qual, qualIndex) in app.subactivity.qualification_set"
                        :key="`qual set ${driller.person_guid} ${app.application_guid} ${qualIndex}`">
                        {{ qual.description }}
                    </div>
                  </div>
                </div>
              </div>
            </td>
            <td></td>
            <td v-if="user && activity === 'DRILL'">{{ driller.status }}</td>
            <td v-if="user">
              <router-link :to="{ name: 'PersonDetail', params: { person_guid: driller.person_guid } }">
                Details
              </router-link>
            </td>
          </tr>
          <tr v-else>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="row">
      <div class="col-xs-12 col-sm-4">
        <span v-if="drillers.results && drillers.results.length">Showing <span id="drillersCurrentOffset">{{ drillers.offset + 1 }}</span> to <span id="drillersCurrentOffsetLimit">{{ drillers.offset + drillers.results.length }}</span> of <span id="drillersTotalResults">{{ drillers.count }}</span></span>
      </div>
      <div v-if="drillers.results && drillers.results.length" class="col-xs-12 col-sm-4 offset-sm-4 offset-md-5 col-md-3">
        <nav aria-label="List navigation" v-if="drillers.results && drillers.results.length">
          <ul class="pagination">
            <li v-if="drillers.previous">
              <button type="button" @click="paginationPrev" class="btn btn-default" aria-label="Previous" id="table-pagination-prev">
                <span aria-hidden="true">Previous</span>
              </button>
            </li>
            <li v-else>
              <button type="button" class="btn btn-default" aria-hidden="true" disabled>
                <span aria-hidden="true">Previous</span>
              </button>
            </li>
            <li v-if="drillers.next">
              <button type="button" @click="paginationNext" class="btn btn-default" aria-label="Next" id="table-pagination-next">
                <span aria-hidden="true">Next</span>
              </button>
            </li>
            <li v-else>
              <button type="button" class="btn btn-default" aria-hidden="true" disabled>
                <span aria-hidden="true">Next</span>
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { FETCH_DRILLER_LIST } from '@/registry/store/actions.types'
const querystring = require('querystring')

export default {
  name: 'RegisterTable',
  props: ['activity'],
  data () {
    return {
      // fields for the table headings
      // visible denotes whether field should be visible to public or admin only
      // activity denotes what fields should be displayed for what activity (driller, installer etc.)
      // activity: 'all' is displayed for all activities
      fields: [
        {
          name: 'Name',
          sortCode: 'surname',
          class: 'col-xs-1',
          visible: 'public',
          sortable: true,
          activity: 'all'
        },
        {
          name: 'Company Name',
          sortCode: 'companies__org__name',
          class: 'col-xs-1',
          visible: 'public',
          sortable: true,
          activity: 'all'
        },
        {
          name: 'Company Address',
          class: 'col-xs-1',
          visible: 'public',
          sortable: false,
          activity: 'all'
        },
        {
          name: 'Contact Information',
          class: 'col-xs-1',
          visible: 'public',
          sortable: false,
          activity: 'all'
        },
        {
          name: 'Class of Driller',
          class: 'col-xs-1',
          visible: 'public',
          sortable: true,
          activity: 'DRILL'
        },
        {
          name: 'Certificate Issued By',
          class: 'col-xs-1',
          visible: 'public',
          sortable: true,
          sortCode: 'issuing_org',
          activity: 'all'
        },
        {
          name: 'Registration Status',
          class: 'col-xs-1',
          visible: 'admin',
          sortable: false,
          activity: 'DRILL'
        },
        {
          name: 'Action',
          class: 'col-xs-1',
          visible: 'admin',
          sortable: false,
          activity: 'all'
        }
      ]
    }
  },
  computed: {
    ...mapGetters([
      'loading',
      'listError',
      'user',
      'drillers'
    ])
  },
  methods: {
    paginationNext () {
      // API provides 'next' and 'previous' links with query strings for the current search
      if (this.drillers.next && ~this.drillers.next.indexOf('?')) {
        const q = this.drillers.next.split('?')[1]
        this.$store.dispatch(FETCH_DRILLER_LIST, querystring.parse(q))
      }
    },
    paginationPrev () {
      if (this.drillers.previous && ~this.drillers.previous.indexOf('?')) {
        const q = this.drillers.previous.split('?')[1]
        this.$store.dispatch(FETCH_DRILLER_LIST, querystring.parse(q))
      }
    },
    sortBy (sortCode) {
      this.$emit('sort', sortCode)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

</style>
