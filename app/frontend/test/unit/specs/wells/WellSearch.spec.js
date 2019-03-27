import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import WellSearch from '@/wells/views/WellSearch.vue'

import {FETCH_CODES} from '@/submissions/store/actions.types.js'
import {FETCH_DRILLER_NAMES, FETCH_ORGANIZATION_NAMES} from '@/wells/store/actions.types.js'

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(VueRouter)

const router = new VueRouter()

describe('WellSearch.vue', () => {
  let store
  let getters
  let actions

  beforeEach(() => {
    getters = {
      codes: () => ({}),
      drillerNames: () => ({}),
      organizationNames: () => ({}),
      userRoles: () => ({ wells: { view: false } })
    }
    actions = {
      [FETCH_CODES]: jest.fn(),
      [FETCH_DRILLER_NAMES]: jest.fn(),
      [FETCH_ORGANIZATION_NAMES]: jest.fn()
    }
    store = new Vuex.Store({
      getters,
      actions
    })
  })

  it('the page renders', () => {
    const wrapper = shallowMount(WellSearch, {
      localVue,
      store,
      router,
      stubs: ['router-link', 'search-form-select', 'b-popover'],
      sync: false
    })

    expect(wrapper.find('#wellSearchTitle').text()).toBe('Well Search')
  })
  it('a well search request adds a token to pending request list', () => {
    const wrapper = shallowMount(WellSearch, {
      localVue,
      store,
      router,
      stubs: ['router-link', 'search-form-select', 'b-popover'],
      sync: false
    })
    expect(wrapper.vm.pendingSearches.length).toBe(0)
    wrapper.vm.wellSearch()
    expect(wrapper.vm.pendingSearches.length).toBe(1)
  })
  it('cancelWellSearches() cancels previous requests', () => {
    const wrapper = shallowMount(WellSearch, {
      localVue,
      store,
      router,
      stubs: ['router-link', 'search-form-select', 'b-popover'],
      sync: false
    })
    const testReq = {
      cancel: jest.fn()
    }
    for (let i = 0; i < 10; i++) {
      wrapper.vm.pendingSearches.push(testReq)
    }

    wrapper.vm.cancelWellSearches()

    expect(testReq.cancel.mock.calls.length).toBe(10)
    expect(wrapper.vm.pendingSearches.length).toBe(0)
  })
})
