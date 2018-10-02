<template>
  <div>
    <gwells-header/>
    <main role="main" class="p-0 mt-0 mt-sm-4">
      <b-container v-if="error">
        <api-error :error="error" resetter="SET_ERROR"/>
      </b-container>
      <router-view/>
    </main>
    <gwells-footer/>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Header from '@/common/components/Header'
import Footer from '@/common/components/Footer'
import APIErrorMessage from '@/common/components/APIErrorMessage.vue'
export default {
  name: 'App',
  components: {
    'gwells-header': Header,
    'gwells-footer': Footer,
    'api-error': APIErrorMessage
  },
  computed: {
    ...mapGetters([
      'error'
    ])
  }
}
</script>

<style lang="scss">
@import '../common/common.scss';
@import '../common/assets/css/ie10-viewport-bug-workaround.css';

@media print {
  .registries-edit-btn {
    display: none!important;
  }
  .registries-action-button {
    display: none!important;
  }
}
</style>
