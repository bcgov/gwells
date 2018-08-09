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
import 'babel-polyfill'
import Vue from 'vue'
import Vuex, {mapActions} from 'vuex'
import BootstrapVue from 'bootstrap-vue'
import App from './App'
import router from './router'
import { store } from './store'
import '@/common/assets/css/bootstrap-theme.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import vSelect from 'vue-select'
import FormInput from '@/common/components/FormInput.vue'
import authenticate from '@/common/authenticate.js'
import {FETCH_CONFIG} from '@/common/store/config.js'

// GWELLS js API library (helper methods for working with API)
import ApiService from '@/common/services/ApiService.js'

Vue.use(Vuex)
Vue.use(BootstrapVue)
Vue.component('v-select', vSelect)
Vue.component('form-input', FormInput)

// set baseURL and default headers
ApiService.init()

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: {
    App
  },
  template: '<App/>',
  methods: {
    ...mapActions([
      FETCH_CONFIG
    ])
  },
  created () {
    // start Keycloak authentication
    authenticate.authenticate(store).then(() => {
      // Auth complete. Do something here if you want.
    })
    this.FETCH_CONFIG()
  }
})
