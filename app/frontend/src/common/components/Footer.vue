<template>
  <footer id="footer">
    <Menubar class="footer-nav-links [&>ul>li+li]:border-l [&>ul>li]:border-white !pl-[10%]" :model="footItems">
      <template #item="{ item }">
        <a v-if="item.visible"
          :href="item.route"
          target="_blank"
          rel="noopener"
          class="text-white px-3 hover:underline decoration-white">
          {{ item.label }}
        </a>
      </template>
      </Menubar>
  </footer>
</template>

<script>
export default {
  computed: {
    footItems () {
      return [
        { label: 'Home', route: "https://www.gov.bc.ca/", visible: true },
        { label: 'About gov.bc.ca', route: "https://www2.gov.bc.ca/gov/content/about-gov-bc-ca", visible: true },
        { label: 'Disclaimer', route: "http://gov.bc.ca/disclaimer/", visible: true },
        { label: 'Privacy', route: "http://gov.bc.ca/privacy/", visible: true },
        { label: 'Copyright', route: "http://gov.bc.ca/copyright", visible: true },
        { label: 'Contact Us', route: "https://www2.gov.bc.ca/gov/content/home/contact-us", visible: true },
      ]
    }
  }
}
</script>

<style lang="scss">

.footer-nav-links {
  background: #003366 !important;
  border-top: #F9B81B solid 3px !important;
  border-left: 0px !important;
  border-right: 0px !important;
  border-bottom: 0px !important;
  border-radius: 0px !important;
  -webkit-box-shadow: 0px 3px 3px 1px rgba(51, 51, 51, 0.5);
  -moz-box-shadow: 0px 3px 3px 1px rgba(51, 51, 51, 0.5);
  box-shadow: 0px 3px 3px 1px rgba(51, 51, 51, 0.5);
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

</style>
