<template>
  <div id="app">
    <b-container fluid class="app-wrapper">
      <gwells-header/>
      <b-container style="background-color: #ffffff; padding-top: 25px; margin-bottom: 45px; height: 100%">
        <router-view/>
      </b-container>
    </b-container>
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
@font-face {
  font-family: 'Myriad-Pro';
  src: url('../assets/fonts/MyriadWebPro.ttf');
}

.app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  margin-bottom: -45px;
  padding: 0;
}

#app {
  font-family: Myriad-Pro, Calibri, Arial, 'sans serif';
  background-color: #f1f1f1;
  color: #494949;
  font-size: 13px;
}

#app a {
  color: #1a5a96;
}

#app a:hover, .navbar-link a:hover {
  color: #00F;
  text-decoration: underline;
}

h1, h2, h3, h4, h5 {
  margin-top: 0;
  color: #494949;
}

h1 {
  font-size: 24px;
  font-weight: 600;
}

h2 {
  font-size: 21px;
}

h3 {
  font-size: 18px;
}

h4 {
  font-size: 15px;
}

.btn {
  border-radius: 0;
}

.btn-primary {
    color: #fff;
    background-color: #38598a;
    border-color: #003366;
}

    .btn-primary:focus,
    .btn-primary.focus {
        color: #fff;
        background-color: #003366;
        border-color: #003366;
    }

    .btn-primary:hover {
        color: #fff;
        background-color: #003366;
        border-color: #003366;
    }

.btn-secondary {
  color: #333;
  background-color: #d1d1d1;
  border-color: #afafaf;
}

.btn-outline-primary {
  color: #003366;
  border-color: #003366;
}

#app .col-form-label {
  font-weight: bold;
}

</style>
