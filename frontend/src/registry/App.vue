<template>
  <div>
    <gwells-header/>
    <main role="main">
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
@import url('https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css');
@import '../../../gwells/static/gwells/css/ie10-viewport-bug-workaround.css';
@import '~bootstrap/scss/_functions';
@import '~bootstrap/scss/_variables';
@import '~bootstrap/scss/mixins/_breakpoints';

html {
  font-size: 14px;
}
body {
  display: flex;
  flex-direction: column;
  height: 100%;
}
main {
  margin-bottom: 45px;
  padding-top: 20px;
  flex: auto;
}
header,
footer {
  flex: none;
}
.h1, .h2, .h3, .h4, .h5, .h6, h1, h2, h3, h4, h5, h6 {
  font-weight: 700;
}

// BC Gov Bootstrap 4 theme override
.custom-select[size]:not([size="0"]) {
  height:auto;
  padding-right:.75rem;
  background-image:none;
}
</style>
