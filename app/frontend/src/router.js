import Vue from 'vue'
import Router from 'vue-router'
import AuthGuard from './authGuard'

// Aquifers components
import AquiferSearch from '@/aquifers/components/Search'
import AquiferView from '@/aquifers/components/View'
import AquiferEdit from '@/aquifers/components/Edit'

import WellSearch from '@/wells/views/WellSearch.vue'
import GroundwaterInformation from '@/wells/views/GroundwaterInformation.vue'

// Registries components
import SearchHome from '@/registry/components/search/SearchHome.vue'
import PersonDetail from '@/registry/components/people/PersonDetail.vue'
import PersonEdit from '@/registry/components/people/PersonEdit.vue'
import PersonAdd from '@/registry/components/people/PersonAdd.vue'
import ApplicationDetail from '@/registry/components/people/ApplicationDetail.vue'
import OrganizationAdd from '@/registry/components/people/OrganizationAdd.vue'
import OrganizationEdit from '@/registry/components/people/OrganizationEdit.vue'

// Submissions components
import SubmissionsHome from '@/submissions/views/SubmissionsHome.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: '/gwells/',
  routes: [
    // aquifers routes
    {
      path: '/aquifers/',
      name: 'aquifers-home',
      component: AquiferSearch
    },
    {
      path: '/aquifers/:id(\\d+)',
      component: AquiferView,
      name: 'aquifers-view',
      props: true
    },
    {
      path: '/aquifers/:id/edit',
      component: AquiferEdit,
      name: 'aquifers-edit',
      props: true
    },

    // Submissions routes
    {
      path: '/submissions/:id/edit',
      name: 'SubmissionsEdit',
      component: SubmissionsHome
    },
    {
      path: '/submissions/',
      name: 'SubmissionsHome',
      component: SubmissionsHome
    },

    // Registries routes
    {
      path: '/registries/people/edit/:person_guid',
      name: 'PersonDetailEdit',
      component: PersonEdit,
      beforeEnter: AuthGuard,
      meta: {
        // list of required permissions (e.g. "edit: true" means user needs edit permission)
        edit: true
      }
    },
    {
      path: '/registries/people/add',
      name: 'PersonAdd',
      component: PersonAdd,
      beforeEnter: AuthGuard,
      meta: {
        edit: true
      }
    },
    {
      path: '/registries/people/:person_guid/registrations/:registration_guid/applications/:application_guid',
      name: 'ApplicationDetail',
      component: ApplicationDetail,
      beforeEnter: AuthGuard,
      meta: {
        view: true
      }
    },
    {
      path: '/registries/people/:person_guid',
      name: 'PersonDetail',
      component: PersonDetail,
      beforeEnter: AuthGuard,
      meta: {
        view: true
      }
    },
    {
      path: '/registries/organizations/manage',
      name: 'OrganizationEdit',
      component: OrganizationEdit,
      beforeEnter: AuthGuard,
      meta: {
        edit: true
      }
    },
    {
      path: '/registries/organizations/add',
      name: 'OrganizationAdd',
      component: OrganizationAdd,
      beforeEnter: AuthGuard,
      meta: {
        edit: true
      }
    },
    {
      path: '/registries/',
      name: 'SearchHome',
      component: SearchHome
    },
    // Wells routes
    {
      path: '/groundwater-information',
      name: 'groundwater-information',
      component: GroundwaterInformation
    },
    {
      path: '/',
      name: 'wells-home',
      component: WellSearch
    }

    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
    // }
  ],
  scrollBehavior (to, from, savedPosition) {
    return { x: 0, y: 0 }
  }
})
