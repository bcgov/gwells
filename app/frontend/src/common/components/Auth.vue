<template>
  <div>
    <div v-if="!keycloak || (keycloak && !keycloak.authenticated)">
      <button type="button" id="gwells-sso-login" class="btn btn-light btn-sm d-none d-sm-block" @click="keyCloakLogin()">Log in</button>
      <div id="ribbon-gwells-sso-login" class="d-sm-none" @click="keyCloakLogin()">Log in</div>
    </div>
    <div v-if="keycloak && keycloak.authenticated">
      <span class="userLoggedInText text-light d-none d-sm-block">{{ keycloak.tokenParsed.name }}</span>
      <button type="button" class="btn btn-light btn-sm d-none d-sm-block" @click="keyCloakLogout()">Log out</button>
      <div id="ribbon-gwells-sso-logout" class="d-sm-none" @click="keyCloakLogout()">Log out</div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '@/common/services/ApiService.js'
import { SET_ERROR } from '@/registry/store/mutations.types.js'

export default {
  data () {
    return {
    }
  },
  computed: {
    ...mapGetters(['keycloak'])
  },
  methods: {
    keyCloakLogin () {
      if (this.keycloak) {
        this.keycloak.init().success(() => {
          this.keycloak.login({ idpHint: 'idir' }).success((authenticated) => {
            if (authenticated) {
              ApiService.authHeader('JWT', this.keycloak.token)
              localStorage.setItem('token', this.keycloak.token)
              localStorage.setItem('refreshToken', this.keycloak.refreshToken)
              localStorage.setItem('idToken', this.keycloak.idToken)
            }
          }).error((e) => {
            this.$store.commit(SET_ERROR, { error: 'Cannot contact SSO provider' })
          })
        })
      }
    },
    keyCloakLogout () {
      // This should log the user out, but unfortunately does not delete the cookie storing the user
      // token.
      if (this.keycloak && this.keycloak.authenticated) {
        this.keycloak.clearToken()
        ApiService.authHeader()
        localStorage.removeItem('token')
        localStorage.removeItem('refreshToken')
        localStorage.removeItem('idToken')
        this.keycloak.logout() // This redirects the user to a logout screen.
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
