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
          <b-navbar-toggle class="d-sm-none" target="nav_collapse"></b-navbar-toggle>
          <b-nav-item>
            <keycloak-auth/>
          </b-nav-item>
        </b-navbar-nav>
      </b-container>
    </b-navbar>
    <b-navbar class="bc-nav-links py-0" toggleable="sm" type="dark">
      <b-container fluid>
        <b-collapse class="py-2" is-nav id="nav_collapse">
          <b-container id="navContainer">
            <b-navbar-nav>
              <b-nav-text class="d-sm-none text-light">Groundwater Wells and Aquifers</b-nav-text>
              <b-nav-item class="navbar-link lvl2-link" href="#">Well Search</b-nav-item>
              <b-nav-item class="navbar-link lvl2-link" href="#">Groundwater Information</b-nav-item>
              <b-nav-item class="navbar-link lvl2-link" href="#">Registry</b-nav-item>
            </b-navbar-nav>
          </b-container>
        </b-collapse>
      </b-container>
    </b-navbar>
  </header>
</template>

<script>
import { mapGetters } from 'vuex'
import { LOGIN, LOGOUT } from '@/registry/store/actions.types'
import Auth from '@/common/components/Auth.vue'
export default {
  components: {
    'keycloak-auth': Auth
  },
  data () {
    return {
      loginPopover: false,
      loginUsernameState: null,
      loginPasswordState: null,
      credentials: {
        username: null,
        password: null
      }
    }
  },
  computed: {
    ...mapGetters([
      'user'
    ])
  },
  watch: {
    'credentials.username' (val) {
      if (val) {
        this.loginUsernameState = true
      }
    },
    'credentials.password' (val) {
      if (val) {
        this.loginPasswordState = true
      }
    }
  },
  methods: {
    login (evt) {
      evt.preventDefault()
      if (!this.credentials.username) { this.loginUsernameState = false }
      if (!this.credentials.password) { this.loginPasswordState = false }
      if (this.credentials.username && this.credentials.password) {
        this.$store.dispatch(LOGIN, this.credentials)
        this.loginPopover = false
      }
    },
    logout () {
      this.$router.push('/')
      this.$store.dispatch(LOGOUT)
    },
    onLoginShown () {
      /* Transfer focus to the first input */
      this.credentials.username = ''
      this.credentials.password = ''
      this.loginUsernameState = null
      this.loginPasswordState = null
      this.$refs.input1.focus()
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
