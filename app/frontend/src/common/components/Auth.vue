<template>
  <div>
    <span v-if="authenticated" class="userLoggedInText text-light">
      {{ keycloak.tokenParsed.name }}
    </span>
    <b-btn  variant="light" size="sm" :id="`${id}-logout-button`" :disabled="!ready" @click="buttonClicked()">
      {{authenticated ? 'Log out' : 'Log in'}}
    </b-btn>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '@/common/services/ApiService.js'
import { SET_ERROR } from '@/registry/store/mutations.types.js'

export default {
  props: {
    id: {
      type: String,
      default: 'sso-auth'
    }
  },
  data () {
    return {
      ready: false
    }
  },
  computed: {
    ...mapGetters(['keycloak', 'authenticated', 'config'])
  },
  methods: {
    buttonClicked () {
      if (this.authenticated) {
        this.keyCloakLogout()
      } else {
        this.keyCloakLogin()
      }
    },
    keyCloakLogin () {
      this.keycloak.init({
        checkLoginIframe: false
      }).then(() => {
        this.keycloak.login({ idpHint: this.config.sso_idp_hint }).then((authenticated) => {
          if (authenticated) {
            ApiService.authHeader('JWT', this.keycloak.token)
            if (window.localStorage) {
              localStorage.setItem('token', this.keycloak.token)
              localStorage.setItem('refreshToken', this.keycloak.refreshToken)
              localStorage.setItem('idToken', this.keycloak.idToken)
            }
          }
        }).catch((e) => {
          console.error("keyCloakLogin: ", e)
          this.$store.commit(SET_ERROR, { error: 'Cannot contact SSO provider' })
        })
      })
    },
    keyCloakLogout () {
      // Clear local storage and other session data
      if (window.localStorage) {
        localStorage.removeItem('token')
        localStorage.removeItem('refreshToken')
        localStorage.removeItem('idToken')
      }

      // Optionally, clear cookies if the tokens are stored there
      // Example of clearing cookies (depending on how they are stored)
      document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;'

      // Logout from Keycloak
      this.keycloak.logout({
        id_token_hint: this.keycloak.token,  // Include the token hint to indicate the session to logout
        post_logout_redirect_uri: "<your-redirect-uri>"  // Redirect to a page after logout
      })
    }
  },
  watch: {
    keycloak (kc) {
      if (kc) {
        if (window._paq && this.authenticated) {
          window._paq.push(["setCustomVariable", 1, "userType", this.keycloak.tokenParsed.identity_provider]);
        }
        this.ready = true
      }
    }
  }
}
</script>

<style>
.userLoggedInText {
  margin-right: 10px;
}
</style>
