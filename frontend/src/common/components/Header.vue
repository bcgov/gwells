<template>
  <div>
    <div class="header-wrapper">
      <b-container class="header" style="padding-top: 0px; padding-left: 0px">
        <b-row no-gutters>
          <b-col cols="3" sm="2">
            <a href="http://gov.bc.ca">
            <div class="d-none d-lg-inline">
              <img class ="header-logo" src="../../assets/images/gov3_bc_logo.png" alt="Province of British Columbia" title="Province of British Columbia logo" />
            </div>
            <div class="d-lg-none pl-2">
              <img class ="header-logo" src="../../assets/images/gov3_bc_logo_mobile.png" alt="Province of British Columbia" title="Province of British Columbia logo" />
            </div>
            </a>
          </b-col>
          <b-col class="pt-1 pt-sm-3 pt-lg-2 ml-3 ml-sm-0">
            <span class="header-title d-none d-lg-inline">Groundwater Wells and Aquifers</span>
            <span class="header-title-small d-none d-sm-inline d-lg-none">Groundwater Wells and Aquifers</span>
            <span class="header-title-xsmall d-sm-none">Groundwater Wells and Aquifers</span>
          </b-col>
        </b-row>
        <div id="access">
          <a class="sr-only sr-only-focusable" accesskey="0" href="#main-content-anchor" aria-label="Skip to main content">Skip to main content</a>
          <a class="sr-only sr-only-focusable" accesskey="0" href="#navigation-anchor" aria-label="Skip to navigation">Skip to navigation</a>
          <a class="sr-only sr-only-focusable" accesskey="0" href="http://gov.bc.ca/webaccessibility/" aria-label="Accessibility Statement">Accessibility Statement</a>
        </div>
      </b-container>
    </div>
    <b-navbar class="nav-wrapper py-0" toggleable="md" type="dark">
      <b-navbar-brand href="#"></b-navbar-brand>
      <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
      <b-collapse is-nav id="nav_collapse">
        <b-container>
        <b-navbar-nav>
          <b-nav-item class="navbar-link" href="#">Search</b-nav-item>
          <b-nav-item class="navbar-link" href="#">Groundwater Information</b-nav-item>
          <b-nav-item class="navbar-link" href="#">Registry</b-nav-item>
        </b-navbar-nav></b-container>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
export default {

}
</script>

<style scoped>

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

</style>
