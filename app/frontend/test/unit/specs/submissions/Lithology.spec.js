import { shallowMount, createLocalVue } from '@vue/test-utils'
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

    expect(wrapper.vm.lithology.length).toBe(1)
  })
  it('adds a new lithology row when clicking Add Row', () => {
    const wrapper = shallowMount(Lithology, {
      localVue,
      store,
      sync: false
    })

    wrapper.find('#addLithologyRowButton').trigger('click')
    expect(wrapper.vm.lithology.length).toBe(2)
  })
  it('when clicking the remove button on a row, removes that row', () => {
    const wrapper = shallowMount(Lithology, {
      localVue,
      store,
      sync: false
    })

    wrapper.find('#removeRowButton0').trigger('click')
    expect(wrapper.vm.lithology.length).toBe(0)
  })
})
