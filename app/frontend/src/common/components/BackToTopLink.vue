<template>
  <a href="#top" class="back-to-top-link" @click.prevent="handleBackToTop">back top top</a>
</template>

<script>
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
      this.$SmoothScroll(this.targetEl)
    }
  }
}
</script>

<style>
.back-to-top-link {
  margin-left: 10px;
}
</style>
