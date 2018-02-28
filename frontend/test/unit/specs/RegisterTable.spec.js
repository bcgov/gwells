import { shallow, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import RegisterTable from '@/registry/components/RegisterTable'
import { FETCH_DRILLER_LIST } from '@/registry/store/actions.types'

const sinon = require('sinon')

const localVue = createLocalVue()
localVue.use(Vuex)

describe('RegisterTable.vue', () => {
  let store
  let getters
  let actions

  beforeEach(() => {
    getters = {
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
      [FETCH_DRILLER_LIST]: sinon.spy()
    }
    store = new Vuex.Store({ getters, actions })
  })

  it('has a row for every person', () => {
    const wrapper = shallow(RegisterTable, {
      store,
      localVue
    })
    expect(wrapper.findAll('#registry-table-row').length)
      .to.equal(2)


  })
  it('has the right people in each row', () => {
    const wrapper = shallow(RegisterTable, {
      store,
      localVue
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
      localVue
    })
    expect(wrapper.find('#table-pagination-next').text()).to.equal('Next')
  })
})
