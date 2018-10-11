import Vue from 'vue'
import VueRouter from 'vue-router'

import Search from './components/Search'
import Retreive from './components/Retrieve'

Vue.use(VueRouter)

export default new VueRouter({
  routes: [
    {
      path: '/',
      component: Search
    },
    {
      path: '/:id',
      component: Retreive,
      props: true
    }
  ]
})
