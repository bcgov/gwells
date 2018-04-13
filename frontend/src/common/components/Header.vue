<template>
  <header>
    <b-navbar type="dark" class="navbar-expand-lg" bg-variant="primary">
      <!-- Navbar content -->
      <b-container>
        <a class="navbar-brand" href="https://www2.gov.bc.ca">
          <img
              class="img-fluid d-none d-sm-block"
              src="@/common/assets/images/17_gov3_bc_logo.svg"
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
          <span class="bc-nav-title d-none d-md-block">Groundwater Wells and Aquifers</span>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-item>
            <keycloak-auth/>
          </b-nav-item>
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
              <b-nav-text class="d-sm-none text-light">Groundwater Wells and Aquifers</b-nav-text>
              <b-nav-item class="navbar-link lvl2-link" :href="url.search">Well Search</b-nav-item>
              <b-nav-item class="navbar-link lvl2-link" :href="url.groundWater">Groundwater Information</b-nav-item>
              <b-nav-item class="navbar-link lvl2-link" :href="url.registry">Registry</b-nav-item>
              <b-nav-item class="navbar-link lvl2-link" v-if="show.dataEntry" :href="url.report">Submit Report</b-nav-item>
              <b-nav-item class="navbar-link lvl2-link" v-if="show.admin" :href="url.admin">Admin</b-nav-item>
              <!--
                Need to match:
                {% if settings.ENABLE_DATA_ENTRY %}
                <li><a id="navbar-submission" href="{% url 'activity_submission_create' %}">Submit Report</a></li>
                {% endif %}
                {% if request.user|has_group:"admin" %}
                <li><a id="collapsable-ribbon-admin" href="{% url 'site_admin' %}">Admin</a></li>
                {% endif %}
               -->
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
  data () {
    // TODO: Get this value from the store (vueX?)
    let baseUrl = 'http://localhost:8000/gwells'
    return {
      url: {
        search: baseUrl,
        groundWater: baseUrl + '/groundwater-information',
        registry: baseUrl + '/registries',
        report: baseUrl + '/submission/create',
        // TODO: The django admin url should be set by environment and pulled in with webpack, placed into
        // store (vuex?) and accessed from there.
        admin: baseUrl + '/admin'
      },
      show: {
        // TODO: Get these values from stor (VueX?)
        // TODO: Find some other way, this is picked up as an error by webpack, complaining that the
        // variables are not defined.
        dataEntry: (typeof ENABLE_DATA_ENTRY === 'undefined') ? false : ENABLE_DATA_ENTRY,
        admin: (typeof SHOW_ADMIN === 'undefined') ? false : SHOW_ADMIN
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
</style>
