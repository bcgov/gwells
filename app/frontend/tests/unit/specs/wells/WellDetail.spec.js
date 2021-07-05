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
import '../../mocks/mapbox-gl'
import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import { merge } from 'lodash'

import WellDetail from '@/wells/views/WellDetail.vue'
import auth from '@/common/store/auth.js'
import wellsStore from '@/wells/store/index.js'
import documentState from '@/common/store/documents.js'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('WellDetail.vue', () => {
  const id = 113169
  const getters = {
    config: () => {}
  }
  const component = (options, storeState = {}) => {
    const store = new Vuex.Store({
      getters,
      modules: { auth, wellsStore, documentState }
    })
    store.replaceState(merge(store.state, storeState))

    return shallowMount(WellDetail, {
      localVue,
      store,
      mocks: {
        $router: {
          push: jest.fn(),
          replace: jest.fn()
        },
        $route: {
          path: `/well/${id}`,
          query: {
            id: id
          }
        }
      },
      stubs: ['router-link'],
      methods: {
        fetchWellData: jest.fn()
      },
      filters: {
        excludeZeroDecimals: jest.fn()
      },
      computed: {
        id () {
          return id
        }
      },
      ...options
    })
  }

  it('the page renders', () => {
    const wrapper = component()
    expect(wrapper.find('#summary_fieldset > legend > span').text()).toBe('Well Summary')
  })

  it('should match snapshot', () => {
    const wrapper = component()
    expect(wrapper.element).toMatchSnapshot()
  })
})
