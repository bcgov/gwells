import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import OrganizationAdd from '@/registry/components/people/OrganizationAdd.vue'
import { FETCH_DRILLER_OPTIONS } from '@/registry/store/actions.types'
import fakeOptions from '../fakeDrillerOptions'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('OrganizationAdd.vue', () => {
  let store
  let getters
  let mutations
  const actions = {
    [FETCH_DRILLER_OPTIONS]: jest.fn()
  }

  beforeEach(() => {
    getters = {
      error: () => null,
      drillerOptions: jest.fn().mockReturnValue(fakeOptions),
      provinceStateOptions: () => ['BC', 'AB']
    }

    store = new Vuex.Store({ getters, actions, mutations })
  })
  it('has a title', () => {
    const wrapper = shallowMount(OrganizationAdd, {
      localVue,
      store,
      stubs: ['router-link', 'router-view', 'v-select']
    })
    expect(wrapper.find('h5.modal-title').text()).toEqual('Add a Company')
  })
  it('form has a reset button that clears fields', () => {
    const wrapper = shallowMount(OrganizationAdd, {
      localVue,
      store,
      stubs: ['router-link', 'router-view', 'v-select']
    })
    wrapper.vm.orgForm.name = 'Big Drilling Co'
    expect(wrapper.vm.orgForm.name).toEqual('Big Drilling Co')
    wrapper.find('#orgFormResetButton').trigger('reset')
    expect(wrapper.vm.orgForm.name).toEqual('')
  })
})
