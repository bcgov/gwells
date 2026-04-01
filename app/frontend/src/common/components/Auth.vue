<template>
  <div>
    <span v-if="commonStore.authenticated" class="userLoggedInText text-light">
      {{ commonStore.keycloak.tokenParsed.name }}
    </span>
    <b-btn  variant="light" size="sm" :id="`${id}-logout-button`" :disabled="!ready" @click="buttonClicked()">
      {{commonStore.authenticated ? 'Log out' : 'Log in'}}
    </b-btn>
  </div>
</template>

<script>
import { useCommonStore } from '@/stores/common.js'
import ApiService from '@/common/services/ApiService.js'
import { useRegistryStore } from '@/stores/registry.js'

export default {
  props: {
    id: {
      type: String,
      default: 'sso-auth'
    }
  },
  data () {
    return {
      ready: false,
      registryStore: useRegistryStore()
    }
  },
  computed: {
    commonStore () { return useCommonStore() }
  },
  methods: {
    buttonClicked () {
      if (this.commonStore.authenticated) {
        this.keyCloakLogout()
      } else {
        this.keyCloakLogin()
      }
    },
    keyCloakLogin () {
      if (!this.commonStore.keycloak.authenticated) {
        if (!this.commonStore.keycloak.didInitialize) {
          console.log('keyCloakLogin: ', this.commonStore.keycloak.didInitialize)
          this.commonStore.keycloak.init({
            checkLoginIframe: false
          }).then(() => {
            this.commonStore.keycloak.login({ idpHint: this.commonStore.config.sso_idp_hint }).then((authenticated) => {
              if (authenticated) {
                ApiService.authHeader('JWT', this.commonStore.keycloak.token)
                if (window.localStorage) {
                  localStorage.setItem('token', this.commonStore.keycloak.token)
                  localStorage.setItem('refreshToken', this.commonStore.keycloak.refreshToken)
                  localStorage.setItem('idToken', this.commonStore.keycloak.idToken)
                }
              }
            }).catch((e) => {
              console.error("keyCloakLogin: ", e)
              this.registryStore.setError({ error: 'Cannot contact SSO provider' })
            })
          })
        } else {
          this.commonStore.keycloak.login({ idpHint: this.commonStore.config.sso_idp_hint }).then((authenticated) => {
            if (authenticated) {
              ApiService.authHeader('JWT', this.commonStore.keycloak.token)
              if (window.localStorage) {
                localStorage.setItem('token', this.commonStore.keycloak.token)
                localStorage.setItem('refreshToken', this.commonStore.keycloak.refreshToken)
                localStorage.setItem('idToken', this.commonStore.keycloak.idToken)
              }
            }
          }).catch((e) => {
            console.error("keyCloakLogin: ", e)
            this.registryStore.setError({ error: 'Cannot contact SSO provider' })
          })
        }
      } else {
        this.commonStore.keycloak.updateToken(30)
      }
    },
    keyCloakLogout () {
      // This should log the user out, but unfortunately does not delete the cookie storing the user
      // token.
      this.commonStore.keycloak.clearToken()
      ApiService.authHeader()
      if (window.localStorage) {
        localStorage.removeItem('token')
        localStorage.removeItem('refreshToken')
        localStorage.removeItem('idToken')
      }
      this.commonStore.keycloak.logout() // This redirects the user to a logout screen.
    }
  },
  watch: {
    'commonStore.keycloak' (kc) {
      if (kc) {
        if (window._paq && this.commonStore.authenticated) {
          window._paq.push(['setCustomVariable', 1, 'userType', this.commonStore.keycloak.tokenParsed.identity_provider])
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
