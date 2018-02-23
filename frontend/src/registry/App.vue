<template>
  <div id="app">
    <gwells-header/>
    <div id="topicTemplate" class="template container gov-container">
      <div class="row">
        <div id="main-content" role="main" class="contentPageMainColumn col-sm-12">
          <a id="main-content-anchor"></a>
          <h1>Register of Well Drillers and Well Pump Installers</h1>
          <div id="introduction">
            <p><a>Learn more about registering as a well driller or well pump installer in B.C.</a></p>
          </div>
        </div>
        <div>
          <router-view/>
        </div>
      </div>
    </div>
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
