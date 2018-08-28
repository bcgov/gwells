import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import Step05Lithology from '@/submissions/components/SubmissionForm/Step05Lithology.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Step05Lithology.vue', () => {
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
    const wrapper = shallowMount(Step05Lithology, {
      localVue,
      store,
      sync: false
    })

    expect(wrapper.vm.lithology.length).toBe(1)
  })
  it('adds a new lithology row when clicking Add Row', () => {
    const wrapper = shallowMount(Step05Lithology, {
      localVue,
      store,
      sync: false
    })

    wrapper.find('#addLithologyRowButton').trigger('click')
    expect(wrapper.vm.lithology.length).toBe(2)
  })
  it('when clicking the remove button on a row, removes that row', () => {
    const wrapper = shallowMount(Step05Lithology, {
      localVue,
      store,
      sync: false
    })

    wrapper.find('#removeRowButton0').trigger('click')
    expect(wrapper.vm.lithology.length).toBe(0)
  })
})
