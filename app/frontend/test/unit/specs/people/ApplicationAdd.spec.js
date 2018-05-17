import { shallow, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import ApplicationAdd from '@/registry/components/people/ApplicationAdd'
import fakeOptions from '../fakeDrillerOptions'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('ApplicationAdd.vue', () => {
  let getters
  let actions
  let store

  beforeEach(() => {
    getters = {
      drillerOptions: jest.fn().mockReturnValue(fakeOptions),
      loading: () => false
    }
    actions = {
      fetchDrillerOptions: jest.fn()
    }
    store = new Vuex.Store({ getters, actions })
  })

  it('Has the correct title', () => {
    const activity = 'DRILL'
    const wrapper = shallow(ApplicationAdd, {
      store,
      propsData: { activity },
      localVue
    })
    expect(wrapper.find('.card-title').text()).toContain('Classification, Qualifications & Adjudication')
  })
  it('Loads driller options correctly', () => {
    const activity = 'DRILL'
    const wrapper = shallow(ApplicationAdd, {
      store,
      propsData: { activity },
      localVue
    })
    expect(wrapper.vm.formOptions.issuer.length).toBeGreaterThan(1)
    expect(wrapper.vm.formOptions.classifications.length).toBeGreaterThan(0)
    expect(wrapper.vm.formOptions.qualifications.length).toBeGreaterThan(0)
  })
  it('Changing classification, results in qualifications changing', () => {
    const activity = 'DRILL'
    const wrapper = shallow(ApplicationAdd, {
      store,
      propsData: { activity },
      localVue
    })
    const option = wrapper.find('input[type="radio"][value="GEOTECH"]')
    option.trigger('click')
    expect(wrapper.vm.qualificationForm.qualifications).toEqual(['MON', 'REM', 'GEO'])
  })
  // it('has a property quals that contains a list of qualification codes', () => {
  //   const wrapper = shallow(ApplicationAdd, { localVue })
  //   // the default is DRILL, which has 6 qualification codes
  //   expect(wrapper.vm.qualType).toEqual('DRILL')
  //   expect(wrapper.vm.quals).toEqual(['WAT', 'MON', 'RECH', 'DEWAT', 'REM', 'GEO'])
  // })
  // it('updates editClassification.qualCodes when classification changes', () => {
  //   const wrapper = shallow(ApplicationAdd, { localVue })
  //   // the default is DRILL, which has 6 qualification codes
  //   expect(wrapper.vm.qualType).toEqual('DRILL')
  //   wrapper.setData({ qualType: 'GEOTECH' })
  //   expect(wrapper.vm.quals).toEqual(['MON', 'REM', 'GEO'])
  //   expect(wrapper.vm.editClassification.qualCodes).toEqual({
  //     wat: false,
  //     mon: true,
  //     rech: false,
  //     inj: false,
  //     dewat: false,
  //     rem: true,
  //     geo: true,
  //     clos: false
  //   })
  // })
})
