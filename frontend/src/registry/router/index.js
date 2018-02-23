import Vue from 'vue'
import Router from 'vue-router'
import RegisterHome from '@/registry/components/RegisterHome'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'RegisterHome',
      component: RegisterHome
    }
  ]
})
