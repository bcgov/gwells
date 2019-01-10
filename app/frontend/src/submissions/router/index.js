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
import Router from 'vue-router'
import { store } from '../store/index.js'
import authenticate from '@/common/authenticate.js'

import SubmissionsHome from '@/submissions/views/SubmissionsHome.vue'

Vue.use(Router)

const router = new Router({
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

router.beforeEach((to, from, next) => {
  authenticate.authenticate(store).then(() => {
    next()
  })
})

export default router
