import { shallow, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import APIErrorMessage from '@/common/components/APIErrorMessage'
import { SET_ERROR } from '@/registry/store/mutations.types'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('APIErrorMessage.vue', () => {
  let mutations
  let store

  beforeEach(() => {
    mutations = {
      [SET_ERROR]: jest.fn()
    }

    store = new Vuex.Store({ mutations })
  })
  it('renders error text when error prop has an object', () => {
    const error = { status: '400', statusText: 'Error!', data: { detail: 'Whoa there! that\'s an error.' } }
    const wrapper = shallow(APIErrorMessage, {
      propsData: { error },
      localVue
    })
    const componentText = wrapper.find('#errorAlert').text()
    expect(componentText).toContain('400')
    expect(componentText).toContain('Error!')
    expect(componentText).toContain('Whoa there!')
  })
  it('tells store to remove error when the alert is clicked', () => {
    const error = { status: '400', statusText: 'Error!', data: { detail: 'Whoa there! that\'s an error.' } }
    const wrapper = shallow(APIErrorMessage, {
      propsData: { error, resetter: 'SET_ERROR' },
      store,
      localVue
    })
    wrapper.find('#errorAlert button.close').trigger('click')
    expect(mutations.SET_ERROR).toHaveBeenCalled()
  })
})
