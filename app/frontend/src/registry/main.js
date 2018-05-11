// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'babel-polyfill'
import Vue from 'vue'
import Vuex from 'vuex'
import BootstrapVue from 'bootstrap-vue'
import Keycloak from 'keycloak-js'
import App from './App'
import router from './router'
import { store } from './store'
import { SET_KEYCLOAK } from '@/registry/store/mutations.types.js'
import '@/common/assets/css/bootstrap-theme.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import vueSmoothScroll from 'vue-smoothscroll'
import vSelect from 'vue-select'
import VueMoment from 'vue-moment'

// GWELLS js API library (helper methods for working with API)
import ApiService from '@/common/services/ApiService.js'

Vue.use(Vuex)
Vue.use(BootstrapVue)
Vue.use(vueSmoothScroll)
Vue.use(VueMoment)
Vue.component('v-select', vSelect)

// start Keycloak
Vue.prototype.$keycloak = Keycloak({
  'realm': 'gwells',
  'url': 'https://dev-sso.pathfinder.gov.bc.ca/auth',
  'clientId': 'webapp-dev-local'
})
Vue.config.productionTip = false

// set baseURL and default headers
ApiService.init()

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>',
  created () {
    this.$keycloak.init({ onLoad: 'check-sso' }).success(() => {
      store.commit(SET_KEYCLOAK, this.$keycloak)
      if (this.$keycloak.authenticated) {
        ApiService.authHeader('JWT', this.$keycloak.token)
      }
    })
  }
})
