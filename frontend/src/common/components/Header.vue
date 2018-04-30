<template>
  <header>
    <b-navbar type="dark" class="navbar-expand-lg d-print-block" bg-variant="primary">
      <!-- Navbar content -->
      <b-container>
        <a class="navbar-brand" href="https://www2.gov.bc.ca">
          <img
              class="nav-logo img-fluid d-none d-sm-block"
              src="@/common/assets/images/17_gov3_bc_logo.svg"
              width="152" height="55"
              alt="B.C. Government Logo">
          <img
              class="img-fluid d-none d-sm-block nav-logo-print"
              src="@/common/assets/images/17_gov3_bc_logo_transparent.svg"
              width="152" height="55"
              alt="B.C. Government Logo">
          <img
              class="img-fluid d-sm-none"
              src="@/common/assets/images/01_gov3_bc_symbol.svg"
              width="61"
              height="43"
              alt="B.C. Government Logo">
        </a>
        <b-navbar-nav>
          <li class="bc-nav-title d-none d-md-block">Groundwater Wells and Aquifers</li>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <li>
            <keycloak-auth v-if="auth !== 'hide'"/>
          </li>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto d-sm-none">
          <b-navbar-toggle class="d-sm-none" target="nav_collapse"></b-navbar-toggle>
        </b-navbar-nav>
      </b-container>
    </b-navbar>
    <b-navbar class="bc-nav-links py-0" toggleable="sm" type="dark">
      <b-container fluid>
        <b-collapse class="py-2" is-nav id="nav_collapse">
          <b-container id="navContainer">
            <b-navbar-nav>
              <li class="d-sm-none text-light mb-2 mt-2">Groundwater Wells and Aquifers</li>
              <b-nav-item id="ribbon-search" class="navbar-link lvl2-link" href="/gwells">Well Search</b-nav-item>
              <b-nav-item id="ribbon-groundwaterinfo" class="navbar-link lvl2-link" href="/gwells/groundwater-information">Groundwater Information</b-nav-item>
              <b-nav-item id="ribbon-registry" class="navbar-link lvl2-link" href="/gwells/registries">Registry</b-nav-item>
              <b-nav-item class="navbar-link lvl2-link" v-if="show.dataEntry" href="/gwells/submission/create">Submit Report</b-nav-item>
              <b-nav-item id="ribbon-admin" class="navbar-link lvl2-link" v-if="show.admin" href="/gwells/admin">Admin</b-nav-item>
            </b-navbar-nav>
          </b-container>
        </b-collapse>
      </b-container>
    </b-navbar>
  </header>
</template>

<script>
import Auth from '@/common/components/Auth.vue'
export default {
  components: {
    'keycloak-auth': Auth
  },
  props: ['auth'],
  data () {
    let adminMeta = document.head.querySelector('meta[name="show.admin"]')
    return {
      show: {
        dataEntry: process.env.ENABLE_DATA_ENTRY,
        admin: adminMeta ? adminMeta.content === 'true' : false
      }
    }
  }
}
</script>

<style lang="scss">
@import '~bootstrap/scss/_functions';
@import '~bootstrap/scss/_variables';
@import '~bootstrap/scss/mixins/_breakpoints';

.navbar {
  margin-bottom: 0px;
}
.nav-item {
  font-size: 13px;
}
.bc-nav-title {
  font-size: 2em;
  color: #fff!important;
  margin-bottom: -10px;
}
.bc-nav-links {
  background-color: #38598a;
  border-bottom: 0px;
  padding-top: 0px;
  padding-bottom: 0px;
  -webkit-box-shadow: 0px 3px 3px 1px rgba(51, 51, 51, 0.5);
  -moz-box-shadow: 0px 3px 3px 1px rgba(51, 51, 51, 0.5);
  box-shadow: 0px 3px 3px 1px rgba(51, 51, 51, 0.5);
}
header li + li {
  @include media-breakpoint-up(sm) {
    border-left: 1px solid #607D8B;
  }
}
.lvl2-link a {
  padding-top:0;
  padding-bottom:0;
}
.nav-logo-print {
  height: 0px !important;
}
@media print {
  header nav {
    background-color: rgba(0,0,0,0) !important;
    border-bottom: none !important;
  }
  .bc-nav-title {
    color: #000 !important;
  }
  .nav-logo-print {
    height: 55px !important;
  }
  .nav-logo {
    height: 0px !important;
  }
}
</style>
