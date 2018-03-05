import { shallow, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import RegisterHome from '@/registry/components/RegisterHome'
import RegisterTable from '@/registry/components/RegisterTable'
import APIErrorMessage from '@/common/components/APIErrorMessage'
import { FETCH_CITY_LIST, FETCH_DRILLER_LIST, LOGIN, LOGOUT } from '@/registry/store/actions.types'

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
      [FETCH_CITY_LIST]: jest.fn(),
      [FETCH_DRILLER_LIST]: jest.fn(),
      [LOGIN]: jest.fn(),
      [LOGOUT]: jest.fn()
    }
    store = new Vuex.Store({ getters, actions })
  })

  it('renders the correct title', () => {
    const wrapper = shallow(RegisterHome, {
      store,
      localVue
    })
    expect(wrapper.find('#registry-title')
      .text().trim()).toEqual('Register of Well Drillers and Well Pump Installers')
  })

  it('loads the table component', () => {
    const wrapper = shallow(RegisterHome, {
      store,
      localVue
    })
    expect(wrapper.findAll(RegisterTable).length)
      .toEqual(1)
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
      .toEqual(1)
  })

  it('doesn\'t load the error component if there is no error', () => {
    const wrapper = shallow(RegisterHome, {
      store,
      localVue
    })
    expect(wrapper.findAll(APIErrorMessage).length)
      .toEqual(0)
  })
  it('dispatches the fetch driller list action when loaded', () => {
    shallow(RegisterHome, {
      store,
      localVue
    })
    expect(actions.fetchDrillers).toHaveBeenCalled()
  })
  it('resets search params when reset button is clicked', () => {
    const wrapper = shallow(RegisterHome, {
      store,
      localVue
    })
    wrapper.setData({
      searchParams: {
        search: 'Bob Driller',
        city: 'Anytown',
        activity: 'PUMP',
        status: 'INACTIVE',
        limit: '10'
      }
    })
    expect(wrapper.vm.searchParams).toEqual({
      search: 'Bob Driller',
      city: 'Anytown',
      activity: 'PUMP',
      status: 'INACTIVE',
      limit: '10'
    })
    wrapper.find('[type=reset]').trigger('reset')
    expect(wrapper.vm.searchParams).toEqual({
      search: '',
      city: '',
      activity: 'DRILL',
      status: 'ACTIVE',
      limit: '10'
    })
  })
  it('dispatches login action when login button is triggered', () => {
    const wrapper = shallow(RegisterHome, {
      store,
      localVue
    })
    wrapper.setData({
      loginPanelToggle: true
    })
    const button = wrapper.find('#loginButton')
    button.trigger('submit')
    expect(actions.login).toHaveBeenCalled()
  })
  it('dispatches logout action when login button is triggered', () => {
    const gettersWithUser = {
      user: function () { return { username: 'im-a-user!' } },
      drillers: () => [],
      loading: () => false,
      listError: () => null,
      cityList: () => []
    }
    const storeWithUser = new Vuex.Store({ getters: gettersWithUser, actions })
    const wrapper = shallow(RegisterHome, {
      store: storeWithUser,
      localVue
    })
    const button = wrapper.find('#logoutButton')
    button.trigger('click')
    expect(actions.logout).toHaveBeenCalled()
  })
  it('fetches a new city list when user changes professional type to pump installer')
})
