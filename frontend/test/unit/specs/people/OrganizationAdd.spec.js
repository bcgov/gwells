import { shallow, createLocalVue } from '@vue/test-utils'
import OrganizationAdd from '@/registry/components/people/OrganizationAdd.vue'

const localVue = createLocalVue()
describe('OrganizationAdd.vue', () => {
  it('has a title', () => {
    const wrapper = shallow(OrganizationAdd, {
      localVue,
      stubs: ['router-link', 'router-view', 'v-select']
    })
    expect(wrapper.find('h5.modal-title').text()).toEqual('Add an Organization')
  })
  it('form has a reset button that clears fields', () => {
    const wrapper = shallow(OrganizationAdd, {
      localVue,
      stubs: ['router-link', 'router-view', 'v-select']
    })
    wrapper.vm.orgForm.name = 'Big Drilling Co'
    expect(wrapper.vm.orgForm.name).toEqual('Big Drilling Co')
    wrapper.find('#orgFormResetButton').trigger('reset')
    expect(wrapper.vm.orgForm.name).toEqual('')
  })
})
