<template>
  <div id="app">
    <gwells-header/>
    <router-view/>
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

<style>
@import '../../node_modules/bootstrap/dist/css/bootstrap.css';
@import '../assets/css/ie10-viewport-bug-workaround.css';
@import '../assets/css/main.css';
@import '../assets/css/custom-form.css';
@import '../assets/css/custom-main.css';
</style>
