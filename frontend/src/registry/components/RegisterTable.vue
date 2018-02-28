<template>
  <div class="">
    <div class="table-responsive">
      <table class="table table-striped">
        <thead>
          <th class="col-xs-2" v-for="field in fields" :key="field">{{field}}</th>
        </thead>
        <tbody>
          <tr id="registry-table-row" v-if="drillers.results && drillers.results.length" v-for="driller in drillers.results" :key="driller.person_guid">
            <td>{{ driller.first_name }} {{ driller.surname }}</td>
            <td>{{ driller.organization_name }}</td>
            <td>{{ driller.contact_tel }}</td>
            <td>{{ driller.contact_email }}</td>
            <td>{{ driller.activity }}</td>
            <td><router-link :to="{ name: 'PersonDetail', params: { person_guid: driller.person_guid } }">Details</router-link></td>
          </tr>
          <tr v-else>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
          </tr>
        </tbody>
      </table>
    </div>
    <!-- <div v-if="loading">Loading results...</div> -->
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
  props: ['items'],
  data () {
    return {
      fields: ['Name', 'Company', 'Telephone', 'E-mail', 'Qualification']
    }
  },
  computed: {
    ...mapGetters([
      'loading',
      'listError',
      'drillers'
    ])
  },
  methods: {
    paginationNext () {
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
