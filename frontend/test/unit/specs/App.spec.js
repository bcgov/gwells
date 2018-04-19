import { shallow, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import App from '@/registry/App.vue'
import Header from '@/common/components/Header.vue'
import Footer from '@/common/components/Footer.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('App.vue', () => {
  let store
  let getters
  let actions
  let mutations
  beforeEach(() => {
    getters = {
      error: () => null
    }
    store = new Vuex.Store({ getters, actions, mutations })
  })
  it('loads header and footer', () => {
    const wrapper = shallow(App, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    expect(wrapper.find(Header)).toBeDefined()
    expect(wrapper.find(Footer)).toBeDefined()
  })
})
