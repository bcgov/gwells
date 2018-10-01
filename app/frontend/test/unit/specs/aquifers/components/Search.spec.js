import { shallowMount, createLocalVue } from '@vue/test-utils'
import SearchComponent from '@/aquifers/components/Search.vue'
import { SEARCH_AQUIFERS, RESET_RESULTS } from '@/aquifers/store/actions.types'
import Vuex from 'vuex'

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

describe('Search Component', () => {
  const component = ({ getters, actions }) => shallowMount(SearchComponent, {
    store: new Vuex.Store({
      getters: Object.assign({
        aquiferList: () => [],
        emptyResults: () => false
      }, getters),
      actions
    }),
    localVue
  })

  it('Displays a message if no aquifers could be found', () => {
    const wrapper = component({
      getters: { emptyResults: () => true }
    })

    expect(wrapper.text()).toContain('No aquifers could be found')
  })

  it('Matches the snapshot', () => {
    const wrapper = component({
      getters: { aquiferList: () => [aquiferFixture] }
    })

    expect(wrapper.element).toMatchSnapshot()
  })

  it('triggers SEARCH_AQUIFERS when form is submitted', () => {
    const spy = jest.fn()
    const wrapper = component({
      actions: { [SEARCH_AQUIFERS]: spy }
    })

    wrapper.find('form').trigger('submit')
    expect(spy).toHaveBeenCalled()
  })

  it('triggers RESET_RESULTS when form is reset', () => {
    const spy = jest.fn()
    const wrapper = component({
      actions: { [RESET_RESULTS]: spy }
    })

    wrapper.find('form').trigger('reset')
    expect(spy).toHaveBeenCalled()
  })

  it('resets input values when form is reset', () => {
    const spy = jest.fn()
    const wrapper = component({
      actions: { [RESET_RESULTS]: spy }
    })

    wrapper.find('form').trigger('reset')
    expect(spy).toHaveBeenCalled()
  })
})
