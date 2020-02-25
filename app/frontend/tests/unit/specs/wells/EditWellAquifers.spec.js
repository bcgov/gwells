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
import { merge } from 'lodash'

import EditWellAquifers from '@/wells/views/EditWellAquifers.vue'
import auth from '@/common/store/auth.js'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('EditWellAquifers.vue', () => {
  const component = (options, storeState = {}) => {
    const store = new Vuex.Store({
      modules: { auth }
    })
    store.replaceState(merge(store.state, storeState))

    return shallowMount(EditWellAquifers, {
      localVue,
      store,
      mocks: {
        $router: {
          push: jest.fn(),
          replace: jest.fn()
        },
        $route: {
          path: '/well/1/aquifers',
          params: {
            wellTagNumber: 1
          }
        }
      },
      stubs: ['router-link', 'v-select'],
      methods: {
        fetchAquifersForWell () {
          this.aquifers = [
            { from: 50, to: 100, aquifer_id: 1, aquifer_name: 'Test Aquifer 1', lat: -123, lng: 50 },
            { from: 200, to: 300, aquifer_id: 2, aquifer_name: 'Test Aquifer 2', lat: -123, lng: 50 }
          ]
        }
      },
      ...options
    })
  }

  it('the page renders', () => {
    const wrapper = component()

    expect(wrapper.find('#page-title').text()).toBe('Well 1 Vertical Aquifer Extents')
  })

  it('matches the snapshot', () => {
    const wrapper = component({
      propsData: { edit: false }
    })

    expect(wrapper.element).toMatchSnapshot()
  })
})
