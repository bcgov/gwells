<template>
  <div>
    <div v-if="!keycloak || (keycloak && !keycloak.authenticated)">
      <button type="button" class="btn btn-light btn-sm" @click="keyCloakLogin()">Log in</button>
    </div>
    <div v-if="keycloak && keycloak.authenticated">
      <span class="userLoggedInText">{{ keycloak.tokenParsed.name }}</span>
      <button type="button" class="btn btn-light btn-sm" @click="keyCloakLogout()">Log out</button>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '@/common/services/ApiService.js'

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
        this.keycloak.login({ idpHint: 'idir' }).success((authenticated) => {
          if (authenticated) {
            ApiService.authHeader('JWT', this.keycloak.token)
          }
        })
      }
    },
    keyCloakLogout () {
      if (this.keycloak && this.keycloak.authenticated) {
        this.keycloak.logout()
        this.$router.push({ name: 'SearchHome' })
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
