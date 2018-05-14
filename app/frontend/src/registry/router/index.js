import Vue from 'vue'
import Router from 'vue-router'
import AuthGuard from './authGuard'

import SearchHome from '@/registry/components/search/SearchHome.vue'

import PersonDetail from '@/registry/components/people/PersonDetail.vue'
import PersonEdit from '@/registry/components/people/PersonEdit.vue'
import PersonAdd from '@/registry/components/people/PersonAdd.vue'

import ApplicationDetail from '@/registry/components/people/ApplicationDetail.vue'

import OrganizationAdd from '@/registry/components/people/OrganizationAdd.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/people/edit/:person_guid',
      name: 'PersonDetailEdit',
      component: PersonEdit,
      beforeEnter: AuthGuard,
      meta: {
        // these meta attributes are work in progress
        view: 'person',
        edit: 'person'
      }
    },
    {
      path: '/people/add',
      name: 'PersonAdd',
      component: PersonAdd,
      beforeEnter: AuthGuard,
      meta: {
        view: 'person',
        edit: 'person'
      }
    },
    {
      path: '/people/:person_guid/applications/:classCode',
      name: 'ApplicationDetail',
      component: ApplicationDetail,
      beforeEnter: AuthGuard,
      meta: {
        view: 'person'
      }
    },
    {
      path: '/people/:person_guid',
      name: 'PersonDetail',
      component: PersonDetail,
      beforeEnter: AuthGuard,
      meta: {
        view: 'person'
      }
    },
    {
      path: '/organizations/add',
      name: 'OrganizationAdd',
      component: OrganizationAdd,
      beforeEnter: AuthGuard,
      meta: {
        edit: 'organization'
      }
    },
    {
      path: '/',
      name: 'SearchHome',
      component: SearchHome
    }
  ],
  mode: 'history',
  base: process.env.APPLICATION_ROOT
})
