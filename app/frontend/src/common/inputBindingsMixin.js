/**
 * inputBindingsMixin makes two-way bindings available for props declared
 * on a component, by added a computed property with a getter and setter
 * for each property. The convention used is to create a computed property with "Input" appended
 * to the original property name. E.g. property "name" will have corresponding computed property "nameInput"
 *
 * Declare which properties to ignore, by adding "twoWayBinding = false" to the property definition.
 *
 *    props: {
 *      name: {
 *        twoWayBinding = false
 *      }
 *    }
 *
 * then use v-model to sync:
 *
 *    <input v-model="nameInput"/>
 *
 */

const inputBindingsMixin = {
  beforeCreate () {
    // TODO: I propose getting rid of the fields
    const fields = this.$options.fields
    if (fields) {
      const props = Object.keys(this.$options.props)
      if (!this.$options.computed) {
        this.$options.computed = {}
      }
      Object.keys(fields).forEach(key => {
        if (!props.includes(fields[key])) {
          console.warn(`Field ${key} declared in fields but corresponding prop ${fields[key]} is missing`)
        }
        this.$options.computed[key] = {
          get () {
            return this[fields[key]]
          },
          set (val) {
            this.$emit(`update:${fields[key]}`, val)
          }
        }
      })
    } else {
      // If you haven't specified fields, then just iterate through the props
      const props = Object.keys(this.$options.props)
      props.forEach(key => {
        if (this.$options.props[key].isInput !== false) {
          const inputKey = `${key}Input`
          this.$options.computed[inputKey] = {
            get () {
              return this[key]
            },
            set (val) {
              this.$emit(`update:${key}`, val)
            }
          }
        }
      })
    }
  }
}

export default inputBindingsMixin
