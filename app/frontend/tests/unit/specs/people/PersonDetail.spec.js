import { mount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import VueMoment from 'vue-moment'
import moxios from 'moxios'
import PersonDetail from '@/registry/components/people/PersonDetail'
import APIErrorMessage from '@/common/components/APIErrorMessage'
import documentState from '@/common/store/documents.js'
import { SET_DRILLER } from '@/registry/store/mutations.types'
import { FETCH_DRILLER, FETCH_DRILLER_OPTIONS } from '@/registry/store/actions.types'
import fakePerson from '../fakePerson'

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(VueMoment)

const GET_DEFAULT_STORE_MODULES = () => {
  return {
    documentState,
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
      },
      actions: {
        [FETCH_DRILLER]: jest.fn(),
        [FETCH_DRILLER_OPTIONS]: jest.fn()
      },
      mutations:{
        [SET_DRILLER]: jest.fn()
      }
    }        
  }  
}

describe('PersonDetail.vue', () => {
  let store
  let modules

  beforeEach(() => {
    moxios.install()
    modules = GET_DEFAULT_STORE_MODULES()
    store = new Vuex.Store({
      modules: modules
    })
  })

  afterEach(() => {
    moxios.uninstall()
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
    expect(modules.registriesStore.actions.FETCH_DRILLER).toHaveBeenCalled()
  })
  it('loads the error component if there is an error', () => {
    modules.registriesStore.getters = Object.assign({}, modules.registriesStore.getters, {
      loading: () => false,
      error: () => {
        return { status: '400', statusText: 'error!' }
      },
      currentDriller: jest.fn().mockReturnValue(fakePerson),
      searchResponse: () => [],
    })
    modules.auth.getters = Object.assign({}, modules.registriesStore.getters, {
      user: () => null,
      userRoles: () => ({ registry: { edit: true, view: true, approve: true } })
    })
    
    const storeError = new Vuex.Store({ modules: modules })
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
