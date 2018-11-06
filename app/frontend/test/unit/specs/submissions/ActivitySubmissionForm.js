import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import ActivitySubmissionForm from '@/submissions/components/SubmissionForm/ActivitySubmissionForm'
import Yield from '@/submissions/components/SubmissionForm/Yield.vue'

import { FETCH_CODES } from '@/submissions/store/actions.types.js'

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(VueRouter)

const router = new VueRouter()

describe('ActivitySubmissionForm.vue', () => {
  let actions
  let store
  let getters

  beforeEach(() => {
    getters = {
      userRoles: () => ({ wells: { edit: true }, submissions: { edit: true } }),
      isAuthenticated: () => true
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

  it('renders components based on the activity selected (Yield exists on construction report', (done) => {
    const wrapper = shallowMount(ActivitySubmissionForm, {
      localVue,
      store,
      router
    })
    wrapper.setData({ activityType: 'CON' })
    wrapper.vm.$nextTick(() => {
      expect(wrapper.find(ActivitySubmissionForm).find('#moo').exists()).toBe(true)
      done()
    })
  })
  it('renders components based on the activity selected (Yield does not exist on decommission report)', (done) => {
    const wrapper = shallowMount(ActivitySubmissionForm, {
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
