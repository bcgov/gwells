<!-- TODO: This file may be redundant, just use the Footer.vue file directly -->
<template>
  <div>
    <gwells-header/>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Header from '@/common/components/Header'
export default {
  name: 'Headie',
  components: {
    'gwells-header': Header
  },
  computed: {
    ...mapGetters([
      'error'
    ])
  }
}
</script>

<style lang="scss">
@import url('https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css');
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
  background-color: #f1f1f1;
  // margin-bottom: 45px!important;
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
  font-weight: 500;
}
.col-form-label {
  font-weight: 600;
}
</style>
