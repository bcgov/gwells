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
import App from './App'
import BootstrapVue from 'bootstrap-vue'
import '@/common/assets/css/bootstrap-theme.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from './router'
import store from './store'
import ApiService from '@/common/services/ApiService.js'

ApiService.init()

Vue.use(BootstrapVue)

/* eslint-disable no-new */
new Vue({
  components: { App },
  el: '#app',
  router,
  store,
  template: '<App/>'
})
