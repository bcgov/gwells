import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import Screens from '@/submissions/components/SubmissionForm/Screens.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Screens.vue', () => {
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

  it('starts with a blank screen row', () => {
    const wrapper = shallowMount(Screens, {
      localVue,
      store,
      sync: false
    })

    expect(wrapper.vm.screens.length).toBe(1)
  })
  it('adds a new screen row when clicking Add Row', () => {
    const wrapper = shallowMount(Screens, {
      localVue,
      store,
      sync: false
    })

    wrapper.find('#addScreenRowButton').trigger('click')
    expect(wrapper.vm.screens.length).toBe(2)
  })
  it('when clicking the remove button on a row, removes that row', () => {
    const wrapper = shallowMount(Screens, {
      localVue,
      store,
      sync: false
    })

    wrapper.find('#removeScreenRowButton0').trigger('click')
    expect(wrapper.vm.screens.length).toBe(0)
  })
})
