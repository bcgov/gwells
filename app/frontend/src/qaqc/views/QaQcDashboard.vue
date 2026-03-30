<template>
  <div id="qaqcDashboard">
    <h1>QA/QC Dashboard</h1>
    <b-tabs v-model="currentTab" content-class="mt-3">
      <b-tab title="Record Compliance" active></b-tab>
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
import { useQAQCStore } from '@/stores/qaqc'

export default {
  name: 'QaQcDashboard',
  components: {
    QaQcTable
  },
  computed: {
    qaqcStore () { return useQAQCStore() },
    currentTab: {
      get () {
        return this.qaqcStore.selectedTab
      },
      set (value) {
        this.qaqcStore.setSelectedTabAction(value)
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
