import { shallow, createLocalVue } from '@vue/test-utils'
import ClassificationAdd from '@/registry/components/ClassificationAdd'

const localVue = createLocalVue()

describe('ClassificationAdd.vue', () => {
  it('dispatches the fetch driller action when page loads', () => {
    const wrapper = shallow(ClassificationAdd, { localVue })
    expect(wrapper.find('#classificationAddHeading').text()).toEqual('Classification and Qualifications')
  })
  it('has a property quals that contains a list of qualification codes', () => {
    const wrapper = shallow(ClassificationAdd, { localVue })
    // the default is DRILL, which has 6 qualification codes
    expect(wrapper.vm.qualType).toEqual('DRILL')
    expect(wrapper.vm.quals).toEqual(['WAT', 'MON', 'RECH', 'DEWAT', 'REM', 'GEO'])
  })
  it('updates editClassification.qualCodes when classification changes', () => {
    const wrapper = shallow(ClassificationAdd, { localVue })
    // the default is DRILL, which has 6 qualification codes
    expect(wrapper.vm.qualType).toEqual('DRILL')
    wrapper.setData({ qualType: 'GEOTECH' })
    expect(wrapper.vm.quals).toEqual(['MON', 'REM', 'GEO'])
    expect(wrapper.vm.editClassification.qualCodes).toEqual({
      wat: false,
      mon: true,
      rech: false,
      inj: false,
      dewat: false,
      rem: true,
      geo: true,
      clos: false
    })
  })
})
