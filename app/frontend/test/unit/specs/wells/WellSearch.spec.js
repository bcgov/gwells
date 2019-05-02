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
import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import WellSearch from '@/wells/views/WellSearch.vue'

import {FETCH_CODES} from '@/submissions/store/actions.types.js'
import {FETCH_DRILLER_NAMES, FETCH_ORGANIZATION_NAMES} from '@/wells/store/actions.types.js'
import {SET_SEARCH_PARAMS} from '@/wells/store/mutations.types.js'

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(VueRouter)

const router = new VueRouter()

describe('WellSearch.vue', () => {
  let store
  let getters
  let mutations
  let actions

  beforeEach(() => {
    getters = {
      codes: () => ({}),
      drillerNames: () => ({}),
      locationErrorMessage: () => ({}),
      organizationNames: () => ({}),
      searchLimit: () => ({}),
      searchErrors: () => ({}),
      searchOffset: () => ({}),
      searchOrdering: () => ({}),
      searchParams: () => ({}),
      searchResultColumns: () => ({}),
      searchResults: () => ({}),
      userRoles: () => ({ wells: { view: false } })
    }
    mutations = {
      [SET_SEARCH_PARAMS]: jest.fn()
    }
    actions = {
      [FETCH_CODES]: jest.fn(),
      [FETCH_DRILLER_NAMES]: jest.fn(),
      [FETCH_ORGANIZATION_NAMES]: jest.fn()
    }
    store = new Vuex.Store({
      getters,
      mutations,
      actions
    })
  })

  it('the page renders', () => {
    const wrapper = shallowMount(WellSearch, {
      localVue,
      store,
      router,
      stubs: ['router-link', 'search-form-select', 'b-popover'],
      sync: false
    })

    expect(wrapper.find('#wellSearchTitle').text()).toBe('Well Search')
  })
})
