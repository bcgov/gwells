import {
  shallow,
  mount,
  createLocalVue
} from '@vue/test-utils'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import SearchTable from '@/registry/components/search/SearchTable'
import {
  FETCH_DRILLER_LIST
} from '@/registry/store/actions.types'
import fakePersonList from '../fakePersonList.js'

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(VueRouter)

describe('SearchTable.vue', () => {
  let store
  let getters
  let actions

  beforeEach(() => {
    getters = {
      userIsAdmin: () => false,
      loading: () => false,
      listError: () => null,
      drillers: jest.fn().mockReturnValue(fakePersonList)
    }
    actions = {
      [FETCH_DRILLER_LIST]: jest.fn()
    }
    store = new Vuex.Store({
      getters,
      actions
    })
  })

  it('has a row for every person', () => {
    const wrapper = shallow(SearchTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    expect(wrapper.findAll('#registry-table tr').length)
      .toEqual(2)
  })

  it('has the right people in each row', () => {
    const wrapper = shallow(SearchTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    wrapper.setData({
      activity: 'Well Driller'
    })
    // first row
    expect(wrapper.find('#registry-table #drillerName0').text())
      .toContain('Bob')
    expect(wrapper.find('#registry-table #drillerName0').text())
      .not.toContain('Don')
    expect(wrapper.find('#registry-table #drillerName1').text())
      .toContain('Don')
    expect(wrapper.find('#registry-table #drillerName1').text())
      .not.toContain('Bob')
  })
  it('shows the pagination button for next page when a link is returned by API', () => {
    const wrapper = shallow(SearchTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    expect(wrapper.find('#table-pagination-next').text()).toEqual('Next')
  })
  it('shows the pagination button for previous page when a link is returned by API', () => {
    const wrapper = shallow(SearchTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    expect(wrapper.find('#table-pagination-prev').text()).toEqual('Previous')
  })
  it('dispatches fetch driller list with correct querystring when pagination next clicked', () => {
    const wrapper = shallow(SearchTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    wrapper.find('#table-pagination-next').trigger('click')
    expect(actions.FETCH_DRILLER_LIST.mock.calls[0][1]).toEqual({
      limit: '30',
      offset: '60'
    })
  })
  it('dispatches fetch driller list with correct querystring when pagination prev clicked', () => {
    const wrapper = shallow(SearchTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    wrapper.find('#table-pagination-prev').trigger('click')
    expect(actions.FETCH_DRILLER_LIST.mock.calls[0][1]).toEqual({
      limit: '30',
      offset: '0'
    })
  })
  it('emits the column code (e.g. surname) to be sorted when column sort button clicked', () => {
    const wrapper = shallow(SearchTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    wrapper.find('th i').trigger('click')
    expect(wrapper.emitted('sort')).toEqual([
      ['surname']
    ])
  })
  it('has the right columns when searching for drillers', () => {
    const wrapper = shallow(SearchTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    wrapper.setProps({
      activity: 'DRILL'
    })
    const tableHeaders = wrapper.findAll('th')
    const expectedHeaders = [
      'Name',
      'Company Name',
      'Company Address',
      'Contact Information',
      'Class of Driller',
      'Certificate Issued By',
      'Registration Status'
    ]
    expect(tableHeaders.length).toEqual(6)
    for (let i = 0; i < tableHeaders.length; i++) {
      expect(tableHeaders.wrappers[i].text()).toEqual(expectedHeaders[i])
    }
  })
  it('has the right columns when searching for well pump installers', () => {
    const wrapper = shallow(SearchTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    wrapper.setProps({
      activity: 'PUMP'
    })
    const tableHeaders = wrapper.findAll('th')
    const expectedHeaders = [
      'Name',
      'Company Name',
      'Company Address',
      'Contact Information',
      'Certificate Issued By',
      'Registration Status'
    ]
    expect(tableHeaders.length).toEqual(5)
    for (let i = 0; i < tableHeaders.length; i++) {
      expect(tableHeaders.wrappers[i].text()).toEqual(expectedHeaders[i])
    }
  })
  it('shows the organization name for each driller', () => {
    const wrapper = mount(SearchTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    wrapper.setData({
      activity: 'DRILL'
    })
    const personOrg = wrapper.find('#personOrg0').text()
    expect(personOrg).toEqual('Drillerson Drilling Ltd.')
  })
  it('shows the driller\'s organization address', () => {
    const wrapper = mount(SearchTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    wrapper.setData({
      activity: 'DRILL'
    })
    const personAddress = wrapper.find('#personAddress0').text()
    expect(personAddress).toContain('1111 Industrial St')
    expect(personAddress).toContain('Victoria, BC')
  })
  it('shows the driller\'s contact info', () => {
    const wrapper = mount(SearchTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    wrapper.setData({
      activity: 'DRILL'
    })
    const personContact = wrapper.find('#personContact0').text()
    expect(personContact).toContain('driller1@example.com')
  })
  it('shows the driller\'s subactivities', () => {
    const wrapper = mount(SearchTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    wrapper.setData({
      activity: 'DRILL'
    })
    const personSubActivity = wrapper.find('#personSubActivity0').text()
    expect(personSubActivity).toContain('Water Well Driller')
    expect(personSubActivity).toContain('Geoexchange Driller')
    expect(personSubActivity).not.toContain('Environmental')
  })
  it('shows the driller\'s certificate authority', () => {
    const wrapper = mount(SearchTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    wrapper.setData({
      activity: 'DRILL'
    })
    const personCertAuth = wrapper.find('#certAuth0').text()
    expect(personCertAuth).toContain('BC')
  })
  it('shows the driller\'s registration status', () => {
    getters = {
      userIsAdmin: () => true,
      user: () => 'user',
      loading: () => false,
      listError: () => null,
      drillers: jest.fn().mockReturnValue(fakePersonList)
    }
    store = new Vuex.Store({
      getters,
      actions
    })
    const wrapper = mount(SearchTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    wrapper.setData({
      activity: 'DRILL'
    })
    const personRegStatus = wrapper.find('#personRegStatus0').text()
    expect(personRegStatus).toContain('Active')
  })
})
