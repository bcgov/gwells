<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <!-- Navbar content -->
      <div class="container">
        <a class="navbar-brand" href="https://www2.gov.bc.ca">

          <img class="img-fluid d-none d-sm-block" src="@/common/assets/images/17_gov3_bc_logo.svg" width="152" height="55" alt="B.C. Government Logo">

          <img class="img-fluid d-sm-none" src="@/common/assets/images/01_gov3_bc_symbol.svg" width="61" height="43" alt="B.C. Government Logo">
        </a>
        <b-navbar-nav>
          <span class="bc-nav-title d-none d-md-block">Groundwater Wells and Aquifers</span>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <b-navbar-toggle class="d-sm-none" target="nav_collapse"></b-navbar-toggle>
        </b-navbar-nav>
      </div>
    </nav>
    <b-navbar class="bc-nav-links" toggleable="sm" type="dark">
      <b-collapse class="py-2" is-nav id="nav_collapse">
        <b-container>
        <b-navbar-nav>
          <b-nav-item class="navbar-link lvl2-link" href="#">Well Search</b-nav-item>
          <b-nav-item class="navbar-link lvl2-link" href="#">Groundwater Information</b-nav-item>
          <b-nav-item class="navbar-link lvl2-link" href="#">Registry</b-nav-item>
        </b-navbar-nav></b-container>
      </b-collapse>
    </b-navbar>
  </header>
</template>

<script>
export default {

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
  margin-bottom: 20px;
  -webkit-box-shadow: 0px 3px 3px 1px rgba(51, 51, 51, 0.5);
  -moz-box-shadow: 0px 3px 3px 1px rgba(51, 51, 51, 0.5);
  box-shadow: 0px 3px 3px 1px rgba(51, 51, 51, 0.5);
}
header li + li {
  @include media-breakpoint-up(sm) {
    border-left: 1px solid #fff;
  }
}
.lvl2-link a {
  padding-top:0;
  padding-bottom:0;
}
</style>
