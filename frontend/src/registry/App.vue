<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
// import Header from '@/common/components/Header'
// import Footer from '@/common/components/Footer'
export default {
  name: 'App',
  components: {
    // 'gwells-header': Header,
    // 'gwells-footer': Footer
  }
}
</script>

<style>
@import url('https://unpkg.com/bootstrap@3.3.7/dist/css/bootstrap.min.css');
@import '../assets/css/ie10-viewport-bug-workaround.css';
@import '../assets/css/main.css';
@import '../assets/css/custom-form.css';
@import '../assets/css/custom-main.css';
</style>
