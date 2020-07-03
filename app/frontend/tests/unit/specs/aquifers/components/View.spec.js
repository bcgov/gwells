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

/* eslint-disable import/first */

import '../../../mocks/mapbox-gl'
import { mount, createLocalVue } from '@vue/test-utils'
import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import { cloneDeep, merge, omit } from 'lodash'

import auth from '@/common/store/auth.js'
import aquiferStore from '@/aquifers/store/index.js'
import documentState from '@/common/store/documents.js'
import ViewComponent from '@/aquifers/components/View.vue'

jest.mock('axios')

const localVue = createLocalVue()
localVue.use(Vuex)

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
  resources: [],
  licence_details: {
    licence_count: 4,
    licences_updated: {
      update_date__max: '2019-11-04T19:47:48.075000Z'
    },
    num_wells_with_ems: 3,
    num_artesian_wells: 4,
    wells_updated: {
      update_date__max: '2016-02-09T21:55:31Z'
    },
    num_wells: 4,
    obs_wells: [{
      well_tag_number: 117042,
      observation_well_number: '2',
      observation_well_status: 'Active'
    }, {
      well_tag_number: 100125,
      observation_well_number: '2',
      observation_well_status: 'Active'
    }],
    wells_by_licence: [{
      licence_number: 501525,
      well_tag_numbers_in_licence: [117041]
    }, {
      licence_number: 501526,
      well_tag_numbers_in_licence: [117043]
    }, {
      licence_number: 501527,
      well_tag_numbers_in_licence: [117044]
    }, {
      licence_number: 501528,
      well_tag_numbers_in_licence: [117045]
    }],
    usage: [{
      purpose__description: '03A - Irrigation: Local Provider ',
      total_qty: 2730000.0
    }, {
      purpose__description: 'WSA09 - Processing & Manufacturing ',
      total_qty: 980000.0
    }, {
      purpose__description: '03B - Irrigation: Private ',
      total_qty: 6850000.0
    }],
    lic_qty: [{
      purpose__description: '03A - Irrigation: Local Provider ',
      total_qty: 1
    }, {
      purpose__description: 'WSA09 - Processing & Manufacturing ',
      total_qty: 1
    }, {
      purpose__description: '03B - Irrigation: Private ',
      total_qty: 2
    }],
    hydraulically_connected: true
  }
}

describe('View Component', () => {
  let fetch = null

  const component = (options, storeState = {}) => {
    const store = new Vuex.Store({
      modules: { auth, aquiferStore, documentState }
    })
    store.replaceState(merge(cloneDeep(store.state), cloneDeep(storeState)))

    return mount(ViewComponent, {
      localVue,
      store,
      mocks: {
        $router: {
          push: jest.fn(),
          replace: jest.fn()
        },
        $route: {
          path: `/aquifers/${aquiferFixture.aquifer_id}`,
          params: {
            id: aquiferFixture.aquifer_id
          }
        }
      },
      stubs: ['router-link', 'aquifer-documents', 'aquifer-form', 'b-popover', 'pie-chart', 'single-aquifer-map'],
      methods: {
        fetch,
        fetchAquifer: jest.fn(),
        fetchWells: jest.fn(),
        fetchFiles: jest.fn(),
        navigateToView: jest.fn()
      },
      ...options
    })
  }

  beforeEach(() => {
    fetch = jest.fn()
    axios.get.mockResolvedValue({})
  })

  it('queries aquifer on load', async () => {
    component()

    await Vue.nextTick()

    expect(fetch).toHaveBeenCalled()
  })

  describe('View mode', () => {
    it('matches the snapshot', () => {
      const wrapper = component({
        propsData: { edit: false }
      }, {
        aquiferStore: {
          view: {
            record: aquiferFixture
          }
        }
      })

      expect(wrapper.element).toMatchSnapshot()
    })
  })

  describe('Edit mode', () => {
    it('matches the snapshot', () => {
      const wrapper = component({
        propsData: { edit: true }
      }, {
        aquiferStore: {
          view: {
            record: aquiferFixture
          }
        }
      })

      expect(wrapper.element).toMatchSnapshot()
    })

    describe('On save', () => {
      it('resets showSaveSuccess to false', () => {
        const wrapper = component({
          data () {
            return {
              showSaveSuccess: true
            }
          }
        }, {
          aquiferStore: {
            view: {
              record: aquiferFixture
            }
          }
        })

        axios.patch.mockResolvedValue(true)

        expect(wrapper.vm.showSaveSuccess).toBe(true)
        wrapper.vm.save()
        expect(wrapper.vm.showSaveSuccess).toBe(false)
      })

      it('resets fieldErrors to empty object', () => {
        const wrapper = component({
          data () {
            return {
              fieldErrors: { a: ['1'] }
            }
          },
          propsData: { edit: true }
        }, {
          aquiferStore: {
            view: {
              record: aquiferFixture
            }
          }
        })
        axios.patch.mockResolvedValue(true)

        wrapper.vm.save()
        expect(wrapper.vm.fieldErrors).toEqual({})
      })

      it('sends a patch with the contents of record on save', () => {
        const wrapper = component({
          computed: {
            id () {
              return 10
            }
          },
          data () {
            return {
              form: aquiferFixture
            }
          }
        }, {
          aquiferStore: {
            view: {
              record: aquiferFixture
            }
          }
        })

        axios.patch.mockResolvedValue(true)

        wrapper.vm.save()

        expect(axios.patch).toHaveBeenCalledWith('aquifers/10', omit(aquiferFixture, 'area', 'licence_details'))
      })
    })
  })
})
