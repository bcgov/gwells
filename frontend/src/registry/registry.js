// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuex from 'vuex'
// import BootstrapVue from 'bootstrap-vue'
import App from './App'
// import App from './AppBS4'
import router from './router'
import { store } from './store'
// import 'bootstrap/dist/css/bootstrap.min.css'
// import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'babel-polyfill'

// GWELLS js API library (helper methods for working with API)
import ApiService from '@/common/services/gwells'

Vue.use(Vuex)
Vue.config.productionTip = false

// set baseURL and default headers
ApiService.init()

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
