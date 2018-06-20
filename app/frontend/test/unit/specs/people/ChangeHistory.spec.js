import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import VueMoment from 'vue-moment'
import ChangeHistory from '@/registry/components/people/ChangeHistory'

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
      drillers: () => [],
      userRoles: () => ({ edit: true, view: true, approve: true })
    }
    store = new Vuex.Store({ getters, actions, mutations })
  })

  it('renders and has a title', () => {
    const wrapper = shallowMount(ChangeHistory, {
      store,
      localVue,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $route: {params: {person_guid: 'aaaa-4444-bbbb-1111'}}
      }
    })
    expect(wrapper.find('#changeHistoryTitle').text()).toContain('History')
  })
  it('displays history records', () => {
    const wrapper = shallowMount(ChangeHistory, {
      store,
      localVue,
      stubs: ['router-link', 'router-view'],
      propsData: {
        resource: 'person',
        id: '123'
      },
      data () {
        return {
          history: JSON.parse(JSON.stringify([
            {
              'diff': {
                'pump_installer_orcs_no': '1234'
              },
              'prev': {
                'pump_installer_orcs_no': null
              },
              'user': 'TestUser2',
              'date': '2018-06-14T22:09:37.695000Z',
              'name': 'Person profile'
            },
            {
              'diff': {},
              'prev': {},
              'user': 'TestUser1',
              'date': '2018-06-09T00:38:04.358000Z',
              'name': 'Geoexchange Driller application',
              'created': true
            }
          ])),
          showHistory: true
        }
      }
    })
    expect(wrapper.find('#history-version-0').text()).toContain('to 1234')
    expect(wrapper.find('#history-version-0').text()).toContain('TestUser2')
    expect(wrapper.find('#history-version-0').text()).toContain('Person profile')
    expect(wrapper.find('#history-version-1').text()).toContain('created')
    expect(wrapper.find('#history-version-1').text()).toContain('TestUser1')
  })
})
