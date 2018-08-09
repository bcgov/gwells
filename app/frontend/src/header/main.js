/*
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/
// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'babel-polyfill'
import Vue from 'vue'
import Vuex, {mapActions} from 'vuex'
import auth from '@/common/store/auth.js'
import config, {FETCH_CONFIG} from '@/common/store/config.js'
import BootstrapVue from 'bootstrap-vue'
import Header from '../common/components/Header'
import '@/common/assets/css/bootstrap-theme.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import ApiService from '@/common/services/ApiService.js'
import authenticate from '@/common/authenticate.js'

Vue.use(Vuex)
Vue.use(BootstrapVue)
Vue.config.productionTip = false

// Create a store instance with the common auth store module
const store = new Vuex.Store({
  modules: {
    auth: auth,
    config: config
  }
})

// set baseURL and default headers
ApiService.init()

/* eslint-disable no-new */
new Vue({
  el: '#header',
  store,
  components: {
    Header
  },
  template: '<Header/>',
  methods: {
    ...mapActions([
      FETCH_CONFIG
    ])
  },
  created () {
    // start Keycloak authentication
    authenticate.authenticate(store).then((result) => {
      // Auth complete. Do something here if you want.
    })
    this.FETCH_CONFIG()
  }
})

Vue.config.devtools = process.env.NODE_ENV !== 'production'
