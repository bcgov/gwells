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
import { LngLatBounds } from 'mapbox-gl'
import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import { merge } from 'lodash'

import WellSearch from '@/wells/views/WellSearch.vue'
import auth from '@/common/store/auth.js'
import wellsStore from '@/wells/store/index.js'
import documentState from '@/common/store/documents.js'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('WellSearch.vue', () => {
  const component = (options, storeState = {}) => {
    const store = new Vuex.Store({
      modules: { auth, wellsStore, documentState }
    })
    store.replaceState(merge(store.state, storeState))

    return shallowMount(WellSearch, {
      localVue,
      store,
      mocks: {
        $router: {
          push: jest.fn(),
          replace: jest.fn()
        },
        $route: {
          path: '/',
          query: {}
        }
      },
      stubs: ['router-link', 'b-popover'],
      methods: {
        fetchSurveys: jest.fn()
      },
      ...options
    })
  }

  it('the page renders', () => {
    const wrapper = component()

    expect(wrapper.find('#wellSearchTitle').text()).toBe('Well Search')
  })

  it('should build query params', () => {
    const searchParams = {
      search: 'abc'
    }
    const storeState = {
      wellsStore: {
        searchParams
      }
    }
    const wrapper = component({ mocks: {
      $router: {
        replace: jest.fn()
      },
      $route: {
        path: '/',
        query: searchParams
      }
    } }, storeState)

    const queryParams = wrapper.vm.buildQueryParams()

    expect(queryParams).toEqual({
      limit: '10',
      offset: '0',
      ordering: '-well_tag_number',
      result_columns: 'wellTagNumber,identificationPlateNumber,ownerName,streetAddress,legalLot,legalPlan,legalDistrictLot,landDistrict,legalPid,diameter,finishedWellDepth',
      search: 'abc'
    })
  })

  it('Should replace the URL qs on map search', () => {
    const searchParams = {
      search: 'abc'
    }
    const storeState = {
      wellsStore: {
        searchParams
      }
    }
    const routerReplaceSpy = jest.fn()
    const wrapper = component({ mocks: {
      $router: {
        replace: routerReplaceSpy
      },
      $route: {
        path: '/',
        query: searchParams
      }
    } }, storeState)

    wrapper.vm.handleMapSearch(new LngLatBounds())

    expect(wrapper.vm.searchParams).toEqual(searchParams)
    expect(routerReplaceSpy).toHaveBeenCalled()
  })
})
