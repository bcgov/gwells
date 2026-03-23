import '../../mocks/mapbox-gl'
import { mount, shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import useCommonStore from '@/stores/common.js'
import SubmissionsHome from '@/submissions/views/SubmissionsHome.vue'

import { FETCH_CODES, FETCH_WELL_TAGS } from '@/submissions/store/actions.types.js'

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
      [FETCH_CODES]: jest.fn(),
      [FETCH_WELL_TAGS]: jest.fn()
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
    expect(actions[FETCH_CODES]).toHaveBeenCalled()
  })
})
