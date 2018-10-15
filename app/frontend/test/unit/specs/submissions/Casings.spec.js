import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import Casings from '@/submissions/components/SubmissionForm/Casings.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Casings.vue', () => {
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

  it('starts with 3 blank casing rows', () => {
    const wrapper = shallowMount(Casings, {
      localVue,
      store,
      propsData: {
        casings: []
      }
    })

    expect(wrapper.vm.casingsInput.length).toBe(3)
  })
  it('adds a new Casings row when clicking Add Row', () => {
    const wrapper = shallowMount(Casings, {
      localVue,
      store,
      propsData: {
        casings: []
      }
    })

    wrapper.find('#addCasingRowBtn').trigger('click')
    expect(wrapper.vm.casingsInput.length).toBe(4)
  })
  it('when clicking the remove button on a row, removes that row', () => {
    const wrapper = shallowMount(Casings, {
      localVue,
      store,
      sync: false,
      propsData: {
        casings: []
      }
    })

    wrapper.find('#removeCasingRowBtn0').trigger('click')
    expect(wrapper.vm.casingsInput.length).toBe(2)
  })
  it('Passes errors into the input components', () => {
    const wrapper = shallowMount(Casings, {
      localVue,
      store,
      sync: true,
      propsData: {
        casings: []
      }
    })
    wrapper.setProps({
      errors: {
        casing_set: [
          {
            start: [
              'Test error for start field'
            ]
          }
        ]
      }
    })
    const errMsg = wrapper.find('#casing_from_0InvalidFeedback')
    expect(errMsg.text()).toContain('Test error for start field')
  })
})
