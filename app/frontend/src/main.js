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
import Vue from 'vue'
import * as Sentry from '@sentry/browser';
import * as Integrations from '@sentry/integrations';
import Vuex, { mapActions } from 'vuex'
import VueNoty from 'vuejs-noty'
import BootstrapVue from 'bootstrap-vue'
import VueAnalytics from 'vue-analytics'
import App from './App'
import router from './router.js'
import { store } from './store'
import '@/common/assets/css/bootstrap-theme.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import vueSmoothScroll from 'vue-smoothscroll'
import vSelect from 'vue-select'
import 'vue-select/dist/vue-select.css'
import VueMoment from 'vue-moment'
import FormInput from '@/common/components/FormInput.vue'
import { FETCH_CONFIG } from '@/common/store/config.js'

// GWELLS js API library (helper methods for working with API)
import ApiService from '@/common/services/ApiService.js'

// Sentry
Sentry.init({
  dsn: 'https://a83809da8c9b4f39b3d7cd683b803859@sentry.io/1802823',
  integrations: process.env.NODE_ENV === 'production' ? [new Integrations.Vue({Vue, attachProps: true, logError: true})] : []
});

Vue.use(Vuex)
Vue.use(VueNoty, {
  layout: 'topRight',
  theme: 'bootstrap-v4',
  timeout: 1800
})
Vue.use(BootstrapVue)
Vue.use(VueMoment)
Vue.use(vueSmoothScroll)
Vue.component('v-select', vSelect)
Vue.component('form-input', FormInput)

// set baseURL and default headers
ApiService.init()

Vue.use(VueAnalytics, {
  id: 'UA-106174915-1',
  set: [
    { field: 'anonymizeIp', value: true }
  ],
  disabled: ApiService.query('analytics', {}).then((response) => {
    return response.data.enable_google_analytics !== true
  })
})

Vue.config.productionTip = false
Vue.config.devtools = process.env.NODE_ENV !== 'production'
Vue.config.performance = process.env.NODE_ENV !== 'production'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>',
  methods: {
    ...mapActions([
      FETCH_CONFIG
    ])
  },
  created () {
    this.FETCH_CONFIG()
    this.$ga.page()
  }
})
