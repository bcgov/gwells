import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import VueMoment from 'vue-moment'
import Notes from '@/registry/components/people/Notes'
import fakePerson from '../fakePerson'

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(VueMoment)

describe('Notes.vue', () => {
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
    store = new Vuex.Store({ getters, actions, mutations })
  })

  it('renders and has a title', () => {
    const wrapper = shallowMount(Notes, {
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
    // our fake person has 1 note, so $note-0 should render
    const wrapper = shallowMount(Notes, {
      store,
      localVue,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: {params: {person_guid: 'aaaa-4444-bbbb-1111'}}
      }
    })
    wrapper.setProps({ type: 'person', guid: fakePerson.person_guid, record: fakePerson })
    expect(wrapper.find('#note-0').text()).toContain('A new note')
    expect(wrapper.find('#note-0').text()).toContain('Test User')
  })
})
