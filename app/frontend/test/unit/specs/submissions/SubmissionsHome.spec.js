import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import SubmissionsHome from '@/submissions/views/SubmissionsHome.vue'

import { FETCH_CODES } from '@/submissions/store/actions.types.js'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('SubmissionsHome.vue', () => {
  let actions
  let store

  beforeEach(() => {
    actions = {
      [FETCH_CODES]: jest.fn()
    }
    store = new Vuex.Store({
      state: {},
      actions
    })
  })

  it('triggers confirmation box when submitting the form', () => {
    const wrapper = shallowMount(SubmissionsHome, {
      localVue,
      store,
      sync: false
    })
    expect(wrapper.vm.confirmSubmitModal).toEqual(false)

    wrapper.find('form').trigger('submit')

    expect(wrapper.vm.confirmSubmitModal).toEqual(true)
  })

  it('requests codes/constants to use in form', () => {
    shallowMount(SubmissionsHome, {
      localVue,
      store,
      sync: false
    })
    expect(actions[FETCH_CODES]).toHaveBeenCalled()
  })
})
