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
import Vuex from 'vuex'
import auth from '@/common/store/auth.js'
import config from '@/common/store/config.js'
import BootstrapVue from 'bootstrap-vue'
import Summary from './components/Summary'
import '@/common/assets/css/bootstrap-theme.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

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

/* eslint-disable no-new */
new Vue({
  el: '#summary',
  store,
  components: {
    Summary
  },
  template: '<Summary/>'
})

Vue.config.devtools = process.env.NODE_ENV !== 'production'
