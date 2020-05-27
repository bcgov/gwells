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
      this.keycloak.init().success(() => {
        this.keycloak.login({ idpHint: this.config.sso_idp_hint }).success((authenticated) => {
          if (authenticated) {
            ApiService.authHeader('JWT', this.keycloak.token)
            if (window.localStorage) {
              localStorage.setItem('token', this.keycloak.token)
              localStorage.setItem('refreshToken', this.keycloak.refreshToken)
              localStorage.setItem('idToken', this.keycloak.idToken)
            }
          }
        }).error((e) => {
          this.$store.commit(SET_ERROR, { error: 'Cannot contact SSO provider' })
        })
      })
    },
    keyCloakLogout () {
      // This should log the user out, but unfortunately does not delete the cookie storing the user
      // token.
      this.keycloak.clearToken()
      ApiService.authHeader()
      if (window.localStorage) {
        localStorage.removeItem('token')
        localStorage.removeItem('refreshToken')
        localStorage.removeItem('idToken')
      }
      this.keycloak.logout() // This redirects the user to a logout screen.
    }
  },
  watch: {
    keycloak (kc) {
      if (kc) {
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
