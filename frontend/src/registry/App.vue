<template>
  <div id="app">
    <gwells-header/>
    <router-view/>
    <gwells-footer/>
  </div>
</template>

<script>
import Header from '@/registry/components/Header'
import Footer from '@/registry/components/Footer'
export default {
  name: 'App',
  components: {
    'gwells-header': Header,
    'gwells-footer': Footer
  }
}
</script>

<style>
@import '../../node_modules/bootstrap/dist/css/bootstrap.css';
@import '../assets/Gov-2.0-Bootstrap-Skeleton/css/ie10-viewport-bug-workaround.css';
@import '../assets/Gov-2.0-Bootstrap-Skeleton/css/main.css';
@import '../assets/Gov-2.0-Bootstrap-Skeleton/css/custom-form.css';
@import '../assets/Gov-2.0-Bootstrap-Skeleton/css/custom-main.css';
</style>
