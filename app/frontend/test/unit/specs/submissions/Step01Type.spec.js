import { shallowMount, createLocalVue } from '@vue/test-utils'
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
                well_subclass_code: 'DOMESTIC',
                description: 'Domestic'
              },
              {
                well_subclass_guid: '321xyz',
                well_subclass_code: 'NON_DOMEST',
                description: 'Non Domestic'
              }
            ]
          }
        ]
      }),
      userRoles: () => ({
        wells: {
          edit: true
        }
      })
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

    expect(wrapper.vm.subclasses.length).toBe(2)
    expect(wrapper.vm.subclasses[0].well_subclass_code).toBe('DOMESTIC')
  })
})
