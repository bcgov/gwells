import { shallowMount, createLocalVue } from '@vue/test-utils'
import ViewComponent from '@/aquifers/components/View.vue'
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

describe('View Component', () => {
  const component = (options) => shallowMount(ViewComponent, {
    localVue,
    store: new Vuex.Store({
      modules: { auth }
    }),
    ...options
  })

  it('Matches the snapshot', () => {
    const wrapper = component({
      data() {
        return {
          record: aquiferFixture
        }
      },
      methods: {
        fetch() { }
      }
    })

    expect(wrapper.element).toMatchSnapshot()
  })

  it('queries aquifer on load', () => {
    const fetch = jest.fn()

    component({
      methods: { fetch }
    })

    expect(fetch).toHaveBeenCalled()
  })

  describe('fetch', () => {
    it('retrieves and assigns the aquifer to record', (done) => {
      const data = { a: 1 }

      axios.get.mockResolvedValue({ data })

      const wrapper = component({
        created() { },
        watch: {}
      })

      wrapper.vm.fetch(10)

      wrapper.vm.$nextTick(() => {
        expect(axios.get).toHaveBeenCalledWith('aquifers/10', { "params": undefined })
        expect(wrapper.vm.record).toEqual(data)
        done()
      })
    })
  })
})
