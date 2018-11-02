import Vue from 'vue'
import VueRouter from 'vue-router'

import Search from './components/Search'
import View from './components/View'
import New from './components/New'

Vue.use(VueRouter)

export default new VueRouter({
  base: '/gwells/aquifers',
  mode: 'history',
  routes: [
    {
      path: '/',
      component: Search,
      name: 'home'
    },
    {
      path: '/:id(\\d+)',
      component: View,
      name: 'view'
    },
    {
      path: '/:id/edit',
      component: View,
      name: 'edit',
      props: { edit: true }
    },
    {
      path: '/new',
      component: New,
      name: 'new'
    }
  ]
})
