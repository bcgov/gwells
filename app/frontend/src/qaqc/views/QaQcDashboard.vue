<template>
  <div id="qaqcDashboard">
    <h1>QA/QC Dashboard</h1>
    <b-tabs v-model="currentTab" content-class="mt-3">
      <b-tab title="Record Compliance"></b-tab>
      <b-tab title="Mislocated Wells"></b-tab>
      <b-tab title="Cross Referencing"></b-tab>
    </b-tabs>
    <QaQcTable :tab="currentTab"></QaQcTable>
  </div>
</template>
<script>

// Import your table components
import QaQcTable from '../components/QaQcTable.vue'
import { FETCH_CODES } from '@/submissions/store/actions.types.js'

export default {
  name: 'QaQcDashboard',
  components: {
    QaQcTable
  },
  computed: {
    currentTab: {
      get () {
        return this.$store.state.selectedTab
      },
      set (value) {
        this.$store.dispatch('SET_QAQC_SELECTED_TAB_ACTION', value)
      }
    }
  },
  created () {
    this.$store.dispatch(FETCH_CODES)
  }
}
</script>
<style lang="scss" scoped>
#qaqcDashboard {
  margin: 5px
}
</style>
