import { shallow, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import PersonEdit from '@/registry/components/PersonEdit'
import APIErrorMessage from '@/common/components/APIErrorMessage'
import { SET_DRILLER } from '@/registry/store/mutations.types'
import { FETCH_DRILLER } from '@/registry/store/actions.types'
import fakePerson from './fakePerson.js'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('PersonEdit.vue', () => {
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
      drillers: () => []
    }
    mutations = {
      [SET_DRILLER]: jest.fn()
    }
    actions = {
      [FETCH_DRILLER]: jest.fn()
    }
    store = new Vuex.Store({ getters, actions, mutations })
  })

  it('dispatches the fetch driller action when page loads if the current driller is not the right one', () => {
    shallow(PersonEdit, {
      store,
      localVue,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: {params: {person_guid: 'aaaa-4444-bbbb-1111'}}
      }
    })
    expect(actions.fetchDriller).toHaveBeenCalled()
  })
  it('loads the error component if there is an error', () => {
    getters = {
      loading: () => false,
      user: () => null,
      error: () => {
        return { status: '400', statusText: 'error!' }
      },
      currentDriller: jest.fn().mockReturnValue(fakePerson),
      drillers: () => []
    }
    const storeError = new Vuex.Store({ getters, actions, mutations })
    const wrapper = shallow(PersonEdit, {
      store: storeError,
      localVue,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: {params: {person_guid: fakePerson.person_guid}}
      }
    })
    expect(wrapper.findAll(APIErrorMessage).length).toEqual(1)
  })
  it('doesn\'t load the error component if there is no error', () => {
    const wrapper = shallow(PersonEdit, {
      store,
      localVue,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: {params: {person_guid: fakePerson.person_guid}}
      }
    })
    expect(wrapper.findAll(APIErrorMessage).length).toEqual(0)
  })
  it('has a classifications property (based on the currentDriller loaded)', () => {
    const wrapper = shallow(PersonEdit, {
      store,
      localVue,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: {params: {person_guid: fakePerson.person_guid}}
      }
    })
    expect(wrapper.vm.classifications).toEqual([
      {
        'code': 'geotech',
        'date': '2005-01-05',
        'description': 'Geotechnical/Environmental Driller',
        'status': 'Approved'
      },
      {
        'code': 'water',
        'date': '2005-01-05',
        'description': 'Water Well Driller',
        'status': 'Approved'}
    ])
  })
})
