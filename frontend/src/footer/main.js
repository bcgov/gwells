// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'babel-polyfill'
import Vue from 'vue'
import Vuex from 'vuex'
import BootstrapVue from 'bootstrap-vue'
import Footer from '../common/components/Footer'
// The footer does not import boostrap css, as it is assumed it's already imported by the header.

Vue.use(Vuex)
Vue.use(BootstrapVue)
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#footer',
  components: {
    Footer
  },
  template: '<Footer/>'
})

Vue.config.devtools = true
