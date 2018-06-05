import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import OrganizationEdit from '@/registry/components/people/OrganizationEdit.vue'
import fakeCompanyList from '../fakeCompanyList'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('OrganizationEdit.vue', () => {
  let store
  let getters
  let mutations
  let actions

  beforeEach(() => {
    getters = {
      error: () => null
    }

    store = new Vuex.Store({ getters, actions, mutations })
  })
  it('has a title', () => {
    const wrapper = shallowMount(OrganizationEdit, {
      localVue,
      store,
      stubs: ['router-link', 'router-view', 'v-select']
    })
    expect(wrapper.find('h4.card-title').text()).toEqual('Manage Companies')
  })
  it('loads company details in the form when a company is selected', () => {
    const wrapper = shallowMount(OrganizationEdit, {
      localVue,
      store,
      stubs: ['router-link', 'router-view', 'v-select']
    })
    wrapper.setData({
      companies: fakeCompanyList,
      selectedCompany: fakeCompanyList[1]
    })
    expect(wrapper.vm.companyForm.name).toEqual('Big Time Drilling Ltd.')
  })
})
