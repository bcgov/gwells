import Vue from 'vue'
import Router from 'vue-router'
import AuthGuard from './authGuard'

import SearchHome from '@/registry/components/search/SearchHome.vue'
import PersonDetail from '@/registry/components/people/PersonDetail.vue'
import ApplicationDetail from '@/registry/components/people/ApplicationDetail.vue'
import PersonEdit from '@/registry/components/people/PersonEdit.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/people/edit/:person_guid',
      name: 'PersonDetailEdit',
      component: PersonEdit,
      beforeEnter: AuthGuard
    },
    {
      path: '/people/:person_guid/applications/:classCode',
      name: 'ApplicationDetail',
      component: ApplicationDetail,
      beforeEnter: AuthGuard
    },
    {
      path: '/people/:person_guid',
      name: 'PersonDetail',
      component: PersonDetail,
      beforeEnter: AuthGuard
    },
    {
      path: '/',
      name: 'SearchHome',
      component: SearchHome
    }
  ],
  mode: 'history',
  base: process.env.NODE_ENV === 'production' ? '/gwells/registries/' : '/'
})
