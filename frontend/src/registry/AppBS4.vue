<template>
  <div id="app">
    <b-container style="background-color: #ffffff">
      <b-row>
        <b-col>
          <a id="main-content-anchor"></a>
          <h1 class="g-title">Register of Well Drillers and Well Pump Installers</h1>
            <p><a href="#">Learn more about registering as a well driller or well pump installer in B.C.</a></p>
        </b-col>
      </b-row>
      <b-row>
        <div>
          <b-col>
          <router-view/>
          </b-col>
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

@font-face {
  font-family: 'Myriad-Pro';
  src: url('../assets/fonts/MyriadWebPro.ttf');
}

body {
  font-family: Myriad-Pro, Calibri, Arial, 'sans serif';
  background-color: #f1f1f1;
  color: #494949;
  font-size: 13px;
}
</style>
