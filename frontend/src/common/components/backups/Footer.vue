<template>
  <b-container class="footer-wrapper" fluid>
    <b-container>
      <b-nav class="footer" style="margin-top: 3px">
          <b-nav-item><a id="footer-home" href="https://www.gov.bc.ca" target="_self">Home</a></b-nav-item>
          <b-nav-item><a id="footer-about" href="https://www2.gov.bc.ca/gov/content/about-gov-bc-ca" target="_self">About gov.bc.ca</a></b-nav-item>
          <b-nav-item><a id="footer-disclaimer" href="http://gov.bc.ca/disclaimer/" target="_self">Disclaimer</a></b-nav-item>
          <b-nav-item><a id="footer-privacy" href="http://gov.bc.ca/privacy/" target="_self">Privacy</a></b-nav-item>
          <b-nav-item><a id="footer-accessibility" href="http://gov.bc.ca/webaccessibility/" target="_self">Accessibility</a></b-nav-item>
          <b-nav-item><a id="footer-copyright" href="http://gov.bc.ca/copyright" target="_self">Copyright</a></b-nav-item>
          <b-nav-item><a href="https://www2.gov.bc.ca/gov/content/home/contact-us" target="_self">Contact Us</a></b-nav-item>
      </b-nav>
    </b-container>
  </b-container>
</template>

<script>
export default {

}
</script>

<style scoped>

.footer-wrapper {
  background-color: #003366;
  border-top: 2px solid #fcba19;
}

.footer {
  min-height: 40px;
}

.footer a {
  color: #ffffff;
}

.navbar-link a {
  margin-top: 5px;
  color: #fff!important;
}
</style>
