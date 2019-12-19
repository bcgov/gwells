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

import { mount, createLocalVue } from '@vue/test-utils'
import SearchComponent from '@/aquifers/components/Search.vue'
import Vuex from 'vuex'
import axios from 'axios'
import VueRouter from 'vue-router'
import auth from '@/common/store/auth.js'
import aquiferStore from '@/aquifers/store/index.js'

jest.mock('axios')

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(VueRouter)

const aquiferFixture = {
  aquifer_id: '4',
  aquifer_name: 'Aggasiz',
  location_description: 'Aggasiz/Sea Bird Island',
  material_description: 'Sand and Gravel',
  litho_stratographic_unit: 'Fraser River Sediments',
  subtype_description: 'Unconfined sand and gravel - large river system',
  vulnerability_description: 'High',
  area: '63.3',
  productivity_description: 'High',
  demand: 'Low',
  mapping_year: '1993',
  resources: []
}

describe('Search Component', () => {
  const component = options =>
    mount(SearchComponent, {
      localVue,
      stubs: ['router-link', 'router-view'],
      router: new VueRouter(),
      store: new Vuex.Store({
        modules: { auth, aquiferStore }
      }),
      methods: {
        scrollToTableTop () {},
        fetchResourceSections () {
          this.aquifer_resource_sections = [
            { text: 'aquifer section', value: 'a' }
          ]
        },
        $SmoothScroll () {}
      },
      ...options
    })

  it('has child checkboxes', () => {
    axios.get.mockResolvedValue({})

    expect(component({}).findAll('[type="checkbox"]').length).toEqual(1)
  })

  it('Displays a message if no aquifers could be found', () => {
    axios.get.mockResolvedValue({})
    const wrapper = component({
      data () {
        return {
          searchResults: [],
          performedSearch: true,
          loadingMap: false
        }
      },
      computed: {
        emptyResults () {
          return true
        }
      },
      methods: {
        fetchResults () {}
      }
    })

    expect(wrapper.text()).toContain('No aquifers could be found')
  })

  it('Matches the snapshot', () => {
    axios.get.mockResolvedValue({})

    const wrapper = component({
      data () {
        return {
          searchResults: [aquiferFixture],
          performedSearch: true,
          loadingMap: false
        }
      },
      computed: {
        emptyResults () {
          return false
        },
        displayPageLength () {
          return 0
        }
      },
      methods: {
        fetchResults () {}
      }
    })

    expect(wrapper.element).toMatchSnapshot()
  })

  it('search updates route query params', () => {
    axios.get.mockResolvedValue({})

    const wrapper = component()

    wrapper.find('#aquifers-search-field').setValue('asdf')

    wrapper.find('input[type="checkbox"]').setChecked()
    wrapper.find('form').trigger('submit')

    expect(axios.get).toHaveBeenCalledWith('aquifers', {
      params: { resources__section__code: 'a', match_any: false, search: 'asdf' }
    })
  })

  it('form reset resets response and query', () => {
    const wrapper = component()
    axios.get.mockResolvedValue({})

    wrapper.find('#aquifers-search-field').setValue('asdf')
    wrapper.find('form').trigger('submit')

    expect(wrapper.vm.query.search).toEqual('asdf')

    wrapper.find('form').trigger('reset')

    expect(wrapper.vm.query.search).toEqual(undefined)
  })
})
