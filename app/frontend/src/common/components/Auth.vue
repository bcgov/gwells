<template>
  <div>
    <div v-if="!keycloak || (keycloak && !keycloak.authenticated)">
      <button type="button" :id="`${id}-login-button`" class="btn btn-light btn-sm" @click="keyCloakLogin()">Log in</button>
    </div>
    <div v-if="keycloak && keycloak.authenticated">
      <span class="userLoggedInText text-light">{{ keycloak.tokenParsed.name }}</span>
      <button type="button" :id="`${id}-logout-button`" class="btn btn-light btn-sm" @click="keyCloakLogout()">Log out</button>
    </div>
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
    }
  },
  computed: {
    ...mapGetters(['keycloak', 'config'])
  },
  methods: {
    keyCloakLogin () {
      if (this.keycloak) {
        this.keycloak.init().success(() => {
          this.keycloak.login({ idpHint: this.config.sso_idp_hint }).success((authenticated) => {
            if (authenticated) {
              ApiService.authHeader('JWT', this.keycloak.token)
            }
          }).error((e) => {
            this.$store.commit(SET_ERROR, { error: 'Cannot contact SSO provider' })
          })
        })
      }
    },
    keyCloakLogout () {
      if (this.keycloak && this.keycloak.authenticated) {
        this.keycloak.clearToken()
        ApiService.authHeader()
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
