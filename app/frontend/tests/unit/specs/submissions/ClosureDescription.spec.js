import { mount, shallowMount, createLocalVue } from '@vue/test-utils'
import Vue from 'vue'
import Vuex from 'vuex'
import ClosureDescription from '@/submissions/components/SubmissionForm/ClosureDescription.vue'

const localVue = createLocalVue()
const defaultRows = 10
localVue.use(Vuex)

describe('ClosureDescription.vue', () => {
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

  it('starts with 10 blank closure description rows', () => {
    const wrapper = shallowMount(ClosureDescription, {
      localVue,
      store,
      sync: false
    })

    expect(wrapper.vm.closureDescriptionSetData.length).toBe(defaultRows)
  })

  it('adds a new ClosureDescription row when clicking Add Row', () => {
    const wrapper = mount(ClosureDescription, {
      localVue,
      store,
      sync: false
    })

    wrapper.find('#addClosureRowButton').trigger('click')
    expect(wrapper.vm.closureDescriptionSetData.length).toBe(defaultRows + 1) // default + 1 extra
  })

  it('when clicking the remove button on a row, removes that row', () => {
    const wrapper = mount(ClosureDescription, {
      localVue,
      store,
      sync: false
    })

    wrapper.find('#removeClosureDescriptionRowBtn0').trigger('click')
    expect(wrapper.vm.closureDescriptionSetData.length).toBe(defaultRows - 1)
  })

  it('Passes errors into the input components', async () => {
    const wrapper = mount(ClosureDescription, {
      localVue,
      store,
      sync: true
    })
    wrapper.setProps({
      errors: {
        decommission_description_set: [
          {
            start: [
              'Test error for start field'
            ]
          }
        ]
      }
    })

    await Vue.nextTick()

    const errMsg = wrapper.find('#closureFrom0InvalidFeedback')
    expect(errMsg.text()).toContain('Test error for start field')
  })
})
