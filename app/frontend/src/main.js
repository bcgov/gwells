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
import '@/common/helpers/browserUpdate.js'
import Vue from 'vue'
import * as Sentry from '@sentry/browser'
import * as Integrations from '@sentry/integrations'
import Vuex, { mapActions } from 'vuex'
import VueNoty from 'vuejs-noty'
import BootstrapVue from 'bootstrap-vue'
import VueMatomo from 'vue-matomo'
import App from './App.vue'
import router from './router.js'
import { store } from './store/index.js'
import '@/common/assets/css/bootstrap-theme.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import vSelect from 'vue-select'
import 'vue-select/dist/vue-select.css'
import VueMoment from 'vue-moment'
import FormInput from '@/common/components/FormInput.vue'
import { FETCH_CONFIG } from '@/common/store/config.js'
<<<<<<< HEAD
import * as filters from './common/filters'
=======
import filters from '@/common/filters'
// Test
>>>>>>> c01a09134 (Test commit)
// GWELLS js API library (helper methods for working with API)
import ApiService from '@/common/services/ApiService.js'

const PRODUCTION_GWELLS_URL = 'https://apps.nrs.gov.bc.ca/gwells'
const STAGING_GWELLS_URLS = ['testapps.nrs.gov.bc.ca', 'gwells-staging.apps.silver.devops.gov.bc.ca']
const BASE_PATH = '/gwells/'
const PRODUCTION_MATOMO_HOST = 'https://water-matomo.apps.silver.devops.gov.bc.ca/'
const TEST_MATOMO_HOST = 'https://water-matomo-staging.apps.silver.devops.gov.bc.ca/'

const isProduction = () => (window.location.href.includes(PRODUCTION_GWELLS_URL))
const isStaging = () => (
  window.location.pathname.includes(BASE_PATH) && STAGING_GWELLS_URLS.includes(window.location.hostname)
)
if (isProduction()) {
  Sentry.init({
    dsn: 'https://a83809da8c9b4f39b3d7cd683b803859@sentry.io/1802823',
    integrations: [new Integrations.Vue({ Vue, attachProps: true, logError: true })],
    beforeSend (event) {
      if (window.msCrypto) { return null }
      return event
    }
  })
}

Vue.use(Vuex)
Vue.use(VueNoty, {
  layout: 'topRight',
  theme: 'bootstrap-v4',
  timeout: 1800
})
Vue.use(BootstrapVue)
Vue.use(VueMoment)
Vue.use(filters)
Vue.component('v-select', vSelect)
Vue.component('form-input', FormInput)

// set baseURL and default headers
ApiService.init()

if (isProduction()) {
  Vue.use(VueMatomo, {
    host: PRODUCTION_MATOMO_HOST,
    siteId: 2,
    router: router,
    domains: 'apps.nrs.gov.bc.ca'
  })
} else if (isStaging()) {
  Vue.use(VueMatomo, {
    host: TEST_MATOMO_HOST,
    siteId: 1,
    router: router,
    domains: STAGING_GWELLS_URLS
  })
} else { // Local & DEV and anything else
  Vue.use(VueMatomo, {
    host: TEST_MATOMO_HOST,
    siteId: 3,
    router: router
  })
}

Vue.config.productionTip = false
Vue.config.devtools = import.meta.env.MODE !== 'production'
Vue.config.performance = import.meta.env.MODE !== 'production'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App), // Replace components/template with render function
  methods: {
    ...mapActions([
      FETCH_CONFIG
    ])
  },
  created () {
    this.FETCH_CONFIG()
    window._paq.push(['trackPageView']) // To track pageview - Matomo
  }
})

// new Vue({
//   el: '#app',
//   router,
//   store,
//   components: { App },
//   template: '<App/>',
//   methods: {
//     ...mapActions([
//       FETCH_CONFIG
//     ])
//   },
//   created () {
//     this.FETCH_CONFIG()
//     window._paq.push(['trackPageView']) // To track pageview - Matomo
//   }
// })
