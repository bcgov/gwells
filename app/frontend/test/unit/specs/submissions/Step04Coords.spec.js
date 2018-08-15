import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import Step04Coords from '@/submissions/components/SubmissionForm/Step04Coords.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Step04Coords.vue', () => {
  let store
  let getters

  beforeEach(() => {
    getters = {
      codes: () => ({}),
      userRoles: () => ({})
    }
    store = new Vuex.Store({
      getters
    })
  })

  it('accepts valid latitude input', () => {
    const wrapper = shallowMount(Step04Coords, {
      localVue,
      store,
      sync: false
    })

    const invalidLats = [{
      deg: 267,
      min: 0,
      sec: 0
    },
    {
      deg: 1,
      min: 61,
      sec: 0
    },
    {
      deg: 1,
      min: 25,
      sec: 99
    }]
    const validLats = [{
      deg: 67,
      min: 0,
      sec: 0
    },
    {
      deg: 0,
      min: 0,
      sec: 0
    }]

    let lat

    invalidLats.forEach(x => {
      lat = wrapper.vm.validDMSLat(x)
      expect(lat).toBe(false)
    })
    validLats.forEach(x => {
      lat = wrapper.vm.validDMSLat(x)
      expect(lat).toBe(true)
    })
  })
})
