const codeToDescription = {
  methods: {
    codeToDescription (content, code) {
      // this requires this.codes to be pulled in from the store.
      // if not available, default to returning the code
      if (!this.codes || !this.codes[content] || !code) {
        return code
      }

      // find a code/description set that matches the given code
      const codeDescriptionObject = this.codes[content].find((item) => {
        return Object.keys(item).some((key) => {
          return item[key] === code
        })
      })

      // if codeDescriptionObject didn't match any of the codes, just return
      // the original code.
      if (!codeDescriptionObject) {
        return code
      }

      return codeDescriptionObject.description || code
    }
  }
}

export default codeToDescription
