import { shallow, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import SearchTable from '@/registry/components/search/SearchTable'
import { FETCH_DRILLER_LIST } from '@/registry/store/actions.types'

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
      drillers: () => {
        return {
          next: 'http://www.example.com/api/?limit=30&offset=60',
          previous: 'http://www.example.com/api/?limit=30&offset=0',
          results: [
            {
              person_guid: '1e252dca-ccb9-439a-a6ec-aeec0f7e4a03',
              first_name: 'Bob',
              surname: 'Driller',
              organization_name: null,
              street_address: null,
              city: null,
              province_state: null,
              contact_tel: null,
              contact_email: null,
              activity: 'Well Driller',
              status: 'Active',
              registration_no: 'WD 08315530'
            },
            {
              person_guid: '1e252dca-ccb9-439a-a6ec-aeec0f7e4a02',
              first_name: 'Rob',
              surname: 'Well',
              organization_name: null,
              street_address: null,
              city: null,
              province_state: null,
              contact_tel: null,
              contact_email: null,
              activity: 'Well Driller',
              status: 'Active',
              registration_no: 'WD 08315531'
            }
          ]
        }
      }
    }
    actions = {
      [FETCH_DRILLER_LIST]: jest.fn()
    }
    store = new Vuex.Store({ getters, actions })
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
    wrapper.setData({activity: 'Well Driller'})
    // first row
    expect(wrapper.findAll('#registry-table tr').at(0).text())
      .toContain('Driller')
    expect(wrapper.findAll('#registry-table tr').at(0).text())
      .not.toContain('Well')
    expect(wrapper.findAll('#registry-table tr').at(1).text())
      .toContain('Well')
    expect(wrapper.findAll('#registry-table tr').at(1).text())
      .not.toContain('Driller')
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
    expect(actions.FETCH_DRILLER_LIST.mock.calls[0][1]).toEqual({limit: '30', offset: '60'})
  })
  it('dispatches fetch driller list with correct querystring when pagination prev clicked', () => {
    const wrapper = shallow(SearchTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    wrapper.find('#table-pagination-prev').trigger('click')
    expect(actions.FETCH_DRILLER_LIST.mock.calls[0][1]).toEqual({limit: '30', offset: '0'})
  })
  it('emits the column code (e.g. surname) to be sorted when column sort button clicked', () => {
    const wrapper = shallow(SearchTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    wrapper.find('th i').trigger('click')
    expect(wrapper.emitted('sort')).toEqual([['surname']])
  })
  it('has the right columns when searching for drillers', () => {
    const wrapper = shallow(SearchTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    wrapper.setProps({ activity: 'DRILL' })
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
    wrapper.setProps({ activity: 'PUMP' })
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
})
