<template>
  <a href="#top" class="back-to-top-link" @click.prevent="handleBackToTop">back to top</a>
</template>

<script>
import smoothScroll from 'smoothscroll'

export default {
  name: 'BackToTopLink',
  props: ['target'],
  data () {
    return { }
  },
  computed: {
    targetEl () {
      return this.target ? this.target.$el : 0
    }
  },
  methods: {
    handleBackToTop () {
      smoothScroll(this.targetEl)
    }
  }
}
</script>

<style>
.back-to-top-link {
  margin-left: 10px;
}
</style>
