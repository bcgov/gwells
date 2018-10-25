import { shallowMount, createLocalVue } from '@vue/test-utils'
import SearchComponent from '@/aquifers/components/Search.vue'
import Vuex from 'vuex'
import axios from 'axios'
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

describe('Search Component', () => {
  const component = (options) => shallowMount(SearchComponent, {
    localVue,
    stubs: ['router-link', 'router-view'],
    router: new VueRouter(),
    methods: {
      scrollToTableTop() {}
    },
    ...options
  })

  it('Displays a message if no aquifers could be found', () => {
    const wrapper = component({
      computed: {
        aquiferList() { return [] },
        emptyResults() { return true }
      }
    })

    expect(wrapper.text()).toContain('No aquifers could be found')
  })

  it('Matches the snapshot', () => {
    const wrapper = component({
      computed: {
        aquiferList() { return [aquiferFixture] }
      }
    })

    expect(wrapper.element).toMatchSnapshot()
  })

  it('search updates route query params', () => {
    axios.get.mockResolvedValue({})

    const wrapper = component()
    wrapper.find('#search').setValue('asdf')
    wrapper.find('form').trigger('submit')

    expect(axios.get).toHaveBeenCalledWith('aquifers/', {"params": { "search": "asdf" }})
  })

  it('form reset resets response and query', () => {
    const wrapper = component()

    wrapper.find('#search').setValue('asdf')
    wrapper.find('form').trigger('submit')

    expect(wrapper.vm.query.search).toEqual('asdf')

    wrapper.find('form').trigger('reset')

    expect(wrapper.vm.query.search).toEqual('')
  })
})
