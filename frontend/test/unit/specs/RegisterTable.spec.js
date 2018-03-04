import { shallow, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import RegisterTable from '@/registry/components/RegisterTable'
import { FETCH_DRILLER_LIST } from '@/registry/store/actions.types'

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(VueRouter)

describe('RegisterTable.vue', () => {
  let store
  let getters
  let actions

  beforeEach(() => {
    getters = {
      user: () => {},
      loading: () => false,
      listError: () => null,
      drillers: () => {
        return {
          next: 'http://www.example.com/next/',
          previous: null,
          results: [
            {
              person_guid: '1',
              first_name: 'Bob',
              surname: 'Driller'
            },
            {
              person_guid: '2',
              first_name: 'Rob',
              surname: 'Well'
            }
          ]
        }
      }
    }
    actions = {
      [FETCH_DRILLER_LIST]: () => { return null }
    }
    store = new Vuex.Store({ getters, actions })
  })

  it('has a row for every person', () => {
    const wrapper = shallow(RegisterTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    expect(wrapper.findAll('#registry-table-row').length)
      .to.equal(2)
  })

  it('has the right people in each row', () => {
    const wrapper = shallow(RegisterTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    // first row
    expect(wrapper.findAll('#registry-table-row').at(0).text())
      .to.contain('Driller')
    expect(wrapper.findAll('#registry-table-row').at(0).text())
      .to.not.contain('Well')
    expect(wrapper.findAll('#registry-table-row').at(1).text())
      .to.contain('Well')
    expect(wrapper.findAll('#registry-table-row').at(1).text())
      .to.not.contain('Driller')
  })
  it('shows the pagination button for next page when a link is returned by API', () => {
    const wrapper = shallow(RegisterTable, {
      store,
      localVue,
      stubs: ['router-link', 'router-view']
    })
    expect(wrapper.find('#table-pagination-next').text()).to.equal('Next')
  })
})
