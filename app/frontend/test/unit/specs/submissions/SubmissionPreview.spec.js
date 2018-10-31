import Vuex from 'vuex'
import SubmissionPreview from '@/submissions/components/SubmissionPreview/SubmissionPreview.vue'
import { shallowMount, createLocalVue } from '@vue/test-utils'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('filterBlankRows', () => {
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
  it('Removes blank rows and objects containing only empty strings for tables', () => {
    const wrapper = shallowMount(SubmissionPreview, {
      localVue,
      store,
      propsData: {
        form: {},
        sections: {}
      }
    })
    let rows = [
      { data: 123 },
      { data: '' },
      {}
    ]

    const filteredRows = wrapper.vm.filterBlankRows(rows)

    expect(filteredRows.length).toBe(1)
  })
  it('Does not remove rows with values for tables', () => {
    const wrapper = shallowMount(SubmissionPreview, {
      localVue,
      store,
      propsData: {
        form: {},
        sections: {}
      }
    })
    let rows = [
      { data: 123 },
      { data: 456 },
      { data: 789 }
    ]

    const filteredRows = wrapper.vm.filterBlankRows(rows)

    expect(filteredRows.length).toBe(3)
  })
})
