import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import PersonDetail from '@/registry/components/people/PersonDetail'
import APIErrorMessage from '@/common/components/APIErrorMessage'
import { SET_DRILLER } from '@/registry/store/mutations.types'
import { FETCH_DRILLER } from '@/registry/store/actions.types'
import fakePerson from '../fakePerson'

const localVue = createLocalVue()
localVue.use(Vuex)

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
      userIsAdmin: () => true
    }
    mutations = {
      [SET_DRILLER]: jest.fn()
    }
    actions = {
      [FETCH_DRILLER]: jest.fn()
    }
    store = new Vuex.Store({ getters, actions, mutations })
  })

  it('dispatches the fetch driller action when page loads', () => {
    shallowMount(PersonDetail, {
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
      userIsAdmin: () => true
    }
    const storeError = new Vuex.Store({ getters, actions, mutations })
    const wrapper = shallowMount(PersonDetail, {
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
    const wrapper = shallowMount(PersonDetail, {
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
    const wrapper = shallowMount(PersonDetail, {
      store,
      localVue,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: {params: {person_guid: 'aaaa-4444-bbbb-1111'}}
      }
    })
    expect(wrapper.vm.classifications.length).toEqual(2)
  })
  it('Application entry form', () => {
    // const wrapper = shallowMount(PersonDetail, {
    //   store,
    //   localVue,
    //   stubs: ['router-link', 'router-view'],
    //   mocks: {
    //     $route: {params: {person_guid: 'aaaa-4444-bbbb-1111'}}
    //   }
    // })
    // describe('Add pump application', () => {
    //   const addPumpApplication = wrapper.find('input[type="button"][id="addPumpApplication"]')
    //   it('Expect add pump application button exists', () => {
    //     expect(addPumpApplication.exists()).toBe(true)
    //   })

    //   describe('Click add', () => {
    //     addPumpApplication.trigger('click')
    //     it('add pump application pops up/injects area to specify application', () => {
    //       const addPumpView = wrapper.find('#addPumpView')
    //       expect(addPumpView.exists()).toBe(false)
    //     })
    //     // TODO: When you get here, write test to enter data
    //     it('add pump application must dispatch appropriate json to endpoint on save', () => {
    //       const savePump = wrapper.find('#savePump')
    //       savePump.trigger('click')
    //       expect(mutations.ADD_APPLICATION).toHaveBeenCalled()
    //     })
    //   })
    // })

    // describe('Add drill application', () => {
    //   const addDrillApplication = wrapper.find('input[type="button"][id="addDrillApplication"]')
    //   it('Expect add drill application button exists', () => {
    //     expect(addDrillApplication.exists()).toBe(true)
    //   })

    //   describe('Click add', () => {
    //     addDrillApplication.trigger('click')

    //     it('add drill application pops up/injects area to specify application', () => {
    //       const addPumpView = wrapper.find('#addDrillView')
    //       expect(addPumpView.exists()).toBe(false)
    //     })
    //     // TODO: When you get here, write test to enter data
    //     it('add drill application must dispatch appropriate json to endpoint on save', () => {
    //       const saveDrill = wrapper.find('#savePump')
    //       saveDrill.trigger('click')
    //       expect(mutations.ADD_APPLICATION).toHaveBeenCalled()
    //     })
    //   })
    // })
  })
})
