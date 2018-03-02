<template>
  <div class="">
    <div class="table-responsive">
      <table class="table table-striped">
        <thead>
          <th v-for="field in fields" :key="field.name" :class="field.class" v-if="field.visible === 'public' || user">{{field.name}}</th>
        </thead>
        <tbody>
          <tr id="registry-table-row" v-if="drillers.results && drillers.results.length" v-for="driller in drillers.results" :key="driller.person_guid">
            <td>{{ driller.first_name }} {{ driller.surname }}</td>
            <td>{{ driller.organization_name }}</td>
            <td>{{ driller.street_address }}</td>
            <td>{{ driller.city }}<span v-if="driller.province_state">, {{ driller.province_state }}</span></td>
            <td>{{ driller.contact_tel }}</td>
            <td>{{ driller.contact_email }}</td>
            <td>{{ driller.activity }}</td>
            <td v-if="user"><router-link :to="{ name: 'PersonDetail', params: { person_guid: driller.person_guid } }">Details</router-link></td>
          </tr>
          <tr v-else>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="drillers.results && !drillers.results.length">No results were found.</div>
    <div v-if="drillers.results && drillers.results.length" class="col-sm-offset-10">
      <nav aria-label="List navigation" v-if="drillers.results && drillers.results.length">
        <ul class="pagination">
          <li v-if="drillers.previous">
            <button @click="paginationPrev" class="btn btn-default" aria-label="Previous">
              <span aria-hidden="true">Previous</span>
            </button>
          </li>
          <li v-else>
            <button class="btn btn-default disabled" aria-hidden="true">
              <span aria-hidden="true">Previous</span>
            </button>
          </li>
          <li v-if="drillers.next">
            <button @click="paginationNext" class="btn btn-default" aria-label="Next" id="table-pagination-next">
              <span aria-hidden="true">Next</span>
            </button>
          </li>
          <li v-else>
            <button class="btn btn-default disabled" aria-hidden="true" id="table-pagination-prev">
              <span aria-hidden="true">Next</span>
            </button>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { FETCH_DRILLER_LIST } from '@/registry/store/actions.types'
const querystring = require('querystring')

export default {
  name: 'RegisterTable',
  data () {
    return {
      // fields for the table headings\
      // visible denotes whether field should be visible to public or admin only
      fields: [
        {
          name: 'Name',
          class: 'col-xs-2',
          visible: 'public'
        },
        {
          name: 'Company',
          class: 'col-xs-2',
          visible: 'public'
        },
        {
          name: 'Address',
          class: 'col-xs-2',
          visible: 'public'
        },
        {
          name: 'City',
          class: 'col-xs-1',
          visible: 'public'
        },
        {
          name: 'Telephone',
          class: 'col-xs-1',
          visible: 'public'
        },
        {
          name: 'E-mail',
          class: 'col-xs-1',
          visible: 'public'
        },
        {
          name: 'Qualification',
          class: 'col-xs-1',
          visible: 'public'
        },
        {
          name: 'Details',
          class: 'col-xs-1',
          visible: 'admin'
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
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
