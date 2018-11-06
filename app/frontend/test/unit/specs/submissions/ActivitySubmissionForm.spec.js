import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import ActivitySubmissionForm from '@/submissions/components/SubmissionForm/ActivitySubmissionForm'

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(VueRouter)

const router = new VueRouter()

describe('ActivitySubmissionForm.vue', () => {
  beforeEach(() => {

  })

  it('renders components based on the activity selected (Yield exists on construction report', (done) => {
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
    wrapper.vm.$nextTick(() => {
      expect(wrapper.vm.show.wellYield).toBe(true)
      done()
    })
  })
  // it('renders components based on the activity selected (Yield does not exist on decommission report)', (done) => {
  //   const wrapper = shallowMount(ActivitySubmissionForm, {
  //     localVue,
  //     router,
  //     propsData: {
  //       sections: { },
  //       currentStep: null,
  //       form: {},
  //       activityType: 'DEC',
  //       formSteps: {
  //         DEC: ['something', 'wellYield']
  //       },
  //       formIsFlat: true
  //     }
  //   })
  //   wrapper.vm.$nextTick(() => {
  //     expect(wrapper.vm.show.wellYield).toBe(false)
  //     done()
  //   })
  // })
})
