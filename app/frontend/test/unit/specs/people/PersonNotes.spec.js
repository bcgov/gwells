import { shallow, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import VueMoment from 'vue-moment'
import PersonNotes from '@/registry/components/people/PersonNotes'
import fakePerson from '../fakePerson'

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(VueMoment)

describe('PersonNotes.vue', () => {
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
    const wrapper = shallow(PersonNotes, {
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
    const wrapper = shallow(PersonNotes, {
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
