<template>
  <div :class="`grid grid-cols-12 gap-${gap}`">
    <template v-for="(component, index) in $slots.default()">
      <div :class="getClassNames(index)">
        <component :is="component"/>
      </div>
    </template>
  </div>
</template>

<script>

export default {
  props: {
    gap: {
      type: Number,
      default: 0
    },
    // Default col span
    cols: {
      type: [Number, Array],
      default: 12
    },
    // Col span for specific screen widths
    xs: [Number, Array],
    sm: [Number, Array],
    md: [Number, Array],
    lg: [Number, Array],
    xl: [Number, Array],
    innerDivClass: [String, Array],
  },
  methods: {
    getClassNames (index) {
      const classNames = []
      // Default column span
      if (this.cols) {
        if (Array.isArray(this.cols)) {
          if (this.cols[index]) {
            classNames.push(`col-span-${this.cols[index]}`)
          }
        } else {
          classNames.push(`col-span-${this.cols}`)
        }
      }
      // X-small column span
      if (this.xs) {
        if (Array.isArray(this.xs)) {
          if (this.xs[index]) {
            classNames.push(`xs:col-span-${this.xs[index]}`)
          }
        } else {
          classNames.push(`xs:col-span-${this.xs}`)
        }
      }
      // Small column span
      if (this.sm) {
        if (Array.isArray(this.sm)) {
          if (this.sm[index]) {
            classNames.push(`sm:col-span-${this.sm[index]}`)
          }
        } else {
          classNames.push(`sm:col-span-${this.sm}`)
        }
      }
      // Medium column span
      if (this.md) {
        if (Array.isArray(this.md)) {
          if (this.md[index]) {
            classNames.push(`md:col-span-${this.md[index]}`)
          }
        } else {
          classNames.push(`md:col-span-${this.md}`)
        }
      }
      // Large column span
      if (this.lg) {
        if (Array.isArray(this.lg)) {
          if (this.lg[index]) {
            classNames.push(`lg:col-span-${this.lg[index]}`)
          }
        } else {
          classNames.push(`lg:col-span-${this.lg}`)
        }
      }
      // X-large column span
      if (this.xl) {
        if (Array.isArray(this.xl)) {
          if (this.xl[index]) {
            classNames.push(`xl:col-span-${this.xl[index]}`)
          }
        } else {
          classNames.push(`xl:col-span-${this.xl}`)
        }
      }
      // Other styling classes
      if (this.innerDivClass) {
        if (Array.isArray(this.innerDivClass)) {
          if (this.innerDivClass[index]) {
            classNames.push(this.innerDivClass[index])
          }
        } else {
          classNames.push(this.innerDivClass)
        }
      }

      return classNames.join(' ')
    }
  }
}

</script>
