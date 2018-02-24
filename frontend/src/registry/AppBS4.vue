<template>
  <div id="app">
    <router-view/>      
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
