// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'babel-polyfill'
import Vue from 'vue'
import Vuex from 'vuex'
import { store } from '@/registry/store'
import BootstrapVue from 'bootstrap-vue'
import Header from '../common/components/Header'
import '@/common/assets/css/bootstrap-theme.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(Vuex)
Vue.use(BootstrapVue)
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#header',
  store,
  components: {
    Header
  },
  template: '<Header auth="hide"/>'
})

Vue.config.devtools = true
