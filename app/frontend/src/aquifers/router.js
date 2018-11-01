import Vue from 'vue'
import VueRouter from 'vue-router'

import Search from './components/Search'
import View from './components/View'
import Edit from './components/Edit'

Vue.use(VueRouter)

export default new VueRouter({
  base: '/gwells/aquifers',
  mode: 'history',
  routes: [
    {
      path: '/',
      component: Search
    },
    {
      path: '/:id(\\d+)',
      component: View,
      name: 'view',
      props: true
    },
    {
      path: '/:id/edit',
      component: Edit,
      name: 'edit',
      props: true
    }
  ]
})
