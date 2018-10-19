import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import Liner from '@/submissions/components/SubmissionForm/Liner.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Liner.vue', () => {
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

  it('starts with 3 blank liner perforation rows', () => {
    const wrapper = shallowMount(Liner, {
      localVue,
      store,
      propsData: {
        linerPerforations: []
      }
    })

    expect(wrapper.vm.linerPerforationsInput.length).toBe(3)
  })
  it('adds a new Liner row when clicking Add Row', () => {
    const wrapper = shallowMount(Liner, {
      localVue,
      store,
      propsData: {
        linerPerforations: []
      }
    })

    wrapper.find('#addlinerPerforationRowBtn').trigger('click')
    expect(wrapper.vm.linerPerforationsInput.length).toBe(4)
  })
  it('when clicking the remove button on a row, removes that row', () => {
    const wrapper = shallowMount(Liner, {
      localVue,
      store,
      propsData: {
        linerPerforations: []
      }
    })

    wrapper.find('#removeLinerPerfRowBtn0').trigger('click')
    expect(wrapper.vm.linerPerforationsInput.length).toBe(2)
  })
})
