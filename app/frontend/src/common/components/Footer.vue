<template>
  <footer class="footer">
    <b-navbar type="dark" variant="primary" toggleable="sm">
      <b-container>
      <!-- Navbar content -->
        <b-navbar-nav>
            <b-nav-item id="footer-home" href="https://www.gov.bc.ca/">Home
            </b-nav-item>
            <b-nav-item id="footer-about" href="https://www2.gov.bc.ca/gov/content/about-gov-bc-ca">About gov.bc.ca
            </b-nav-item>
            <b-nav-item id="footer-disclaimer" href="http://gov.bc.ca/disclaimer/">Disclaimer
            </b-nav-item>
            <b-nav-item id="footer-privacy" href="http://gov.bc.ca/privacy/">Privacy
            </b-nav-item>
            <b-nav-item id="footer-accessibility" href="http://gov.bc.ca/webaccessibility/">Accessibility
            </b-nav-item>
            <b-nav-item id="footer-copyright" href="http://gov.bc.ca/copyright">Copyright
            </b-nav-item>
            <b-nav-item href="https://www2.gov.bc.ca/gov/content/home/contact-us">Contact Us
            </b-nav-item>
        </b-navbar-nav>
      </b-container>
    </b-navbar>
  </footer>
</template>

<script>
export default {

}
</script>

<style lang="scss">
@import '~bootstrap/scss/_functions';
@import '~bootstrap/scss/_variables';
@import '~bootstrap/scss/mixins/_breakpoints';
.footer {
  @include media-breakpoint-only(xs) {
    height: 8.2rem!important;
    margin-top: 10rem;
  }
  @include media-breakpoint-up(sm) {
    height: 45px!important;
  }
  position: absolute;
  bottom: 0
}
.footer .nav-item {
  font-size: 13px;
}
.footer .nav-link {
  padding: .1rem .5rem;
}
.footer nav {
  min-height: 45px;
}
.footer a {
  color: #fff!important;
}
footer li+li  {
  @include media-breakpoint-up(sm) {
    border-left: 1px solid #4b5e73;
  }
}
</style>
