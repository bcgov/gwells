import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import Surveys from '@/surveys/views/Surveys.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Surveys.vue', () => {
  let store
  let getters

  beforeEach(() => {
    getters = {
      codes: () => ({}),
      userRoles: () => ({
        surveys: { edit: true }
      })
    }
    store = new Vuex.Store({
      getters
    })
  })

  it('renders if authorized', () => {
    const wrapper = shallowMount(Surveys, {
      localVue,
      store
    })

    expect(wrapper.find('#surveyList').text()).toBe('Current Surveys')
  })
  it('shows an error if not authorized', () => {
    getters = {
      codes: () => ({}),
      userRoles: () => ({
        surveys: { edit: false }
      })
    }
    store = new Vuex.Store({
      getters
    })

    const wrapper = shallowMount(Surveys, {
      localVue,
      store
    })

    expect(wrapper.find('#loginMsg').text()).toBe('Please log in to continue.')
  })
})
