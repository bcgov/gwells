<template>
  <div class="p-md-2 m-50px">
    <h3>Well Driller Results</h3>
    <b-table
      responsive
      striped
      :items="items"
      :fields="fields"
    />
    <div v-if="loading">Loading results...</div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'RegisterTable',
  props: ['items'],
  data () {
    return {
      fields: ['name', 'street_address', 'city', 'province_state', 'main_tel']
    }
  },
  computed: {
    ...mapGetters([
      'loading',
      'error'
    ])
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
