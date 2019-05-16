import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import ApplicationDetail from '@/registry/components/people/ApplicationDetail'
import { FETCH_DRILLER_OPTIONS } from '@/registry/store/actions.types'
import fakePerson from '../fakePerson'
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
      drillerOptions: () => jest.fn().mockReturnValue(fakeDrillerOptions),
      userRoles: () => ({ registry: { edit: true, view: true, approve: true } })
    }
    mutations = {
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
    wrapper.vm.$nextTick(() => {
      const titlePersonName = wrapper.find('#titlePersonName')
      expect(titlePersonName.text()).toBe(`${fakePerson.first_name} ${fakePerson.surname}`)
    })
  })
  it('gets the list of qualified well/hole types from the driller profile for this application', () => {
    const wrapper = shallowMount(ApplicationDetail, {
      localVue,
      store,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: {params: {person_guid: fakePerson.person_guid, application_guid: fakeRegistration.applications[0].application_guid}}
      }
    })
    wrapper.vm.$nextTick(() => {
      expect(wrapper.vm.qualifications.length).toBe(7)
    })
  })
  describe('User has edit rights', () => {
    let getters = {
      loading: () => false,
      error: () => null,
      user: () => null,
      currentDriller: jest.fn().mockReturnValue(fakePerson),
      drillerOptions: jest.fn().mockReturnValue(fakeDrillerOptions),
      drillers: () => [],
      userRoles: () => ({ registry: { edit: true, view: true, approve: true } })
    }
    let mutations = {
    }
    let actions = {
      [FETCH_DRILLER_OPTIONS]: jest.fn()
    }
    let store = new Vuex.Store({ getters, actions, mutations })
    const wrapper = shallowMount(ApplicationDetail, {
      localVue,
      store,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: {params: {person_guid: fakePerson.person_guid, application_guid: fakeRegistration.applications[0].application_guid}}
      }
    })
    wrapper.vm.$nextTick(() => {
      const edit = wrapper.find('#editClassification')
      it('show edit button if user has appropriate rights', () => {
        expect(edit.exists()).toBe(true)
      })
      describe('User has clicked edit', () => {
        edit.trigger('click')
        const save = wrapper.find('#saveClassification')
        it('has a save button', () => {
          expect(save.exists()).toBe(true)
        })
        it('has current issuer selected', () => {
          const issuer = wrapper.find('#issuer')
          expect(issuer.value).toBe(fakeRegistration.applications[0].primary_certificate.acc_cert_guid)
        })
        const cancel = wrapper.find('#cancelClassification')
        it('has a cancel button', () => {
          expect(cancel.exists()).toBe(true)
        })
        describe('User has clicked cancel', () => {
          cancel.trigger('click')
          it('show are you sure dialog', () => {
            expect(wrapper.find('#confirmCancelModal')).toBeTruthy()
          })
          // Get rid of the modal
          wrapper.find('#confirmCancel').trigger('click')
        })
      })
    })
  })
  describe('User can\'t edit', () => {
    let getters = {
      loading: () => false,
      error: () => null,
      user: () => null,
      currentDriller: jest.fn().mockReturnValue(fakePerson),
      drillerOptions: jest.fn().mockReturnValue(fakeDrillerOptions),
      drillers: () => [],
      userRoles: () => ({ registry: { edit: false, view: true, approve: false } })

    }
    let mutations = {
    }
    let actions = {
      [FETCH_DRILLER_OPTIONS]: jest.fn()
    }
    let store = new Vuex.Store({ getters, actions, mutations })
    const wrapper = shallowMount(ApplicationDetail, {
      localVue,
      store,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: {params: {person_guid: fakePerson.person_guid, application_guid: fakeRegistration.applications[0].application_guid}}
      }
    })
    it('doesn\'t show edit button if user doesn\'t have appropriate rights', () => {
      expect(wrapper.find('#editClassification').exists()).toBe(false)
    })
    it('doesn\'t have a save button when not in edit mode', () => {
      expect(wrapper.find('#saveClassification').exists()).toBe(false)
    })
  })
})
