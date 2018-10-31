const filterBlankRowsMixin = {
  methods: {
    // filter blank rows from an array (for example, casing_set, lithology_set)
    // this method will return a new array stripped of blank objects or objects
    // where all keys have null or empty string values
    filterBlankRows (set) {
      if (!set) {
        return []
      }

      return set.filter(item => {
        // check that item is an object, has keys and at least one of those keys
        // has a value (i.e. not null or empty string)
        return item.constructor === Object && Object.keys(item).length !== 0 && !Object.keys(item).every((key) => {
          return !item[key] && item[key] !== 0
        })
      })
    }
  }
}

export default filterBlankRowsMixin
