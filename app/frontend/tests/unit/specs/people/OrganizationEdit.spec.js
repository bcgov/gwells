import { mount, shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import moxios from 'moxios'
import OrganizationEdit from '@/registry/components/people/OrganizationEdit.vue'
import fakeCompanyList from '../fakeCompanyList'
import { FETCH_DRILLER_OPTIONS } from '@/registry/store/actions.types'
import fakeOptions from '../fakeDrillerOptions'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('OrganizationEdit.vue', () => {
  let store

  beforeEach(() => {
    moxios.install()

    store = new Vuex.Store({
      modules: {
        registriesStore: {
          namespaced: true,
          getters: {
            error: () => null,
            drillerOptions: jest.fn().mockReturnValue(fakeOptions),
            provinceStateOptions: () => ['BC', 'AB']
          },
          actions: {
            [FETCH_DRILLER_OPTIONS]: jest.fn()
          },
          mutations: {
          }
        }
      }
    })
  })

  afterEach(() => {
    moxios.uninstall()
  })

  it('has a title', () => {
    const wrapper = mount(OrganizationEdit, {
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
