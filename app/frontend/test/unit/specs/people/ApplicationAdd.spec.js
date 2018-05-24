import { shallowMount, createLocalVue } from '@vue/test-utils'
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
    const wrapper = shallowMount(ApplicationAdd, {
      store,
      propsData: { activity },
      localVue
    })
    expect(wrapper.find('.card-title').text()).toContain('Classification & Qualifications')
  })
  it('Loads driller options correctly', () => {
    const activity = 'DRILL'
    const wrapper = shallowMount(ApplicationAdd, {
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
    const wrapper = shallowMount(ApplicationAdd, {
      store,
      propsData: { activity },
      localVue
    })
    const option = wrapper.find('input[type="radio"][value="GEOTECH"]')
    option.trigger('click')
    expect(wrapper.vm.qualificationForm.qualifications).toEqual(['MON', 'REM', 'GEO'])
  })
})
