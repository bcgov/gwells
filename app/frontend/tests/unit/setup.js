import Vue from 'vue'
import PrimeVue from 'primevue/config';
import vSelect from 'vue-select'
import FormInput from '@/common/components/FormInput.vue'

Vue.use(PrimeVue)
Vue.component('v-select', vSelect)
Vue.component('form-input', FormInput)
Vue.config.productionTip = false
