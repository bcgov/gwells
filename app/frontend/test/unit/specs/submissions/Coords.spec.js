import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import Coords from '@/submissions/components/SubmissionForm/Coords.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Coords.vue', () => {
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

  it('converts from WSG84 to UTM', () => {
    const wrapper = shallowMount(Coords, {
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
    const wrapper = shallowMount(Coords, {
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
  it('converts from decimal degrees to DMS', () => {
    const wrapper = shallowMount(Coords, {
      localVue,
      store,
      sync: false
    })

    const cases = [
      {
        test: [-144.5099, 48.50112],
        expected: {
          lat: {
            deg: '48',
            min: '30',
            sec: '4.03'
          },
          long: {
            deg: '-144',
            min: '30',
            sec: '35.64'
          }
        }
      }
    ]

    for (let i = 0; i < cases.length; i++) {
      const args = cases[i]['test']

      // longitude first
      let result = wrapper.vm.convertToDMS(args[0])

      expect(result.deg).toBe(cases[i].expected.long.deg)
      expect(result.min).toBe(cases[i].expected.long.min)
      expect(result.sec).toBe(cases[i].expected.long.sec)

      // latitude
      result = wrapper.vm.convertToDMS(args[1])

      expect(result.deg).toBe(cases[i].expected.lat.deg)
      expect(result.min).toBe(cases[i].expected.lat.min)
      expect(result.sec).toBe(cases[i].expected.lat.sec)
    }
  })
  it('converts from DMS to decimal degrees', () => {
    const wrapper = shallowMount(Coords, {
      localVue,
      store,
      sync: false
    })

    const cases = [
      {
        test: {
          lat: {
            deg: 49,
            min: 24,
            sec: 55.98
          },
          long: {
            deg: 142,
            min: 58,
            sec: 43.01
          }},
        expected: {
          latitude: '49.415550',
          longitude: '142.978614'
        }
      },
      {
        test: {
          lat: {
            deg: -49,
            min: 24,
            sec: 55.98
          },
          long: {
            deg: -142,
            min: 58,
            sec: 43.01
          }},
        expected: {
          latitude: '-49.415550',
          longitude: '-142.978614'
        }
      }
    ]

    for (let i = 0; i < cases.length; i++) {
      const args = cases[i]['test']

      let result = wrapper.vm.convertDMStoDeg(args.long)

      // longitude
      expect(result).toBe(cases[i].expected.longitude)

      // latitude
      result = wrapper.vm.convertDMStoDeg(args.lat)

      expect(result).toBe(cases[i].expected.latitude)
    }
  })
})
