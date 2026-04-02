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
import "@/common/helpers/browserUpdate.js";
import { createApp } from "vue";
import * as Sentry from "@sentry/browser";
import * as Integrations from "@sentry/integrations";
import VueNoty from "vuejs-noty";
import BootstrapVue from "bootstrap-vue";
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
import VueMatomo from "vue-matomo";
import App from "./App.vue";
import router from "./router.js";
import "@/common/assets/css/bootstrap-theme.min.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";
import VueMoment from "vue-moment";
import FormInput from "@/common/components/FormInput.vue";
import * as filters from "./common/filters";
// GWELLS js API library (helper methods for working with API)
import ApiService from "@/common/services/ApiService.js";
import authenticate from "@/common/authenticate.js";
import { createPinia } from "pinia";

const PRODUCTION_GWELLS_URL = "https://apps.nrs.gov.bc.ca/gwells";
const STAGING_GWELLS_URLS = [
  "testapps.nrs.gov.bc.ca",
  "gwells-staging.apps.silver.devops.gov.bc.ca",
];
const BASE_PATH = "/gwells/";
const PRODUCTION_MATOMO_HOST =
  "https://water-matomo.apps.silver.devops.gov.bc.ca";
const TEST_MATOMO_HOST =
  "https://water-matomo-staging.apps.silver.devops.gov.bc.ca";

const PRODUCTION_GWELLS_HOST = new URL(PRODUCTION_GWELLS_URL).hostname;
const isProduction = () =>
  window.location.hostname === PRODUCTION_GWELLS_HOST &&
  window.location.pathname.startsWith(BASE_PATH);
const isStaging = () =>
  window.location.pathname.includes(BASE_PATH) &&
  STAGING_GWELLS_URLS.includes(window.location.hostname);

// set baseURL and default headers
ApiService.init();

const app = createApp(App);
authenticate.setApp(app);

// Initialize Sentry
if (isProduction()) {
  Sentry.init({
    dsn: "https://a83809da8c9b4f39b3d7cd683b803859@sentry.io/1802823",
    integrations: [
      new Integrations.Vue({ app, attachProps: true, logError: true }),
    ],
    beforeSend(event) {
      if (window.msCrypto) {
        return null;
      }
      return event;
    },
  });
}

app.use(router);
app.use(VueNoty, {
  layout: "topRight",
  theme: "bootstrap-v4",
  timeout: 1800,
});
app.use(BootstrapVue);
app.use(PrimeVue, {
  theme: {
    preset: Aura
  }
});
app.use(VueMoment);

// Register global components
app.component("v-select", vSelect);
app.component("form-input", FormInput);

const pinia = createPinia();
app.use(pinia);

if (isProduction()) {
  app.use(VueMatomo, {
    host: PRODUCTION_MATOMO_HOST,
    siteId: 2,
    router: router,
    domains: "apps.nrs.gov.bc.ca",
  });
} else if (isStaging()) {
  app.use(VueMatomo, {
    host: TEST_MATOMO_HOST,
    siteId: 1,
    router: router,
    domains: STAGING_GWELLS_URLS,
  });
} else {
  // Local & DEV and anything else
  app.use(VueMatomo, {
    host: TEST_MATOMO_HOST,
    siteId: 3,
    router: router,
  });
}

app.config.productionTip = false;
app.config.devtools = import.meta.env.MODE !== "production";
app.config.performance = import.meta.env.MODE !== "production";

app.config.globalProperties.excludeZeroDecimals = filters.excludeZeroDecimals;
app.config.globalProperties.nullBooleanToYesNo = filters.nullBooleanToYesNo;
app.config.globalProperties.booleanToYesNo = filters.booleanToYesNo;

// Mount app
app.mount("#app");
