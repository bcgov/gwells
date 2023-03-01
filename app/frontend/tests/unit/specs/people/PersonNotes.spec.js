import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import VueMoment from 'vue-moment'
import PersonNotes from '@/registry/components/people/PersonNotes'
import fakePerson from '../fakePerson'

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(VueMoment)

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
      },
      actions: {        
      },
      mutations:{        
      }
    }        
  }  
}

describe('PersonNotes.vue', () => {
  let store
  let modules

  beforeEach(() => {
    modules = GET_DEFAULT_STORE_MODULES()
    store = new Vuex.Store({
      modules: modules
    })
  })

  it('renders and has a title', () => {
    const wrapper = shallowMount(PersonNotes, {
      store,
      localVue,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: {params: {person_guid: 'aaaa-4444-bbbb-1111'}}
      }
    })
    expect(wrapper.find('#notesSectionTitle').text()).toEqual('Notes')
  })
  it('displays notes', () => {
    // our fake person has 1 note, so $person-note-0 should render
    const wrapper = shallowMount(PersonNotes, {
      store,
      localVue,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: {params: {person_guid: 'aaaa-4444-bbbb-1111'}}
      }
    })
    expect(wrapper.find('#person-note-0').text()).toContain('A new note')
    expect(wrapper.find('#person-note-0').text()).toContain('Test User')
  })
})
