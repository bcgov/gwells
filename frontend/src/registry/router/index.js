import Vue from 'vue'
import Router from 'vue-router'
import RegisterHome from '@/registry/components/RegisterHome'
import PersonDetail from '@/registry/components/PersonDetail'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'RegisterHome',
      component: RegisterHome
    },
    {
      path: '/people/:person_guid',
      name: 'PersonDetail',
      component: PersonDetail
    }
  ]
})
