import '../../mocks/mapbox-gl'
import { mount, shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import useCommonStore from '@/stores/common.js'
import SubmissionsHome from '@/submissions/views/SubmissionsHome.vue'
import { useSubmissionStore } from '@/stores/submission'

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
      fetchCodes: jest.fn(),
      fetchWellTags: jest.fn()
    }
    store = new Vuex.Store({
      state: {},
      actions,
      getters,
      modules: { useCommonStore }
    })
  })

  it('requests codes/constants to use in form', () => {
    shallowMount(SubmissionsHome, {
      localVue,
      store,
      router,
      sync: false
    })
    expect(actions.fetchCodes()).toHaveBeenCalled()
  })
})
