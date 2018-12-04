const isUpper = (word) => {
  return word === word.toUpperCase() && word !== word.toLowerCase()
}

const splitWords = (original) => {
  // replace commonly used punctuation
  const strippedPunctuation = original.replace(/[\,\-\:\\\/;\.\?&()]+/g, ' ')

  // replace extra whitespace with 1 space
  const strippedSpaces = strippedPunctuation.replace(/\s+/g, ' ')
  return strippedSpaces.split(' ')
}

const classify = (word, prev) => {
  word = word.toLowerCase()
  prev = prev.toLowerCase()

  if ((prev !== 'some') && (prev !== 'trace') && (prev !== 'and')) {
    prev = ''
  }

  const wordlist = []
  const suffixes = ['s', 'y', 'ey', 'ly']

  for (let i; i < suffixes.length; i++) {
    if word.endsWith(suffixes[i]) {
      wordlist.push([

      ])
    }
  }

  wordList.push([
    word
  ])

}

class Lithology {
  constructor (description) {
    this.original = description
  }

  parseSoilTerms () {
    const words = splitWords(this.original)
    const soils = []
    let inputIsAllCaps = true

    let prev = ''

    for (let i; i < words.length; i++) {
      const word = words[i]
      const soil = {}
      soil['capitalized'] = false

      // capitalized words are significant in soil classification, but many descriptions
      // in the existing database are all capital letters.
      // if we find an uncapitalized word, we can rule out "all caps" for this lithology description
      if (isUpper(word)) {
        soil['capitalized'] = true
      } else {
        inputIsAllCaps = false
      }

      const classifiedSoil = classify(word, prev)
    }
  }
}

export default Lithology
