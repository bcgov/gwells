<template>
  <div class="app-view d-flex flex-column">
    <gwells-header ref="header"/>
    <main role="main" class="p-0 mt-0 mt-sm-4 main-body justify-content-center">
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
  @import './common/assets/css/ie10-viewport-bug-workaround.css';

  @media (min-width: 1500px) {
    .container {
      max-width: 1400px
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

  .app-view {
    min-height: 100vh;
  }

  .main-body {
    display: flex;
    flex: 1 0 0%;
  }

  .body-wrapper {
    flex: none;
  }

</style>
