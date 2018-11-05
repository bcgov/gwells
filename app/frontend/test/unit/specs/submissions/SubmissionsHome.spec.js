import { shallowMount, createLocalVue, mount } from '@vue/test-utils'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import SubmissionsHome from '@/submissions/views/SubmissionsHome.vue'
import Yield from '@/submissions/components/SubmissionForm/Yield.vue'
// import ActivitySubmissionForm from '@/submissions/components/SubmissionForm/ActivitySubmissionForm.vue'

import { FETCH_CODES } from '@/submissions/store/actions.types.js'

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(VueRouter)

const router = new VueRouter()

describe('SubmissionsHome.vue', () => {
  let actions
  let store
  let getters

  beforeEach(() => {
    getters = {
      userRoles: () => ({ wells: { edit: true }, submissions: { edit: true } })
    }
    actions = {
      [FETCH_CODES]: jest.fn()
    }
    store = new Vuex.Store({
      state: {},
      actions,
      getters
    })
  })

  it('triggers confirmation box when submitting the form', () => {
    const wrapper = shallowMount(SubmissionsHome, {
      localVue,
      store,
      router,
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
      router,
      sync: false
    })
    expect(actions[FETCH_CODES]).toHaveBeenCalled()
  })

  it('renders components based on the activity selected (Yield exists on construction report', (done) => {
    const wrapper = mount(SubmissionsHome, {
      localVue,
      store,
      router
    })
    wrapper.setData({ activityType: 'CON' })
    wrapper.vm.$nextTick(() => {
      expect(wrapper.find(Yield).exists()).toBe(true)
      done()
    })
  })
  it('renders components based on the activity selected (Yield does not exist on decommission report)', (done) => {
    const wrapper = shallowMount(SubmissionsHome, {
      localVue,
      store,
      router
    })
    wrapper.setData({ activityType: 'DEC', formIsFlat: true })
    wrapper.vm.$nextTick(() => {
      expect(wrapper.find(Yield).exists()).toBe(false)
      done()
    })
  })
})
