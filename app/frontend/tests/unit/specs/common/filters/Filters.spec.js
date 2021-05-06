import { excludeZeroDecimals } from '@/common/filters'

const excludeZeroDecimalsFixture = [
  { was: 1.500, should: 1.5 },
  { was: 1.000, should: 1 },
  { was: 1.006, should: 1.006 },
  { was: 5555.12000000, should: 5555.12 },
  { was: 1, should: 1 },
  { was: 1.456, should: 1.456 },
  { was: 3.141592653589000, should: 3.141592653589000 },
  { was: 1.45600000000000, should: 1.45600000000000 },
  { was: 3.141, should: 3.141 },
  { was: 'A', should: 'A' },
  { was: { a: '1' }, should: { a: '1' } },
  { was: null, should: null },
  { was: undefined, should: undefined },
  { was: '', should: '' },
  { was: ' ', should: ' ' }
]

describe('filters', () => {
  it('prove excludeZeroDecimals', () => {
    excludeZeroDecimalsFixture.forEach(c => {
      expect(excludeZeroDecimals(c.was)).toEqual(c.should)
    })
  })
})
