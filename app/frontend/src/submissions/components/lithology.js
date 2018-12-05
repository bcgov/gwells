/*
Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/

// default valid soil types
// these can be overrided if the application provides a list
const VALID_SOILS = [
  'gravel',
  'sand',
  'clay',
  'silt',
  'hardpan',
  'soil',
  'muskeg',
  'topsoil',
  'mud',
  'till',
  'organic',
  'boulder',
  'pebbles',
  'cobble'
]

// default valid bedrock types
const VALID_BEDROCK = [
  'bedrock',
  'mudstone',
  'granite',
  'conglomerate',
  'granodiorite',
  'basalt',
  'sandstone',
  'shale',
  'rock',
  'gneiss',
  'quartz',
  'quartzite',
  'limestone',
  'volcanics',
  'feldspar'
]

// checks if a string is all uppercase
const isUpper = (word) => {
  return word === word.toUpperCase() && word !== word.toLowerCase()
}

// splitWords takes a string, removes common punctuation and returns an array of words
const splitWords = (original) => {
  // replace commonly used punctuation
  const strippedPunctuation = original.replace(/[,\-\\:/;.?&()]+/g, ' ')

  // replace extra whitespace with 1 space
  const strippedSpaces = strippedPunctuation.replace(/\s+/g, ' ')
  return strippedSpaces.split(' ')
}

// classify takes a word (and the previous word) and tries to determine if that
// word is a valid soil/bedrock term.  It also tries to determine the importance of the word
// based on the suffix and previous word.
const classify = (word, prev, soilTerms = [], rockTerms = []) => {
  word = word.toLowerCase()
  prev = prev.toLowerCase()

  if ((prev !== 'some') && (prev !== 'trace') && (prev !== 'and')) {
    prev = ''
  }

  // suffixes like 'ey' (as in clayey) get a modifier of 'y' to denote clayey, gravelly etc.
  // these often come before the primary consistituent but are always less significant.
  // a suffix of 's' likely comes from 'sands', 'gravels' etc. and keep the previous word
  // as a modifier (as in 'some sands').
  const suffixes = [
    { suffix: 's', modifier: prev },
    { suffix: 'y', modifier: 'y' },
    { suffix: 'ey', modifier: 'y' },
    { suffix: 'ly', modifier: 'y' }
  ]

  // build a list of words to test in order (this allows testing varations of a term to check
  // for different suffixes/modifiers)
  const wordlist = [
    [word, prev]
  ]

  for (let i = 0; i < suffixes.length; i++) {
    if (word.endsWith(suffixes[i].suffix)) {
      const trimmedWord = word.slice(0, -(suffixes[i].suffix).length)
      wordlist.push([
        trimmedWord, suffixes[i].modifier
      ])
    }
  }

  for (let i = 0; i < wordlist.length; i++) {
    if (soilTerms.includes(wordlist[i][0])) {
      return {
        original: word,
        term: wordlist[i][0],
        modifier: wordlist[i][1],
        class: 'soil'
      }
    }
    if (rockTerms.includes(wordlist[i][0])) {
      return {
        original: word,
        term: wordlist[i][0],
        modifier: wordlist[i][1],
        class: 'bedrock'
      }
    }
  }

  // did not match either a valid soil or bedrock
  return null
}

// sortSoils sorts soil terms in order of significance
// capitalized words go first (if sorting by capitalization is on) followed
// by words that are not "qualified" or "modified" (e.g. unqualified: silt; qualified: trace silt)
const sortSoils = (soils, capitalization = false) => {
  // groupA: capitalized words. these are assumed to be the most important terms.
  // groupB: unqualified terms.  these are usually the first in the description
  // groupC: qualified terms like "silty" or "trace clay"
  let groupA = []
  let groupB = []
  let groupC = []

  for (let i = 0; i < soils.length; i++) {
    const soil = soils[i]

    if (soil.capitalized && capitalization && (soil.modifier === '' || soil.modifier === 'and')) {
      // capitalized soils (when sorting by capitalization is on) with no modifier get put first
      groupA.push(soil)
    } else if (soil.modifier === '' || soil.modifier === 'and') {
      // all uncapitalized soils with no qualifying term (e.g. just 'sand' as opposed to 'some sand')
      groupB.push(soil)
    } else {
      // all 'modified' or qualified soils (e.g. silty, some clay, trace sand etc.)
      groupC.push(soil)
    }
  }
  return groupA.concat(groupB).concat(groupC)
}

// Lithology represents a lithology or soil unit description.
// a string 'description' is required.
// arrays of valid soilTerms and rockTerms are optional.
//
// parseSoilTerms() returns an array of valid soil and rock terms
// ordered from most significant (primary soil type) to least significant.
// Usage:
// const soil = new Lithology('sand and gravel')
// const validSoils = soil.parseSoilTerms()    // === ['sand', 'gravel']
class Lithology {
  constructor (description, soilTerms = VALID_SOILS, rockTerms = VALID_BEDROCK) {
    this.original = description
    this.soilTerms = soilTerms
    this.rockTerms = rockTerms
  }

  // parseSoilTerms classifies and sorts a description and returns a list of valid soil/rock terms
  // ranked in order of importance
  parseSoilTerms () {
    const words = splitWords(this.original)
    let soils = []
    let inputIsAllCaps = true

    let prev = ''

    for (let i = 0; i < words.length; i++) {
      const word = words[i]
      let soil = {
        // start the soil object off with a capitalized property
        capitalized: false
      }

      // capitalized words are significant in soil classification, but many descriptions
      // in the existing database are all capital letters.
      // if we find an uncapitalized word, we can rule out "all caps" for this lithology description
      if (isUpper(word)) {
        soil.capitalized = true
      } else {
        inputIsAllCaps = false
      }

      // try to classify the soil into a valid soil or rock type
      const classifiedSoil = classify(word, prev, this.soilTerms, this.rockTerms)
      if (classifiedSoil) {
        soil = Object.assign(soil, classifiedSoil)
        soils.push(soil)
      }
      prev = word
    }

    // sort soils by order of importance
    const sorted = sortSoils(soils, !inputIsAllCaps) || []

    // return an array of just the valid soil/rock terms
    return sorted.map((soil) => soil.term)
  }
}

export default Lithology
