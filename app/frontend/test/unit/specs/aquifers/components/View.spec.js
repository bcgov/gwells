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
  mapping_year: '1993'
}

describe('View Component', () => {
  const component = (options) => mount(ViewComponent, {
    localVue,
    router: new VueRouter(),
    store: new Vuex.Store({
      modules: { auth, aquiferCodes }
    }),
    ...options
  })

  it('queries aquifer on load', () => {
    const fetch = jest.fn()

    component({
      methods: { fetch }
    })

    expect(fetch).toHaveBeenCalled()
  })

  describe('View mode', () => {
    it('matches the snapshot', () => {
      const wrapper = component({
        data() {
          return {
            record: aquiferFixture
          }
        },
        methods: { fetch () {} },
        propsData: { edit: true }
      })

      expect(wrapper.element).toMatchSnapshot()
    })
  })

  describe('Edit mode', () => {
    it('matches the snapshot', () => {
      const wrapper = component({
        data() {
          return {
            record: aquiferFixture
          }
        },
        methods: { fetch () {} },
        propsData: { edit: true }
      })

      expect(wrapper.element).toMatchSnapshot()
    })

    describe('On save', () => {
      it('resets showSaveSuccess to false', () => {
        const wrapper = component({
          data() {
            return {
              record: aquiferFixture,
              showSaveSuccess: true
            }
          },
          methods: {
            fetch () {},
            navigateToView () {}
          },
          propsData: { edit: true }
        })

        axios.patch.mockResolvedValue(true)

        expect(wrapper.vm.showSaveSuccess).toBe(true)
        wrapper.vm.save()
        expect(wrapper.vm.showSaveSuccess).toBe(false)
      })

      it('resets fieldErrors to empty object', () => {
        const wrapper = component({
          data() {
            return {
              record: aquiferFixture,
              fieldErrors: { a: ['1'] }
            }
          },
          methods: {
            fetch () {},
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
            navigateToView () {}
          },
          computed: { id () { return 10 } },
          data() { return { record: aquiferFixture } }
        })

        axios.patch.mockResolvedValue(true)

        wrapper.vm.save()

        expect(axios.patch).toHaveBeenCalledWith('aquifers/10/', aquiferFixture)
      })
    })
  })

  it('displays field errors messages', () => {
    let errorMessage = 'error message'

    const wrapper = component({
      data() {
        return {
          fieldErrors: {
            mapping_year: [errorMessage],
            aquifer_name: [errorMessage],
            litho_stratographic_unit: [errorMessage],
            location_description: [errorMessage],
            vulnerability: [errorMessage],
            material: [errorMessage],
            subtype: [errorMessage],
            quality_concern: [errorMessage],
            productivity: [errorMessage],
            area: [errorMessage],
            demand: [errorMessage],
            known_water_use: [errorMessage],
            notes: [errorMessage],
          }
        }
      },
      methods: { fetch () {} },
      propsData: { edit: true }
    })

    expect(wrapper.find('#mapping_year + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#aquifer_name + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#litho_stratographic_unit + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#location_description + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#vulnerability + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#material + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#subtype + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#quality_concern + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#productivity + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#area + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#demand + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#known_water_use + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#notes + [role="alert"]').text()).toBe(errorMessage)
  })
})
