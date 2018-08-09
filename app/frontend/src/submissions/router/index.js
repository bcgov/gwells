import Vue from 'vue'
import Router from 'vue-router'

import SubmissionsHome from '@/submissions/views/SubmissionsHome.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/:id/edit',
      name: 'SubmissionsEdit',
      component: SubmissionsHome,
      meta: {
        edit: true // requires wells/edit permission. note: beforeEnter guard not implemented yet
      }
    },
    {
      path: '/',
      name: 'SubmissionsHome',
      component: SubmissionsHome
    }
  ],
  mode: 'history',
  base: '/gwells/submissions',
  scrollBehavior (to, from, savedPosition) {
    return { x: 0, y: 0 }
  }
})
