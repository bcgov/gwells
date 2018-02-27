<template>
  <div class="">
    <div class="table-responsive">
    <table class="table table-striped" v-if="!loading">
      <thead>
        <th v-for="field in fields" :key="field">{{field}}</th>
      </thead>
      <tbody>
        <tr v-for="driller in drillers" :key="driller.person_guid">
          <td>{{ driller.name }}</td>
          <td>{{ driller.company }}</td>
          <td>{{ driller.tel }}</td>
          <td>{{ driller.email }}</td>
          <td>{{ driller.status }}</td>
        </tr>
      </tbody>
    </table>
    </div>
    <div v-if="loading">Loading results...</div>
    <div v-if="!drillers.length">No results were found.</div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

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
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
