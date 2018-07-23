import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import SubmissionsHome from '@/submissions/views/SubmissionsHome.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('SubmissionsHome.vue', () => {
  it('triggers confirmation box when submitting the form', () => {
    const wrapper = shallowMount(SubmissionsHome, {
      localVue,
      sync: false
    })
    expect(wrapper.vm.confirmSubmitModal).toEqual(false)

    wrapper.find('form').trigger('submit')

    expect(wrapper.vm.confirmSubmitModal).toEqual(true)
  })
})
