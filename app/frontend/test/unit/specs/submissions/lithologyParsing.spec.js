import Lithology from '@/submissions/components/lithology.js'

describe('Lithology', () => {
  it('Splits up a string into words', () => {
    const desc1 = new Lithology('sand, gravelly, some silt')

    // some input comes with a variety of punctuation
    const desc2 = new Lithology('Sand&gravel/silt,,,clay')

    expect(desc1.splitWords().length).toBe(4)
    expect(desc2.splitWords().length).toBe(4)
    expect(desc2.splitWords()[0]).toBe('Sand')
    expect(desc2.splitWords()[1]).toBe('gravel')
    expect(desc2.splitWords()[2]).toBe('silt')
    expect(desc2.splitWords()[3]).toBe('clay')
  })
})
