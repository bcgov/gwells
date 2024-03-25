import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vue from 'vue'
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

const GET_DEFAULT_STORE_MODULES = () => {
  return {
    auth: {
      getters: {
        user: () => null,
        userRoles: () => ({ registry: { edit: true, view: true, approve: true } })
      }
    },
    registriesStore: {
      namespaced: true,
      getters: {
        loading: () => false,
        error: () => null,
        currentDriller: jest.fn().mockReturnValue(fakePerson),
        searchResponse: () => [],
        drillerOptions: () => jest.fn().mockReturnValue(fakeDrillerOptions)
      },
      actions: {
        [FETCH_DRILLER_OPTIONS]: jest.fn()
      },
      mutations: {
      }
    }
  }
}

describe('ApplicationDetail.vue', () => {
  let store
  let modules

  beforeEach(() => {
    modules = GET_DEFAULT_STORE_MODULES()
    store = new Vuex.Store({
      modules: modules
    })

    ApiService.__setMockResponse(fakeRegistration)
  })

  it('loads the currentDriller and renders the person name as the page title', async () => {
    const wrapper = shallowMount(ApplicationDetail, {
      localVue,
      store,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: { params: { person_guid: fakePerson.person_guid, application_guid: fakeRegistration.applications[0].application_guid } }
      }
    })

    await Vue.nextTick()

    const titlePersonName = wrapper.find('#titlePersonName')
    expect(titlePersonName.text()).toBe(`${fakePerson.first_name} ${fakePerson.surname}`)
  })

  it('gets the list of qualified well/hole types from the driller profile for this application', async () => {
    const wrapper = shallowMount(ApplicationDetail, {
      localVue,
      store,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: { params: { person_guid: fakePerson.person_guid, application_guid: fakeRegistration.applications[0].application_guid } }
      }
    })

    await Vue.nextTick()

    expect(wrapper.vm.qualifications.length).toBe(7)
  })

  describe('User has edit rights', () => {
    console.log(modules)
    ApiService.__setMockResponse(fakeRegistration)
    modules = GET_DEFAULT_STORE_MODULES()
    modules.registriesStore.getters = Object.assign({}, modules.registriesStore.getters, {
      loading: () => false,
      error: () => null,
      currentDriller: jest.fn().mockReturnValue(fakePerson),
      drillerOptions: jest.fn().mockReturnValue(fakeDrillerOptions),
      drillers: () => []
    })
    modules.auth.getters = Object.assign({}, modules.registriesStore.getters, {
      user: () => null,
      userRoles: () => ({ registry: { edit: true, view: true, approve: true } })
    })
    let store = new Vuex.Store({ modules: modules })
    const wrapper = shallowMount(ApplicationDetail, {
      localVue,
      store,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: { params: { person_guid: fakePerson.person_guid, application_guid: fakeRegistration.applications[0].application_guid } }
      }
    })

    it('show edit button if user has appropriate rights', async () => {
      const edit = wrapper.find('#editClassification')
      expect(edit.exists()).toBe(true)
    })

    describe('User has clicked edit', () => {
      beforeAll(() => {
        const edit = wrapper.find('#editClassification')
        edit.trigger('click')
      })

      it('has a save button', () => {
        const save = wrapper.find('#saveClassification')
        expect(save.exists()).toBe(true)
      })

      it('has current issuer selected', () => {
        const issuer = wrapper.find('#issuer')
        expect(issuer.value).toBe(fakeRegistration.applications[0].primary_certificate.acc_cert_guid)
      })

      it('has a cancel button', () => {
        const cancel = wrapper.find('#cancelClassification')
        expect(cancel.exists()).toBe(true)
      })

      it('clicking cancel should show are you sure dialog', () => {
        const cancel = wrapper.find('#cancelClassification')
        cancel.trigger('click')
        expect(wrapper.find('#confirmCancelModal')).toBeTruthy()
        // Get rid of the modal
        wrapper.find('#confirmCancel').trigger('click')
      })
    })
  })

  describe('User can\'t edit', () => {
    modules = GET_DEFAULT_STORE_MODULES()
    modules.registriesStore.getters = Object.assign({}, modules.registriesStore.getters, {
      loading: () => false,
      error: () => null,
      currentDriller: jest.fn().mockReturnValue(fakePerson),
      drillerOptions: jest.fn().mockReturnValue(fakeDrillerOptions),
      drillers: () => []
    })
    modules.auth.getters = Object.assign({}, modules.registriesStore.getters, {
      user: () => null,
      userRoles: () => ({ registry: { edit: false, view: true, approve: false } })
    })

    let store = new Vuex.Store({ modules: modules })
    const wrapper = shallowMount(ApplicationDetail, {
      localVue,
      store,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: { params: { person_guid: fakePerson.person_guid, application_guid: fakeRegistration.applications[0].application_guid } }
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
