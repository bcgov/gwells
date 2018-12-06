import Lithology from '@/submissions/components/lithology.js'

describe('Lithology.js', () => {
  it('parses and sorts soil/rock terms', () => {
    // all of these cases will be checked
    // running parseSoilTerms() on the test string should result in the 'want' array
    const cases = [
      { test: 'wet gravel', want: ['gravel'] },
      { test: 'compact silty sand, some clay, wet', want: ['sand', 'silt', 'clay'] },
      { test: 'water bearing sands, trace gravel, loose', want: ['sand', 'gravel'] },
      { test: 'silty sand and gravel', want: ['sand', 'gravel', 'silt'] },
      { test: 'sand and gravel, silty', want: ['sand', 'gravel', 'silt'] },
      { test: 'silty SAND and GRAVEL', want: ['sand', 'gravel', 'silt'] },
      { test: 'weathered granite', want: ['granite'] },
      { test: 'trees and grass', want: [] }
    ]

    // loop through each test case
    for (let i = 0; i < cases.length; i++) {
      const lith = new Lithology(cases[i].test)
      const soils = lith.parseSoilTerms()

      // test that each array has the same members in the same order
      for (let j = 0; j < cases[i].want.length; j++) {
        expect(soils[j]).toBe(cases[i].want[j])
      }
      expect(soils.length).toBe(cases[i].want.length)
    }
  })

  it('parses colour terms', () => {
    // mock colour terms to check against
    const VALID_COLOURS = [
      {
        'lithology_colour_code': 'BROWN',
        'description': 'Brown'
      },
      {
        'lithology_colour_code': 'GREY',
        'description': 'Grey'
      }
    ]

    const cases = [
      { test: 'wet gravel, brown', want: 'BROWN' },
      { test: 'compact silty sand, some clay, wet, grey', want: 'GREY' }
    ]

    for (let i = 0; i < cases.length; i++) {
      const lith = new Lithology(cases[i].test)
      const colour = lith.colour(VALID_COLOURS)

      expect(colour).toBe(cases[i].want)
    }
  })

  it('parses moisture terms', () => {
    // define some mock moisture terms (in the application, these will come from the database)
    const VALID_MOISTURE = [
      {
        'lithology_moisture_code': 'DRY',
        'description': 'Dry'
      },
      {
        'lithology_moisture_code': 'WET',
        'description': 'Wet'
      }
    ]

    const cases = [
      { test: 'wet gravel, brown', want: 'WET' },
      { test: 'compact silty sand, some clay, dry, grey', want: 'DRY' }
    ]

    for (let i = 0; i < cases.length; i++) {
      const lith = new Lithology(cases[i].test)
      const moisture = lith.moisture(VALID_MOISTURE)

      expect(moisture).toBe(cases[i].want)
    }
  })

  it('parses hardness terms', () => {
    // mock hardness terms to check against
    const VALID_HARDNESS = [
      {
        'lithology_hardness_code': 'VERY_DENSE',
        'description': 'Very Dense'
      },
      {
        'lithology_hardness_code': 'HARD',
        'description': 'Hard'
      }
    ]

    const cases = [
      { test: 'wet gravel, brown, very dense', want: 'VERY_DENSE' },
      { test: 'HARD SILT, DRY', want: 'HARD' },
      { test: 'sand', want: '' }
    ]

    for (let i = 0; i < cases.length; i++) {
      const lith = new Lithology(cases[i].test)
      const hardness = lith.hardness(VALID_HARDNESS)

      expect(hardness).toBe(cases[i].want)
    }
  })
})
