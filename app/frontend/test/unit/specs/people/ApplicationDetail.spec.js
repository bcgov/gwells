import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import ApplicationDetail from '@/registry/components/people/ApplicationDetail'
import { SET_DRILLER } from '@/registry/store/mutations.types'
import { FETCH_DRILLER_OPTIONS } from '@/registry/store/actions.types'
import fakePerson from '../fakePerson2' // TODO: rename this! or use a single one!
import fakeDrillerOptions from '../fakeDrillerOptions'
import fakeRegistration from '../fakeRegistration'
import ApiService from '@/common/services/ApiService.js'

jest.mock('@/common/services/ApiService.js')

const localVue = createLocalVue()
localVue.use(Vuex)

describe('ApplicationDetail.vue', () => {
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
      userIsAdmin: () => false,
      drillerOptions: () => jest.fn().mockReturnValue(fakeDrillerOptions)
    }
    mutations = {
      [SET_DRILLER]: jest.fn()
    }
    actions = {
      [FETCH_DRILLER_OPTIONS]: jest.fn()
    }
    store = new Vuex.Store({ getters, actions, mutations })

    ApiService.__setMockResponse(fakeRegistration)
  })
  it('loads the currentDriller and renders the person name as the page title', () => {
    const wrapper = shallowMount(ApplicationDetail, {
      localVue,
      store,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: {params: {person_guid: fakePerson.person_guid, application_guid: fakeRegistration.applications[0].application_guid}}
      }
    })
    wrapper.setData({registration: fakeRegistration})
    wrapper.vm.$forceUpdate()
    expect(wrapper.find('#titlePersonName').text()).toBe(`${fakePerson.first_name} ${fakePerson.surname}`)
  })
  it('gets the list of qualified well/hole types from the driller profile for this application', () => {
    const wrapper = shallowMount(ApplicationDetail, {
      localVue,
      store,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: {params: {person_guid: fakePerson.person_guid, classCode: 'geotech'}}
      }
    })
    wrapper.setData({registration: fakeRegistration})
    wrapper.vm.$forceUpdate()
    expect(wrapper.vm.qualCodeList.length).toBe(3)
  })
  // it('removes current driller from store if we need to fetch another driller (prevent momentarily showing previous driller', () => {
  //   shallowMount(ApplicationDetail, {
  //     localVue,
  //     store,
  //     stubs: ['router-link', 'router-view'],
  //     mocks: {
  //       $route: {params: {person_guid: 'aaaa-4444-aaaa', classCode: 'geotech'}}
  //     }
  //   })
  //   expect(mutations.SET_DRILLER).toHaveBeenCalled()
  // })

  // describe('User has edit rights', () => {
  //   let getters = {
  //     loading: () => false,
  //     error: () => null,
  //     user: () => null,
  //     currentDriller: jest.fn().mockReturnValue(fakePerson),
  //     drillerOptions: jest.fn().mockReturnValue(fakeDrillerOptions),
  //     drillers: () => [],
  //     userIsAdmin: () => true
  //   }
  //   let mutations = {
  //     [SET_DRILLER]: jest.fn()
  //   }
  //   let actions = {
  //     [FETCH_DRILLER]: jest.fn()
  //   }
  //   let store = new Vuex.Store({ getters, actions, mutations })
  //   const wrapper = shallowMount(ApplicationDetail, {
  //     localVue,
  //     store,
  //     stubs: ['router-link', 'router-view'],
  //     mocks: {
  //       $route: {params: {person_guid: fakePerson.person_guid, classCode: 'geotech'}}
  //     }
  //   })

  //   const edit = wrapper.find('#editClassification')
  //   it('show edit button if user has appropriate rights', () => {
  //     expect(edit.exists()).toBe(true)
  //   })
  //   describe('User has clicked edit', () => {
  //     edit.trigger('click')
  //     const save = wrapper.find('#saveClassification')
  //     it('has a save button', () => {
  //       expect(save.exists()).toBe(true)
  //     })
  //   //   describe('User has clicked save', () => {
  //   //     // TODO: When you get here, write test to enter data
  //   //     save.trigger('click')
  //   //     it('dispatches mutation when save/update is clicked', () => {
  //   //       expect(mutations.UPDATE_APPLICATION).toHaveBeenCalled()
  //   //     })
  //   //   })
  //   })
  // })
  // // describe('User can\'t edit', () => {
  // //   const wrapper = shallowMount(ApplicationDetail, {
  // //     localVue,
  // //     store,
  // //     stubs: ['router-link', 'router-view'],
  // //     mocks: {
  // //       $route: {params: {person_guid: fakePerson.person_guid, classCode: 'geotech'}}
  // //     }
  // //   })
  // //   it('doesn\'t show edit button if user doesn\'t have appropriate rights', () => {
  // //     expect(wrapper.find('input[type="button"][id="edit"]').exists()).toBe(false)
  // //   })

  // //   it('doesn\'t have a save button when not in edit mode', () => {
  // //     expect(wrapper.find('input[type="button"][id="save"]').exists()).toFalse(true)
  // //   })
  // // })
})
