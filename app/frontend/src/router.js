import Vue from 'vue'
import Router from 'vue-router'
import * as Sentry from '@sentry/browser'

import authenticate from '@/common/authenticate.js'
import AuthGuard from './authGuard'
import { store } from './store/index.js'

// Aquifers components
import AquiferSearch from '@/aquifers/components/Search'
import AquiferView from '@/aquifers/components/View'
import AquiferNew from '@/aquifers/components/New'
import BulkHome from '@/bulk/components/BulkHome.vue'
import BulkWellAquiferCorrelation from '@/bulk/components/BulkWellAquiferCorrelation.vue'
import BulkWellDocuments from '@/bulk/components/BulkWellDocuments.vue'
import BulkAquiferDocuments from '@/bulk/components/BulkAquiferDocuments.vue'
import BulkVerticalAquiferExtents from '@/bulk/components/BulkVerticalAquiferExtents.vue'

import WellSearch from '@/wells/views/WellSearch.vue'
import WellDetail from '@/wells/views/WellDetail.vue'
import EditWellAquifers from '@/wells/views/EditWellAquifers.vue'
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
import SubmissionDetail from '@/submissions/views/SubmissionDetail.vue'

// Common components
import PageNotFound from '@/common/components/PageNotFound.vue'

// Surveys
import Surveys from '@/surveys/views/Surveys.vue'

Vue.use(Router)

const router = new Router({
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
      name: 'aquifers-view'
    },
    {
      path: '/aquifers/:id/edit',
      component: AquiferView,
      name: 'aquifers-edit',
      beforeEnter: AuthGuard,
      props: { edit: true },
      meta: {
        edit: true,
        app: 'aquifers'
      }
    },
    {
      path: '/bulk/',
      component: BulkHome,
      name: 'bulk-home'
    },
    {
      path: '/bulk/well-aquifer-correlation',
      component: BulkWellAquiferCorrelation,
      name: 'bulk-well-aquifer-correlation'
    },
    {
      path: '/bulk/well-documents',
      component: BulkWellDocuments,
      name: 'bulk-well-documents'
    },
    {
      path: '/bulk/aquifer-documents',
      component: BulkAquiferDocuments,
      name: 'bulk-aquifer-documents'
    },
    {
      path: '/bulk/vertical-aquifer-extents',
      component: BulkVerticalAquiferExtents,
      name: 'bulk-vertical-aquifer-extents'
    },
    {
      path: '/new',
      component: AquiferNew,
      name: 'new',
      meta: {
        edit: true,
        app: 'aquifers'
      }
    },

    // Submissions routes
    {
      path: '/submissions/:id/edit',
      name: 'SubmissionsEdit',
      component: SubmissionsHome,
      meta: {
        edit: true,
        app: 'submissions'
      }
    },
    {
      path: '/submissions/:id/submissions/:submissionId',
      name: 'SubmissionDetail',
      component: SubmissionDetail,
      meta: {
        edit: true
      }
    },
    {
      path: '/submissions/',
      name: 'SubmissionsHome',
      component: SubmissionsHome,
      meta: {
        edit: true,
        app: 'submissions'
      }
    },

    // Registries routes
    {
      path: '/registries/people/edit/:person_guid',
      name: 'PersonDetailEdit',
      component: PersonEdit,
      beforeEnter: AuthGuard,
      meta: {
        // list of required permissions (e.g. "edit: true" means user needs edit permission)
        edit: true,
        app: 'registry'
      }
    },
    {
      path: '/registries/people/add',
      name: 'PersonAdd',
      component: PersonAdd,
      beforeEnter: AuthGuard,
      meta: {
        edit: true,
        app: 'registry'
      }
    },
    {
      path: '/registries/people/:person_guid/registrations/:registration_guid/applications/:application_guid',
      name: 'ApplicationDetail',
      component: ApplicationDetail,
      beforeEnter: AuthGuard,
      meta: {
        view: true,
        app: 'registry'
      }
    },
    {
      path: '/registries/people/:person_guid',
      name: 'PersonDetail',
      component: PersonDetail,
      beforeEnter: AuthGuard,
      meta: {
        view: true,
        app: 'registry'
      }
    },
    {
      path: '/registries/organizations/manage',
      name: 'OrganizationEdit',
      component: OrganizationEdit,
      beforeEnter: AuthGuard,
      meta: {
        edit: true,
        app: 'registry'
      }
    },
    {
      path: '/registries/organizations/add',
      name: 'OrganizationAdd',
      component: OrganizationAdd,
      beforeEnter: AuthGuard,
      meta: {
        edit: true,
        app: 'registry'
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
      path: '/well/:id',
      name: 'wells-detail',
      component: WellDetail
    },
    {
      path: '/well/:wellTagNumber/aquifers',
      name: 'well-aquifers',
      component: EditWellAquifers,
      beforeEnter: AuthGuard,
      meta: {
        edit: true,
        app: 'aquifers'
      }
    },
    {
      path: '/surveys',
      name: 'Surveys',
      component: Surveys,
      beforeEnter: AuthGuard,
      meta: {
        edit: true,
        app: 'surveys'
      }
    },
    { path: '/search', redirect: '/' },
    {
      path: '/',
      name: 'wells-home',
      component: WellSearch
    },
    {
      path: '*',
      name: 'page-not-found',
      component: PageNotFound
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
    if (to.name !== from.name) {
      return { x: 0, y: 0 }
    }
  }
})

router.beforeEach((to, from, next) => {
  if (!router.app.$keycloak) {
    authenticate.authenticate(store).then((keycloak) => {
      if (keycloak.authenticated) {
        Sentry.setUser({ username: keycloak.tokenParsed.preferred_username })
      }

      next()
    }).catch((e) => {
      next({ name: 'wells-home' })
    })
  } else {
    next()
  }
})

export default router
