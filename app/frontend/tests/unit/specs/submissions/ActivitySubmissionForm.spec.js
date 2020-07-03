import '../../mocks/mapbox-gl'
import { shallowMount, mount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import ActivitySubmissionForm from '@/submissions/components/SubmissionForm/ActivitySubmissionForm'
import Lithology from '@/submissions/components/SubmissionForm/Lithology'

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(VueRouter)

const router = new VueRouter()

describe('ActivitySubmissionForm.vue', () => {
  it('renders components based on the activity selected (Yield exists on construction report', () => {
    const wrapper = shallowMount(ActivitySubmissionForm, {
      localVue,
      router,
      propsData: {
        sections: { wellYield: true },
        currentStep: null,
        form: {},
        activityType: 'CON',
        formSteps: {
          CON: ['wellYield']
        },
        formIsFlat: true
      }
    })

    expect(wrapper.vm.showSection('wellYield')).toBe(true)
  })

  it('renders components based on the activity selected (Yield does not exist on decommission report)', () => {
    const wrapper = shallowMount(ActivitySubmissionForm, {
      localVue,
      router,
      propsData: {
        sections: { },
        currentStep: null,
        form: {},
        activityType: 'DEC',
        formSteps: {
          DEC: ['something']
        },
        formIsFlat: true
      }
    })

    expect(wrapper.vm.showSection('wellYield')).toBe(false)
  })

  it('updates lithologydescription_set when lithology table is altered on Lithology child component', () => {
    let getters = {
      codes: () => ({})
    }
    let store = new Vuex.Store({
      getters
    })

    const wrapper = mount(ActivitySubmissionForm, {
      localVue,
      router,
      store,
      propsData: {
        sections: { lithology: true },
        currentStep: 'lithology',
        activityType: 'STAFF_EDIT',
        formSteps: {
          STAFF_EDIT: ['lithology']
        },
        isStaffEdit: true,
        formIsFlat: true,
        formSubmitLoading: false,
        formValueChanged: false,
        form: {
          lithologydescription_set: [{
            lithology_raw_data: '34',
            lithology_colour: 'black',
            lithology_hardness: 'hard',
            lithology_moisture: 'Dry',
            lithology_observation: 'test',
            lithology_description: 'basic'
          }]
        }
      }
    })

    wrapper.find(Lithology).vm.lithologyData.push({
      lithology_raw_data: '1',
      lithology_colour: 'white',
      lithology_hardness: 'test1322',
      lithology_moisture: 'Wet',
      lithology_observation: 'non',
      lithology_description: 'Solid'
    })

    expect(wrapper.vm.form.lithologydescription_set.length).toBe(2)
    expect(wrapper.vm.form.lithologydescription_set[1].lithology_hardness).toBe('test1322')
  })
})
