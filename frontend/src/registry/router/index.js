import Vue from 'vue'
import Router from 'vue-router'
import AuthEntry from './authEntry'
import AuthGuard from './authGuard'

import RegisterHome from '@/registry/components/RegisterHome'
import PersonDetail from '@/registry/components/PersonDetail'
import PersonApplicationDetail from '@/registry/components/PersonApplicationDetail'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'RegisterHome',
      component: RegisterHome,
      beforeEnter: AuthEntry
    },
    {
      path: '/people/:person_guid',
      name: 'PersonDetail',
      component: PersonDetail,
      beforeEnter: AuthGuard
    },
    {
      path: '/people/:person_guid/applications/:classCode',
      name: 'PersonApplicationDetail',
      component: PersonApplicationDetail,
      beforeEnter: AuthGuard
    }
  ]
})
