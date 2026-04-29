<template>
  <div id="qaqcDashboard">
    <h1>QA/QC Dashboard</h1>
    <Tabs v-model:value="currentTab" content-class="mt-4">
      <TabList>
        <Tab :value="0" active>Record Compliance</Tab>
        <Tab :value="1">Mislocated Wells</Tab>
        <Tab :value="2">Cross Referencing</Tab>
      </TabList>
    </Tabs>
    <QaQcTable :tab="currentTab"></QaQcTable>
  </div>
</template>
<script>

// Import your table components
import { Tabs, TabList, Tab } from 'primevue'
import QaQcTable from '../components/QaQcTable.vue'
import { useSubmissionStore } from '@/stores/submission'
import { useQAQCStore } from '@/stores/qaqc'

export default {
  name: 'QaQcDashboard',
  components: {
    QaQcTable,
    Tab,
    TabList,
    Tabs
  },
  computed: {
    submissionStore() { return useSubmissionStore() },
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
    this.submissionStore.fetchCodes()
  }
}
</script>
<style lang="scss" scoped>
#qaqcDashboard {
  margin: 5px
}
</style>
