import { shallow, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import OrganizationAdd from '@/registry/components/people/OrganizationAdd.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('OrganizationAdd.vue', () => {
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
    const wrapper = shallow(OrganizationAdd, {
      localVue,
      store,
      stubs: ['router-link', 'router-view', 'v-select']
    })
    expect(wrapper.find('h5.modal-title').text()).toEqual('Add a Company')
  })
  it('form has a reset button that clears fields', () => {
    const wrapper = shallow(OrganizationAdd, {
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
