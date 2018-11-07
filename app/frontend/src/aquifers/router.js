/*
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/

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
