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

body {
  font-family: Myriad-Pro, Calibri, Arial, 'sans serif';
  background-color: #f1f1f1;
  color: #494949;
  font-size: 13px;
}

a {
  color: #1a5a96;
}

a:hover, .navbar-link a:hover {
  color: #00F;
  text-decoration: underline;
}

.header-wrapper {
  background-color: #003366;
  border-bottom: 2px solid #fcba19;
}

.nav-wrapper {
  background-color: #38598a;
  -webkit-box-shadow: 0px 3px 3px 1px rgba(51, 51, 51, 0.5);
  -moz-box-shadow: 0px 3px 3px 1px rgba(51, 51, 51, 0.5);
  box-shadow: 0px 3px 3px 1px rgba(51, 51, 51, 0.5);
}

.footer-wrapper {
  background-color: #003366;
  border-top: 2px solid #fcba19;
}

.header {
  min-height: 68px;
  padding-top: 32px;
}

.header .header-title {
  color: #ffffff;
  font-size: 35px;
  font-weight: 600;
  margin-bottom: 0;
  margin-left: 0px;
  margin-top: 25px;
}

.header .header-title-small {
  color: #ffffff;
  font-size: 24px;
  font-weight: normal;
  margin-bottom: 0;
  margin-left: 20px;
  padding-top: 0;
}

.header .header-title-xsmall {
  color: #ffffff;
  font-size: 20px;
  font-weight: normal;
  margin-bottom: 0;
  margin-top: -10px;
  vertical-align: middle;
}

.header .header-logo {
  margin-left: 0px;
}

.navbar-link a {
  margin-top: 5px;
  color: #fff!important;
}

.footer {
  min-height: 40px;
}

.footer a {
  color: #ffffff;
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

.btn-outline-primary {
  color: #003366;
  border-color: #003366;
}

.col-form-label {
  font-weight: bold;
}

</style>
