<template>
  <div class="">
    <div class="table-responsive">
      <table class="table table-striped">
        <thead>
          <th v-for="field in fields" :key="field">{{field}}</th>
        </thead>
        <tbody v-if="drillers.results && drillers.results.length && !loading">
          <tr v-if="drillers.results && drillers.results.length && !loading" v-for="driller in drillers.results" :key="driller.person_guid">
            <td>{{ driller.first_name }} {{ driller.surname }}</td>
            <td>
              <span v-if="driller.companies && driller.companies.length">{{ driller.companies[0].organization_name }}</span></td>
            <td><span v-if="driller.companies && driller.companies.length">{{ driller.companies[0].contact_tel }}</span></td>
            <td><span v-if="driller.companies && driller.companies.length">{{ driller.companies[0].contact_email }}</span></td>
            <td>
              <span v-if="
                driller.applications &&
                driller.applications.length &&
                driller.applications[0].registrations &&
                driller.applications[0].registrations.length"
              >{{ driller.applications[0].registrations[0].status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="loading">Loading results...</div>
    <div v-if="drillers.results && !drillers.results.length">No results were found.</div>
    <div v-if="drillers.results && drillers.results.length" class="col-sm-offset-10">
      <nav aria-label="List navigation" v-if="drillers.results && drillers.results.length && !loading">
        <ul class="pagination">
          <li v-if="drillers.previous">
            <button @click="paginationPrev" class="btn btn-outline-primary" aria-label="Previous">
              <span aria-hidden="true">&laquo; Previous</span>
            </button>
          </li>
          <li v-if="drillers.next">
            <button @click="paginationNext" class="btn btn-outline-primary" aria-label="Next">
              <span aria-hidden="true">Next &raquo;</span>
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
      fields: ['Name', 'Company', 'Telephone', 'E-mail', 'Status']
    }
  },
  computed: {
    ...mapGetters([
      'loading',
      'error',
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
