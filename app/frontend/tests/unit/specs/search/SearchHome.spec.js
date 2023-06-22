import '../../mocks/mapbox-gl'
import { mount, shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import moxios from 'moxios'
import SearchHome from '@/registry/components/search/SearchHome'
import SearchTable from '@/registry/components/search/SearchTable'
import APIErrorMessage from '@/common/components/APIErrorMessage'
import fakeDrillerOptions from '../fakeDrillerOptions'
import {
  FETCH_CITY_LIST,
  FETCH_DRILLER_OPTIONS,
  REQUEST_MAP_POSITION,
  SEARCH,
  RESET_SEARCH
} from '@/registry/store/actions.types'
import { SET_SEARCH_RESPONSE, SET_LAST_SEARCHED_PARAMS } from '@/registry/store/mutations.types'
import fakePersonList from '../fakePersonList.js'

const localVue = createLocalVue()
localVue.use(Vuex)

const DEFAULT_REGISTRIES_STORE_GETTERS = {
  drillerOptions: jest.fn().mockReturnValue(fakeDrillerOptions),
  searchResponse: () => {
    return {
      results: [
        {
          person_guid: '1e252dca-ccb9-439a-a6ec-aeec0f7e4a03',
          first_name: 'Alexis',
          surname: 'Rodriguez',
          organization_name: null,
          street_address: null,
          city: null,
          province_state: null,
          contact_tel: null,
          contact_email: null,
          activity: 'Well Driller',
          status: 'Active',
          registration_no: 'WD 08315530'
        },
        {
          person_guid: 'db02b5bb-1473-4f97-9bcf-f6214e8dd5aa',
          first_name: 'Ann',
          surname: 'Berg',
          organization_name: 'Earthplex Installers',
          street_address: '7010 Rocky Bluff Mall',
          city: 'Atlin',
          province_state: 'BC',
          contact_tel: '(604) 424-7090',
          contact_email: 'cardenas@driller.ca',
          activity: 'Well Driller',
          status: 'Active',
          registration_no: 'WD 04187177'
        }
      ]
    }
  },
  loading: () => false,
  listError: () => null,
  cityList: () => {
    return {
      drillers: [
        {
          cities: ['Duncan', 'Esquimalt'],
          prov: 'BC'
        },
        {
          prov: 'AB',
          cities: ['Jasper']
        }
      ],
      installers: [
        {
          cities: ['Nanaimo'],
          prov: 'BC'
        }
      ]
    }
  },
  activity: () => 'DRILL',
  searchParams: () => {
    return {
      search: '',
      city: [''],
      activity: 'DRILL',
      status: 'A',
      limit: '10',
      ordering: ''
    }
  },
  isSearchInProgress: () => false,
  lastSearchedParams: () => {
    return {
      raw: {
        search: '',
        city: [''],
        activity: 'DRILL',
        status: 'A',
        limit: '10',
        ordering: 'surname'
      },
      api: {}
    }
  },
  requestedMapPosition: () => null,
  hasSearched: () => false
}
const DEFAULT_REGISTRIES_STORE_ACTIONS = {
  [FETCH_CITY_LIST]: jest.fn(),
  [FETCH_DRILLER_OPTIONS]: jest.fn(),
  [REQUEST_MAP_POSITION]: jest.fn(),
  [SEARCH]: jest.fn(),
  [RESET_SEARCH]: jest.fn()
}
const DEFAULT_REGISTIES_STORE_MUTATIONS = {
  [SET_SEARCH_RESPONSE]: jest.fn(),
  [SET_LAST_SEARCHED_PARAMS]: jest.fn()
}

describe('SearchHome.vue', () => {
  let store
  let authGetters

  beforeEach(() => {
    moxios.install()
    authGetters = {
      userRoles: () => ({ registry: { edit: false, view: false, approve: false } })
    }
    store = new Vuex.Store({
      modules: {
        auth: { getters: authGetters },
        registriesStore: { namespaced: true, getters: DEFAULT_REGISTRIES_STORE_GETTERS, actions: DEFAULT_REGISTRIES_STORE_ACTIONS, mutations: DEFAULT_REGISTIES_STORE_MUTATIONS }
      }
    })
  })

  afterEach(() => {
    moxios.uninstall()
  })

  it('loads the table component', () => {
    const wrapper = shallowMount(SearchHome, {
      store,
      localVue
    })
    expect(wrapper.findAll(SearchTable).length)
      .toEqual(1)
  })

  it('loads the error component if there is an error', () => {
    const authGetters = {
      userRoles: () => ({ registry: { edit: false, view: false, approve: false } })
    }
    const registriesStoreGetters = Object.assign({}, DEFAULT_REGISTRIES_STORE_GETTERS, {
      searchResponse: () => [],
      loading: () => false,
      listError: () => {
        return { status: '400', statusText: 'error!' }
      },
      cityList: () => [],
      activity: () => 'DRILL'
    })
    const store = new Vuex.Store({
      modules: {
        auth: { getters: authGetters },
        registriesStore: { namespaced: true, getters: registriesStoreGetters, actions: DEFAULT_REGISTRIES_STORE_ACTIONS, mutations: DEFAULT_REGISTIES_STORE_MUTATIONS }
      }
    })
    const wrapper = shallowMount(SearchHome, {
      store,
      localVue
    })
    expect(wrapper.findAll(APIErrorMessage).length)
      .toEqual(1)
  })

  it('doesn\'t load the error component if there is no error', () => {
    const wrapper = shallowMount(SearchHome, {
      store,
      localVue
    })
    expect(wrapper.findAll(APIErrorMessage).length)
      .toEqual(0)
  })
  it('calls sort method when register table component emits a sort code', () => {
    const wrapper = shallowMount(SearchHome, {
      store,
      localVue
    })
    const table = wrapper.find(SearchTable)
    let spy = jest.spyOn(wrapper.vm, 'sortTable')
    wrapper.setMethods({ sortTable: spy })
    table.vm.$emit('sort', '-surname')
    expect(spy).toHaveBeenCalledWith('-surname')
    spy.mockRestore()
  })
  it('has a list of cities for drillers', () => {
    const wrapper = shallowMount(SearchHome, {
      store,
      localVue
    })
    const cityOptions = wrapper.findAll('#cityOptions option')
    expect(cityOptions.length).toEqual(4) // three options in store + 'all' option
    expect(cityOptions.at(0).text()).toEqual('All')
    expect(cityOptions.at(1).text()).toEqual('Duncan')
    expect(cityOptions.at(2).text()).toEqual('Esquimalt')
    expect(cityOptions.at(3).text()).toEqual('Jasper')
  })
  it('store reset_search action is dispatched after reset button clicked', () => {
    const wrapper = mount(SearchHome, {
      store,
      localVue
    })
    wrapper.find('[type=reset]').trigger('reset')
    expect(DEFAULT_REGISTRIES_STORE_ACTIONS.RESET_SEARCH).toHaveBeenCalled()
  })
  it('shows shows the xlsx and csv download links', () => {
    const authGetters = {
      userRoles: () => ({ registry: { edit: false, view: true, approve: false } })
    }
    const registriesStoreGetters = Object.assign({}, DEFAULT_REGISTRIES_STORE_GETTERS, {
      drillerOptions: jest.fn().mockReturnValue(fakeDrillerOptions),
      searchResponse: jest.fn().mockReturnValue(fakePersonList),
      loading: () => false,
      listError: () => {
        return { status: '400', statusText: 'error!' }
      },
      cityList: () => [],
      activity: () => 'DRILL'
    })
    const store = new Vuex.Store({
      modules: {
        auth: { getters: authGetters },
        registriesStore: { namespaced: true, getters: registriesStoreGetters, actions: DEFAULT_REGISTRIES_STORE_ACTIONS, mutations: DEFAULT_REGISTIES_STORE_MUTATIONS }
      }
    })
    const wrapper = shallowMount(SearchHome, {
      store,
      localVue
    })

    const downloadlinks = wrapper.findAll('#searched-registry-download a')
    expect(downloadlinks.length).toBe(2)
  })
})
