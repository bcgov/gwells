<template>
  <div>
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
@import url('https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css');
@import '../../../gwells/static/gwells/css/ie10-viewport-bug-workaround.css';
@import '../../../gwells/static/gwells/css/main.css';
@import '../../../gwells/static/gwells/css/custom-form.css';
@import '../../../gwells/static/gwells/css/custom-main.css';
</style>
