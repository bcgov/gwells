import { shallowMount, createLocalVue } from '@vue/test-utils'
import EditComponent from '@/aquifers/components/Edit.vue'
import Vuex from 'vuex'
import axios from 'axios'
import auth from '@/common/store/auth.js'

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
  mapping_year: '1993'
}

describe('Edit Component', () => {
  const component = (options) => shallowMount(EditComponent, {
    localVue,
    data() {
      return {
        record: aquiferFixture
      }
    },
    store: new Vuex.Store({
      modules: { auth }
    }),
    methods: {
      fetchCode() { },
      fetch() { }
    },
    propsData: {
      id: 10
    },
    ...options
  })

  it('Matches the snapshot', () => {
    const wrapper = component()

    expect(wrapper.element).toMatchSnapshot()
  })

  it('queries aquifer on load', () => {
    const fetch = jest.fn()

    component({ methods: { fetchCode() { }, fetch } })

    expect(fetch).toHaveBeenCalled()
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
            quality_concerns: [errorMessage],
            productivity: [errorMessage],
            area: [errorMessage],
            demand: [errorMessage],
            known_water_use: [errorMessage],
            notes: [errorMessage],
          }
        }
      }
    })

    expect(wrapper.find('#mapping_year + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#aquifer_name + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#litho_stratographic_unit + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#location_description + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#vulnerability + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#material + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#subtype + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#quality_concerns + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#productivity + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#area + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#demand + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#known_water_use + [role="alert"]').text()).toBe(errorMessage)
    expect(wrapper.find('#notes + [role="alert"]').text()).toBe(errorMessage)
  })

  describe('save', () => {
    it('sends a patch with the contents of record on save', () => {
      const wrapper = component()

      axios.patch.mockResolvedValue(true)

      wrapper.vm.save()

      expect(axios.patch).toHaveBeenCalledWith('aquifers/10/', aquiferFixture)
    })
  })
})
