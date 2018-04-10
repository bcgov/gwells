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
      kc.init().success((authenticated) => {
        console.log('kc init')
        this.kc = kc
        this.$store.commit(SET_KEYCLOAK, kc)
      })
    },
    keyCloakLogin () {
      if (this.kc) {
        this.kc.login()
        this.$store.commit(SET_KEYCLOAK, this.kc)
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
