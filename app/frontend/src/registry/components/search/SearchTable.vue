<template>
  <div>
    <div class="table-responsive">
      <table class="table table-striped" id="registry-table">
        <thead>
          <th v-for="field in fields"
              :key="field.name"
              :class="field.class"
              v-if="(field.visible === 'public' || userRoles.registry.view) && (field.activity === activity || field.activity == 'all')">
            {{field.name}} <i class="fa fa-sort" v-if="field.sortable && field.sortCode" @click="sortBy(field.sortCode)"></i>
          </th>
        </thead>
        <tbody>
          <tr v-if="drillers.results && drillers.results.length"
              v-for="(driller, index) in drillers.results"
              :key="`tr ${driller.person_guid} ${index}`" :id="`registry-table-row-${index}`">
            <td :id="`drillerName${index}`">
              <router-link
                v-if="userRoles.registry.view"
                :to="{ name: 'PersonDetail', params: { person_guid: driller.person_guid } }">
                  {{ driller.surname }}, {{ driller.first_name }}
              </router-link>
              <div v-else class="font-weight-bold">
                {{ driller.surname }}, {{ driller.first_name }}
              </div>
              <div v-if="driller.registrations && driller.registrations.length">
                <div
                    v-for="(reg, regIndex) in driller.registrations"
                    v-if="reg.activity === activity"
                    :key="`reg no ${driller.person_guid} ${regIndex}`">
                  {{ reg.registration_no }}</div>
              </div>
            </td>
            <td :id="`personOrg${index}`">
              <driller-org-name :driller="driller" :activity="activity"></driller-org-name>
            <td :id="`personAddress${index}`">
              <driller-org-address :driller="driller" :activity="activity"></driller-org-address>
            </td>
            <td :id="`personContact${index}`">
              <div>
                <driller-contact-info :driller="driller"/>
              </div>
            </td>
            <td v-if="activity === 'DRILL'" :id="`personSubActivity${index}`">
              <driller-subactivity :driller="driller"/>
            </td>
            <td :id="`certAuth${index}`">
              <driller-certificate-authority :driller="driller" :activity="activity"/>
            </td>
            <td v-if="userRoles.registry.view && activity === 'DRILL'" :id="`personRegStatus${index}`">
              <driller-registration-status :driller="driller" :activity="activity"/>
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
            <li>
              <button type="button" @click="paginationPrev" class="btn btn-default" aria-label="Previous" id="table-pagination-prev" :disabled="!drillers.previous">
                <span aria-hidden="true">Previous</span>
              </button>
            </li>
            <li>
              <button type="button" @click="paginationNext" class="btn btn-default" aria-label="Next" id="table-pagination-next" :disabled="!drillers.next">
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
import DrillerSubactivity from '@/registry/components/search/table-helpers/DrillerSubactivity.vue'
import DrillerRegistrationStatus from '@/registry/components/search/table-helpers/DrillerRegistrationStatus.vue'
import DrillerContactInfo from '@/registry/components/search/table-helpers/DrillerContactInfo.vue'
import DrillerCertAuth from '@/registry/components/search/table-helpers/DrillerCertAuth.vue'
import DrillerOrganization from '@/registry/components/search/table-helpers/DrillerOrganization.vue'
import DrillerOrgAddress from '@/registry/components/search/table-helpers/DrillerOrgAddress.vue'

const querystring = require('querystring')

export default {
  name: 'RegisterTable',
  components: {
    'driller-subactivity': DrillerSubactivity,
    'driller-registration-status': DrillerRegistrationStatus,
    'driller-contact-info': DrillerContactInfo,
    'driller-certificate-authority': DrillerCertAuth,
    'driller-org-name': DrillerOrganization,
    'driller-org-address': DrillerOrgAddress
  },
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
          class: 'col-xs-1',
          visible: 'public',
          sortable: false,
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
          sortable: false,
          activity: 'DRILL'
        },
        {
          name: 'Certificate Issued By',
          class: 'col-xs-1',
          visible: 'public',
          sortable: false,
          activity: 'all'
        },
        {
          name: 'Registration Status',
          class: 'col-xs-1',
          visible: 'admin',
          sortable: false,
          activity: 'DRILL'
        }
      ]
    }
  },
  computed: {
    ...mapGetters([
      'loading',
      'listError',
      'userRoles',
      'drillers',
      'activity'
    ])
  },
  watch: {
    // When drillers has a new state, scroll to the top of the searchTable.
    drillers () {
      this.scrollToTableTop()
    }
  },
  methods: {
    /**
     * Gets called when the user clicks on the next button, load the next result page.
     */
    paginationNext () {
      // API provides 'next' and 'previous' links with query strings for the current search
      if (this.drillers.next && ~this.drillers.next.indexOf('?'))
        this.getPage(this.drillers.next.split('?')[1])
    },
    /**
     * Gets called when the user clicks on the previous button, load the previous result page.
     */
    paginationPrev () {
      if (this.drillers.previous && ~this.drillers.previous.indexOf('?'))
        this.getPage(this.drillers.previous.split('?')[1])
    },
    /**
     * Triggers FETCH_DRILLER_LIST store action.
     * @param {string} query QueryString of the new page to be loaded.
     */
    getPage (query) {
      if(!query) throw new Error('query parameter is required.')
      this.$store.dispatch(FETCH_DRILLER_LIST, querystring.parse(query))
    },
    sortBy (sortCode) {
      this.$emit('sort', sortCode)
    },
    /**
     * Scrolls user's screen to the top of the SearchTable component.
     */
    scrollToTableTop () {
      this.$SmoothScroll(this.$el, 100)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

</style>
