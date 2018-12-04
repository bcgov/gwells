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
      { test: 'silty SAND and GRAVEL', want: ['sand', 'gravel', 'silt'] }

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
})
