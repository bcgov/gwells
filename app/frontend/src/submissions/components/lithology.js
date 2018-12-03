class Lithology {
  constructor(description) {
    this.original = description
  }

  splitWords() {
    let singleWords = []
    // replace commonly used 
    const tidiedDescription = this.original.replace(/[\,\-\:\\\/;\.\?()]+/g, ' ')
    return tidiedDescription.split(' ')
  }
}