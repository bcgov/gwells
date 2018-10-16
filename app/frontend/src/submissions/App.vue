<template>
  <div>
    <gwells-header/>
    <main role="main" class="p-0 mt-0 mt-sm-4 container container-wide">
      <router-view/>
    </main>
    <gwells-footer/>
  </div>
</template>

<script>
import Header from '@/common/components/Header'
import Footer from '@/common/components/Footer'
export default {
  name: 'App',
  components: {
    'gwells-header': Header,
    'gwells-footer': Footer
  }
}
</script>

<style lang="scss">
@import '../common/common.scss';
@import '../common/assets/css/ie10-viewport-bug-workaround.css';
.container-wide {
  max-width: 1400px
}
</style>
