import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import vSelect from 'vue-select'
import FormInput from '@/common/components/FormInput.vue'

Vue.use(BootstrapVue)
Vue.component('v-select', vSelect)
Vue.component('form-input', FormInput)
Vue.config.productionTip = false
