<template>
  <div class="">
    <div class="table-responsive">
      <table class="table table-striped">
        <thead>
          <th v-for="field in fields" :key="field.name" :class="field.class" v-if="(field.visible === 'public' || user) && (field.activity === activity || field.activity == 'all')">
            {{field.name}} <i class="fa fa-sort" v-if="field.sortable && field.sortCode" @click="sortBy(field.sortCode)"></i>
          </th>
        </thead>
        <tbody>
          <tr id="registry-table-row" v-if="drillers.results && drillers.results.length" v-for="driller in drillers.results" :key="driller.person_guid">
            <td>
              <div><b>{{ driller.first_name }} {{ driller.surname }}</b></div>
              <div>{{ driller.registration_no }}</div>
            </td>
            <td>{{ driller.organization_name }}</td>
            <td>{{ driller.street_address }}<div>{{ driller.city }}<span v-if="driller.province_state">, {{ driller.province_state }}</span></div></td>
            <td><div v-if="driller.contact_tel">Phone: {{ driller.contact_tel }}</div><div v-if="driller.contact_email">Email: {{ driller.contact_email }}</div></td>
            <td v-if="activity === 'DRILL'">{{ driller.activity }}</td>
            <td></td>
            <td>{{ driller.status }}</td>
            <td v-if="user"><router-link :to="{ name: 'PersonDetail', params: { person_guid: driller.person_guid } }">Details</router-link></td>
          </tr>
          <tr v-else>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="drillers.results && !drillers.results.length">No results were found.</div>
    <div class="row">
      <div class="col-xs-12 col-sm-4">
        <span v-if="drillers.results && drillers.results.length">Showing {{ drillers.offset + 1 }} to {{ drillers.offset + drillers.results.length }} of {{ drillers.count }}</span>
      </div>
      <div v-if="drillers.results && drillers.results.length" class="col-xs-12 col-sm-4 col-sm-offset-4 col-md-offset-5 col-md-3">
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
          name: 'Qualified to Drill',
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
          visible: 'public',
          sortable: false,
          activity: 'all'
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
<style scoped>

</style>
