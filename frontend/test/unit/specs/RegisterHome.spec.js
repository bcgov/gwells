import { shallow, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import RegisterHome from '@/registry/components/RegisterHome'
import RegisterTable from '@/registry/components/RegisterTable'
import APIErrorMessage from '@/common/components/APIErrorMessage'
import { FETCH_CITY_LIST, FETCH_DRILLER_LIST } from '@/registry/store/actions.types'

const sinon = require('sinon')

const localVue = createLocalVue()
localVue.use(Vuex)

describe('RegisterHome.vue', () => {
  let store
  let getters
  let actions

  beforeEach(() => {
    getters = {
      user: () => {},
      drillers: () => [],
      loading: () => false,
      listError: () => null,
      cityList: () => []
    }
    actions = {
      [FETCH_CITY_LIST]: sinon.spy(),
      [FETCH_DRILLER_LIST]: sinon.spy()
    }
    store = new Vuex.Store({ getters, actions })
  })

  it('renders the correct title', () => {
    const wrapper = shallow(RegisterHome, {
      store,
      localVue
    })
    expect(wrapper.find('#registry-title')
      .text().trim()).to.equal('Register of Well Drillers and Well Pump Installers')
  })

  it('tries to load the table component', () => {
    const wrapper = shallow(RegisterHome, {
      store,
      localVue
    })
    expect(wrapper.findAll(RegisterTable).length)
      .to.equal(1)
  })

  it('loads the error component if there is an error', () => {
    const getters = {
      user: () => {},
      drillers: () => [],
      loading: () => false,
      listError: () => {
        return { status: '400', statusText: 'error!' }
      },
      cityList: () => []
    }
    const store = new Vuex.Store({ getters, actions })
    const wrapper = shallow(RegisterHome, {
      store,
      localVue
    })
    expect(wrapper.findAll(APIErrorMessage).length)
      .to.equal(1)
  })

  it('doesn\'t load the error component if there is no error', () => {
    const wrapper = shallow(RegisterHome, {
      store,
      localVue
    })
    expect(wrapper.findAll(APIErrorMessage).length)
      .to.equal(0)
  })
})
