<template>
  <div id="app">
    <b-container>
      <b-row>
        <b-col>
          <a id="main-content-anchor"></a>
          <h1>Register of Well Drillers and Well Pump Installers</h1>
            <p><a>Learn more about registering as a well driller or well pump installer in B.C.</a></p>
        </b-col>
      </b-row>
      <b-row>
        <div>
          <router-view/>
        </div>
      </b-row>
    </b-container>
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
@import "bootstrap/dist/css/bootstrap.min.css";
@import "bootstrap-vue/dist/bootstrap-vue.css";
/* @import '../assets/css/main.css'; */
</style>
