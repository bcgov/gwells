import Vue from 'vue'
import Router from 'vue-router'
import DrillerTable from '@/registry/components/DrillerTable'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'DrillerTable',
      component: DrillerTable
    }
  ]
})
