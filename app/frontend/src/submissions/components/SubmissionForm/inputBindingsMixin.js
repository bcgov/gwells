/**
 * inputBindingsMixin makes two-way bindings available for props declared
 * on a component, by added a computed property with a getter and setter
 * for each item listed in "fields"
 *
 * Declare which props to bind to by adding them to the fields object on the component
 * instance:
 *
 *    props: ['name'],
 *    fields: {
 *      nameInput: 'name'
 *    }
 *
 * then use v-model to sync:
 *
 *    <input v-model="nameInput"/>
 *
 */

const inputBindingsMixin = {
  beforeCreate () {
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
        this.$options.computed[`${key}`] = {
          get () {
            return this[fields[key]]
          },
          set (val) {
            this.$emit(`update:${fields[key]}`, val)
          }
        }
      })
    }
  }
}

export default inputBindingsMixin
