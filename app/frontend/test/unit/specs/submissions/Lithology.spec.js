import { mount, shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import Lithology from '@/submissions/components/SubmissionForm/Lithology.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Lithology.vue', () => {
  let store
  let getters

  beforeEach(() => {
    getters = {
      codes: () => ({})
    }
    store = new Vuex.Store({
      getters
    })
  })

  it('starts with a blank lithology row', () => {
    const wrapper = shallowMount(Lithology, {
      localVue,
      store,
      sync: false
    })

    expect(wrapper.vm.lithologyData.length).toBe(10)
  })
  it('adds a new lithology row when clicking Add Row', () => {
    const wrapper = mount(Lithology, {
      localVue,
      store,
      sync: false
    })

    wrapper.find('#addLithologyRowButton').trigger('click')
    expect(wrapper.vm.lithologyData.length).toBe(11)
  })
  it('when clicking the remove button on a row, removes that row', () => {
    const wrapper = mount(Lithology, {
      localVue,
      store,
      sync: false
    })

    wrapper.find('#removeRowButton0').trigger('click')
    expect(wrapper.vm.lithologyData.length).toBe(9)
  })
})
