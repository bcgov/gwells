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
import {mapActions, mapMutations} from 'vuex'
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import {FETCH_CONFIG} from '@/common/store/config.js'
import ApiService from '@/common/services/ApiService.js'
import authenticate from '@/common/authenticate.js'
import '@/common/assets/css/bootstrap-theme.min.css'

import App from './App'
import router from './router'
import store from './store'
import vueSmoothScroll from 'vue-smoothscroll'

ApiService.init()

Vue.use(BootstrapVue)
Vue.use(vueSmoothScroll)

/* eslint-disable no-new */
new Vue({
  components: { App },
  el: '#app',
  router,
  store,
  template: '<App/>',
  created () {
    authenticate.authenticate(store).then(() => {
      // Auth complete. Do something here if you want.
    })
    this.FETCH_CONFIG()
    this.fetchCodes()
  },
  methods: {
    ...mapMutations('aquiferCodes', ['addCodes']),
    ...mapActions([FETCH_CONFIG]),
    fetchCode (codePath, key) {
      ApiService.query(codePath).then((response) => {
        this.addCodes({key, codeTable: response.data.results})
      })
    },
    fetchCodes () {
      this.fetchCode('aquifer-codes/materials', 'material_codes')
      this.fetchCode('aquifer-codes/quality-concerns', 'quality_concern_codes')
      this.fetchCode('aquifer-codes/vulnerability', 'vulnerability_codes')
      this.fetchCode('aquifer-codes/subtypes', 'subtype_codes')
      this.fetchCode('aquifer-codes/productivity', 'productivity_codes')
      this.fetchCode('aquifer-codes/demand', 'demand_codes')
      this.fetchCode('aquifer-codes/water-use', 'known_water_use_codes')
    }
  }
})
