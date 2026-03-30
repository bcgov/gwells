<template>
  <div>
    <gwells-header ref="header"/>
    <main role="main" class="p-0 mt-4">
      <router-view/>
    </main>
    <gwells-footer/>
    <back-to-top :target="$refs.header"/>
  </div>
</template>

<script>
import { useCommonStore } from '@/stores/common.js'
import Header from './common/components/Header.vue'
import Footer from './common/components/Footer.vue'
import BackToTop from './common/components/BackToTop.vue'
import useSubmissionStore from './stores/submission'
export default {
  name: 'App',
  components: {
    'gwells-header': Header,
    'gwells-footer': Footer,
    BackToTop
  },
  data () {
    return {
      commonStore: useCommonStore()
    }
  },
  computed: {
    submissionStore () { return useSubmissionStore() }
  },
  created () {
    console.log('New deploy of Gwells')
    this.commonStore.fetchConfig()
    window._paq = window._paq || []
    window._paq.push(['trackPageView']) // To track pageview -
  }
}
</script>

<style lang="scss">
  @use './common/common.scss' as *;
  @use './common/mapbox.scss' as *;
  @use './common/assets/css/ie10-viewport-bug-workaround.css' as *;

  @media (min-width: 1500px) {
    .container {
      max-width: 1400px!important;
    }
  }

  @media print {
    .registries-edit-btn {
      display: none!important;
    }
    .registries-action-button {
      display: none!important;
    }
  }

  // remove cursor CSS from bootstrap tables
  table.b-table tr {
    cursor: default !important;
  }

  .buorg {
    background-color: #FFEAEA !important;
    border-bottom-color: #FFB8B8 !important;
  }
</style>
