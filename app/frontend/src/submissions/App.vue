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
import APIErrorMessage from '@/common/components/APIErrorMessage.vue'
export default {
  name: 'App',
  components: {
    'gwells-header': Header,
    'gwells-footer': Footer,
    'api-error': APIErrorMessage
  }
}
</script>

<style lang="scss">
@import '../common/common.scss';
.container-wide {
  max-width: 1400px
}
</style>
