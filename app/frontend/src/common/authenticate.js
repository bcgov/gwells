import { SET_KEYCLOAK } from '@/registry/store/mutations.types.js'
import { store } from '@/registry/store'
import Keycloak from 'keycloak-js'
import ApiService from '@/common/services/ApiService.js'

export default {
  getInstance: function () {
    // TODO: This has to read from environment configuration!
    return Keycloak({
      'realm': 'gwells',
      'url': 'https://dev-sso.pathfinder.gov.bc.ca/auth',
      'clientId': 'webapp-dev-local'
    })
  },

  authenticate: function (instance) {
    const token = localStorage.getItem('token')
    const refreshToken = localStorage.getItem('refreshToken')
    const idToken = localStorage.getItem('idToken')
    instance.init({
      onLoad: 'check-sso',
      checkLoginIframe: true,
      timeSkew: 10,
      token,
      refreshToken,
      idToken }
    ).success(() => {
      store.commit(SET_KEYCLOAK, instance)
      if (instance.authenticated) {
        localStorage.setItem('token', instance.token)
        localStorage.setItem('refreshToken', instance.refreshToken)
        localStorage.setItem('idToken', instance.idToken)
        ApiService.authHeader('JWT', instance.token)
      }
    })
  }
}
