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

  it('converts from WSG84 to UTM', () => {
    const wrapper = shallowMount(Step04Coords, {
      localVue,
      store,
      sync: false
    })

    const cases = [
      {
        test: [-123.370922, 48.419588],
        expected: {
          easting: 472556.02,
          northing: 5363003.85,
          zone: 10
        }
      },
      {
        test: [-120.504983, 49.462639],
        expected: {
          easting: 680786.83,
          northing: 5481879.63,
          zone: 10
        }
      },
      {
        test: [-120.336986, 59.630933],
        expected: {
          easting: 650161.61,
          northing: 6613321.83,
          zone: 10
        }
      },
      {
        test: [-138.907356, 59.981918],
        expected: {
          easting: 616773.56,
          northing: 6651244.21,
          zone: 7
        }
      }
    ]

    for (let i = 0; i < cases.length; i++) {
      const args = cases[i]['test']
      const result = wrapper.vm.convertToUTM(...args)
      expect(Number.parseFloat(result.easting).toFixed(2)).toBe(cases[i].expected.easting.toFixed(2))
      expect(Number.parseFloat(result.northing).toFixed(2)).toBe(cases[i].expected.northing.toFixed(2))
      expect(result.zone).toBe(cases[i].expected.zone)
    }
  })
  it('converts from UTM to WGS84', () => {
    const wrapper = shallowMount(Step04Coords, {
      localVue,
      store,
      sync: false
    })

    const cases = [
      {
        test: [472556.02, 5363003.85, 10],
        expected: {
          longitude: '-123.370922',
          latitude: '48.419588'
        }
      },
      {
        test: [616773.56, 6651244.21, 7],
        expected: {
          longitude: '-138.907356',
          latitude: '59.981918'
        }
      }
    ]

    for (let i = 0; i < cases.length; i++) {
      const args = cases[i]['test']
      const result = wrapper.vm.convertToWGS84(...args)
      expect(Number.parseFloat(result.longitude).toFixed(6)).toBe(cases[i].expected.longitude)
      expect(Number.parseFloat(result.latitude).toFixed(6)).toBe(cases[i].expected.latitude)
      expect(result.zone).toBe(cases[i].expected.zone)
    }
  })
})
