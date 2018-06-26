import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import ApplicationAddEdit from '@/registry/components/people/ApplicationAddEdit'
import { FETCH_DRILLER_OPTIONS } from '@/registry/store/actions.types'
import fakeOptions from '../fakeDrillerOptions'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('ApplicationAddEdit.vue', () => {
  describe('When loaded', () => {
    const getters = {
      drillerOptions: jest.fn().mockReturnValue(fakeOptions),
      loading: () => false
    }
    const actions = {
      [FETCH_DRILLER_OPTIONS]: jest.fn()
    }
    const store = new Vuex.Store({ getters, actions })
    const activity = 'DRILL'

    const wrapper = shallowMount(ApplicationAddEdit, {
      store,
      propsData: { activity, mode: 'add' },
      localVue
    })
    it('Has the correct title', () => {
      expect(wrapper.find('.card-title').text()).toContain('Classification & Qualifications')
    })
    it('Loads driller options correctly', () => {
      expect(wrapper.vm.formOptions.issuer.length).toBeGreaterThan(1)
      expect(wrapper.vm.formOptions.classifications.length).toBeGreaterThan(0)
      expect(wrapper.vm.formOptions.qualifications.length).toBeGreaterThan(0)
    })
    it('Has loaded proof of age options', () => {
      expect(wrapper.vm.formOptions.proofOfAge.length).toBeGreaterThan(0)
    })

    describe('When changing classification', () => {
      const option = wrapper.find('input[type="radio"][value="GEOTECH"]')
      option.trigger('click')
      it('results in qualifications changing', () => {
        expect(wrapper.vm.qualificationForm.qualifications).toEqual(['MON', 'REM', 'GEO'])
      })
    })
  })
})
