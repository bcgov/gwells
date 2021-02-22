import { mount, shallowMount, createLocalVue } from '@vue/test-utils'
import Vue from 'vue'
import Vuex from 'vuex'
import WellType from '@/submissions/components/SubmissionForm/WellType.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('WellType.vue', () => {
  let store
  let getters

  beforeEach(() => {
    getters = {
      codes: () => ({
        well_classes: [
          {
            well_class_code: 'WATR_SPPLY',
            description: 'Water Supply',
            wellsubclasscode_set: [
              {
                well_subclass_guid: '123abc',
                well_subclass_code: 'NA',
                description: 'Not Applicable'
              }
            ]
          },
          {
            well_class_code: 'UNK',
            description: 'Unknown',
            wellsubclasscode_set: []
          }
        ],
        intended_water_uses: [
          {
            intended_water_use_code: 'IRR',
            description: 'Irrigation'
          },
          {
            intended_water_use_code: 'NA',
            description: 'Not Applicable'
          }
        ]
      }),
      userRoles: () => ({
        wells: {
          edit: true
        }
      }),
      wells: () => {
        return []
      }
    }
    store = new Vuex.Store({
      getters
    })
  })

  it('computes valid subclasses from well class code options', () => {
    const wellClass = 'WATR_SPPLY'
    const wrapper = shallowMount(WellType, {
      localVue,
      store,
      propsData: { wellClass },
      sync: false
    })

    expect(wrapper.vm.subclasses.length).toBe(1)
    expect(wrapper.vm.subclasses[0].well_subclass_code).toBe('NA')
  })

  it('removes NA from intended water use dropdown when well class is WATR_SPPLY', () => {
    const wrapper = mount(WellType, {
      localVue,
      store,
      propsData: { wellClass: 'WATR_SPPLY' },
      sync: false
    })

    const intendedWaterUseSelectEl = wrapper.find('#intendedWaterUse select')

    expect(intendedWaterUseSelectEl.element).toBeDefined()
    expect(intendedWaterUseSelectEl.element.options.length).toEqual(2)
    expect(intendedWaterUseSelectEl.element.disabled).toEqual(false)
  })

  it('set intended water use to NA when well class is UNK', async () => {
    const wrapper = mount(WellType, {
      localVue,
      store,
      propsData: { wellClass: null, intendedWaterUse: null },
      sync: false
    })

    const wellClassSelectEl = wrapper.find('#wellClass select')
    const intendedWaterUseSelectEl = wrapper.find('#intendedWaterUse select')

    expect(intendedWaterUseSelectEl.element.disabled).toEqual(false)
    expect(intendedWaterUseSelectEl.element.value).toEqual('')

    wellClassSelectEl.setValue('UNK')
    await Vue.nextTick()

    // Form inputs trigger a change event that needs the parent will catch and update the props
    expect(wrapper.emitted()['update:wellClass']).toEqual([['UNK']])
    wrapper.setProps({ wellClass: 'UNK' })
    await Vue.nextTick()

    expect(wrapper.vm.wellClassInput).toEqual('UNK')
    // Form inputs trigger a change event that needs the parent will catch and update the props
    expect(wrapper.emitted()['update:intendedWaterUse']).toEqual([['NA']])

    wrapper.setProps({ intendedWaterUse: 'NA' })
    await Vue.nextTick()

    expect(wrapper.vm.intendedWaterUseInput).toEqual('NA')
    expect(intendedWaterUseSelectEl.element.disabled).toEqual(true)
  })
})
