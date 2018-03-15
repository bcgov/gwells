import { shallow, createLocalVue } from '@vue/test-utils'
import Legal from '@/registry/components/Legal'

const localVue = createLocalVue()

describe('Legal.vue', () => {
  it('renders Well Driller text when activity prop is DRILL', () => {
    const activity = 'DRILL'
    const wrapper = shallow(Legal, {
      propsData: { activity },
      localVue
    })
    expect(wrapper.find('h3').text().trim()).toEqual('LEGAL DISCLAIMER FOR WELL DRILLER:')
  })
  it('renders pump installer text when activity prop is PUMP', () => {
    const activity = 'PUMP'
    const wrapper = shallow(Legal, {
      propsData: { activity },
      localVue
    })
    expect(wrapper.find('h3').text().trim()).toEqual('LEGAL DISCLAIMER FOR WELL PUMP INSTALLER:')
  })
})
