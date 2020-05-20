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
import { mapGetters } from 'vuex'
import Header from '@/common/components/Header'
import Footer from '@/common/components/Footer'
import BackToTop from '@/common/components/BackToTop'
export default {
  name: 'App',
  components: {
    'gwells-header': Header,
    'gwells-footer': Footer,
    BackToTop
  },
  computed: {
    ...mapGetters([
      'error'
    ])
  }
}
</script>

<style lang="scss">
  @import './common/common.scss';
  @import './common/mapbox.scss';
  @import './common/assets/css/ie10-viewport-bug-workaround.css';

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
