<template>
  <div>
    <div v-if="!keycloak || (keycloak && !keycloak.authenticated)">
      <button type="button" class="btn btn-light" @click="keyCloakLogin()">Log in</button>
    </div>
    <div v-if="keycloak && keycloak.authenticated">Logged in <span>({{ keycloak.tokenParsed.name }})</span></div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Keycloak from 'keycloak-js'
import ApiService from '@/common/services/ApiService.js'
import { SET_KEYCLOAK } from '@/registry/store/mutations.types.js'

export default {
  data () {
    return {
      kc: null
    }
  },
  computed: {
    ...mapGetters(['user', 'keycloak'])
  },
  methods: {
    keyCloakInit () {
      const kc = Keycloak({
        'realm': 'gwells',
        'url': 'https://dev-sso.pathfinder.gov.bc.ca/auth',
        'clientId': 'webapp-dev-local'
      })
      kc.init({onLoad: 'check-sso'}).success(() => {
        console.log('kc init')
        this.kc = kc
        this.$store.commit(SET_KEYCLOAK, kc)
        ApiService.authHeader('JWT', kc.token)
      })
    },
    keyCloakLogin () {
      if (this.kc) {
        this.kc.login().success((authenticated) => {
          if (authenticated) {
            this.$store.commit(SET_KEYCLOAK, this.kc)
            ApiService.authHeader('JWT', this.kc.token)
          }
        })
      }
    }
  },
  created () {
    this.keyCloakInit()
  }
}
</script>

<style>

</style>
