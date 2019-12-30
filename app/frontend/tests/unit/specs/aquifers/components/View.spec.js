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
import ViewComponent from '@/aquifers/components/View.vue'
import Vuex from 'vuex'
import axios from 'axios'
import auth from '@/common/store/auth.js'
import documentState from '@/common/store/documents.js'
import aquiferCodes from '@/aquifers/store/codes'
import VueRouter from 'vue-router'

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

describe('View Component', () => {
  const component = options =>
    mount(ViewComponent, {
      localVue,
      router: new VueRouter(),
      store: new Vuex.Store({
        modules: { auth, aquiferCodes, documentState }
      }),
      stubs: ['router-link', 'aquifer-documents', 'aquifer-form'],
      ...options
    })

  it('queries aquifer on load', (done) => {
    const fetch = jest.fn()

    const wrapper = component({
      methods: {
        fetch,
        fetchFiles () {
          return {
            public: [],
            private: []
          }
        },
        fetchResourceSections () {
          this.aquifer_resource_sections = []
        },
        fetchWells () {
          this.wells = []
        }
      }
    })

    wrapper.vm.$nextTick(() => {
      expect(fetch).toHaveBeenCalled()
      done()
    })
  })

  describe('View mode', () => {
    it('matches the snapshot', () => {
      const wrapper = component({
        data () {
          return {
            record: aquiferFixture
          }
        },
        methods: {
          fetch () {},
          fetchFiles () {
            return {
              public: [],
              private: []
            }
          },
          fetchResourceSections () {
            this.aquifer_resource_sections = []
          },
          fetchWells () {
            this.wells = []
          }
        },
        propsData: { edit: true }
      })

      expect(wrapper.element).toMatchSnapshot()
    })
  })

  describe('Edit mode', () => {
    it('matches the snapshot', () => {
      const wrapper = component({
        data () {
          return {
            record: aquiferFixture
          }
        },
        methods: {
          fetch () {},
          fetchFiles () {
            return {
              public: [],
              private: []
            }
          },
          fetchResourceSections () {
            this.aquifer_resource_sections = []
          },
          fetchWells () {
            this.wells = []
          }
        },
        propsData: { edit: true }
      })

      expect(wrapper.element).toMatchSnapshot()
    })

    describe('On save', () => {
      it('resets showSaveSuccess to false', () => {
        const wrapper = component({
          data () {
            return {
              record: aquiferFixture,
              showSaveSuccess: true
            }
          },
          methods: {
            fetch () {},
            fetchFiles () {
              return {
                public: [],
                private: []
              }
            },
            fetchResourceSections () {
              this.aquifer_resource_sections = []
            },
            fetchWells () {
              this.wells = []
            },
            navigateToView () {}
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
              record: aquiferFixture,
              fieldErrors: { a: ['1'] }
            }
          },
          methods: {
            fetch () {},
            fetchFiles () {
              return {
                public: [],
                private: []
              }
            },
            fetchResourceSections () {
              this.aquifer_resource_sections = []
            },
            fetchWells () {
              this.wells = []
            },
            navigateToView () {}
          },
          propsData: { edit: true }
        })
        axios.patch.mockResolvedValue(true)

        wrapper.vm.save()
        expect(wrapper.vm.fieldErrors).toEqual({})
      })

      it('sends a patch with the contents of record on save', () => {
        const wrapper = component({
          methods: {
            fetch () {},
            fetchFiles () {
              return {
                public: [],
                private: []
              }
            },
            fetchResourceSections () {
              this.aquifer_resource_sections = []
            },
            fetchWells () {
              this.wells = []
            },
            navigateToView () {}
          },
          computed: {
            id () {
              return 10
            }
          },
          data () {
            return {
              record: aquiferFixture,
              form: aquiferFixture
            }
          }
        })

        axios.patch.mockResolvedValue(true)

        wrapper.vm.save()

        expect(axios.patch).toHaveBeenCalledWith('aquifers/10', aquiferFixture)
      })
    })
  })
})
