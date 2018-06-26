import { mount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import VueMoment from 'vue-moment'
import PersonDetail from '@/registry/components/people/PersonDetail'
import APIErrorMessage from '@/common/components/APIErrorMessage'
import { SET_DRILLER } from '@/registry/store/mutations.types'
import { FETCH_DRILLER, FETCH_DRILLER_OPTIONS } from '@/registry/store/actions.types'
import fakePerson from '../fakePerson'

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(VueMoment)

describe('PersonDetail.vue', () => {
  let store
  let getters
  let mutations
  let actions

  beforeEach(() => {
    getters = {
      loading: () => false,
      error: () => null,
      user: () => null,
      currentDriller: jest.fn().mockReturnValue(fakePerson),
      drillers: () => [],
      userRoles: () => ({ edit: true, view: true, approve: true })
    }
    mutations = {
      [SET_DRILLER]: jest.fn()
    }
    actions = {
      [FETCH_DRILLER]: jest.fn(),
      [FETCH_DRILLER_OPTIONS]: jest.fn()
    }
    store = new Vuex.Store({ getters, actions, mutations })
  })

  it('dispatches the fetch driller action when page loads', () => {
    mount(PersonDetail, {
      store,
      localVue,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: {params: {person_guid: 'aaaa-4444-bbbb-1111'}}
      }
    })
    expect(actions.FETCH_DRILLER).toHaveBeenCalled()
  })
  it('loads the error component if there is an error', () => {
    getters = {
      loading: () => false,
      user: () => null,
      error: () => {
        return { status: '400', statusText: 'error!' }
      },
      currentDriller: jest.fn().mockReturnValue(fakePerson),
      drillers: () => [],
      userRoles: () => ({ edit: true, view: true, approve: true })
    }
    const storeError = new Vuex.Store({ getters, actions, mutations })
    const wrapper = mount(PersonDetail, {
      store: storeError,
      localVue,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: {params: {person_guid: 'aaaa-4444-bbbb-1111'}}
      }
    })
    expect(wrapper.findAll(APIErrorMessage).length).toEqual(1)
  })
  it('doesn\'t load the error component if there is no error', () => {
    const wrapper = mount(PersonDetail, {
      store,
      localVue,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: {params: {person_guid: 'aaaa-4444-bbbb-1111'}}
      }
    })
    expect(wrapper.findAll(APIErrorMessage).length).toEqual(0)
  })
  it('has a classifications property (based on the currentDriller loaded)', () => {
    const wrapper = mount(PersonDetail, {
      store,
      localVue,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: {params: {person_guid: 'aaaa-4444-bbbb-1111'}}
      }
    })
    expect(wrapper.vm.classifications.length).toEqual(2)
  })
})
