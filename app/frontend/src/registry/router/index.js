import Vue from 'vue'
import Router from 'vue-router'
import AuthGuard from './authGuard'

import SearchHome from '@/registry/components/search/SearchHome.vue'

import PersonDetail from '@/registry/components/people/PersonDetail.vue'
import PersonEdit from '@/registry/components/people/PersonEdit.vue'
import PersonAdd from '@/registry/components/people/PersonAdd.vue'

import ApplicationDetail from '@/registry/components/people/ApplicationDetail.vue'

import OrganizationAdd from '@/registry/components/people/OrganizationAdd.vue'
import OrganizationEdit from '@/registry/components/people/OrganizationEdit.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/people/edit/:person_guid',
      name: 'PersonDetailEdit',
      component: PersonEdit,
      beforeEnter: AuthGuard,
      meta: {
        // list of required permissions (e.g. "edit: true" means user needs edit permission)
        edit: true
      }
    },
    {
      path: '/people/add',
      name: 'PersonAdd',
      component: PersonAdd,
      beforeEnter: AuthGuard,
      meta: {
        edit: true
      }
    },
    {
      path: '/people/:person_guid/registrations/:registration_guid/applications/:application_guid',
      name: 'ApplicationDetail',
      component: ApplicationDetail,
      beforeEnter: AuthGuard,
      meta: {
        view: true
      }
    },
    {
      path: '/people/:person_guid',
      name: 'PersonDetail',
      component: PersonDetail,
      beforeEnter: AuthGuard,
      meta: {
        view: true
      }
    },
    {
      path: '/organizations/manage',
      name: 'OrganizationEdit',
      component: OrganizationEdit,
      beforeEnter: AuthGuard,
      meta: {
        edit: true
      }
    },
    {
      path: '/organizations/add',
      name: 'OrganizationAdd',
      component: OrganizationAdd,
      beforeEnter: AuthGuard,
      meta: {
        edit: true
      }
    },
    {
      path: '/',
      name: 'SearchHome',
      component: SearchHome
    }
  ],
  mode: 'history',
  base: '/gwells/registries',
  scrollBehavior (to, from, savedPosition) {
    return { x: 0, y: 0 }
  }
})
