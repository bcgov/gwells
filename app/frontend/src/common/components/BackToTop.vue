<template>
  <div id="backToTop">
    <transition name="fade">
      <img class="back-to-top" v-if="scrolled" src="../assets/images/back-to-top.png" @click="handleBackToTop">
    </transition>
  </div>
</template>

<script>
import smoothScroll from 'smoothscroll'

export default {
  name: 'BackToTop',
  props: ['target'],
  data () {
    return {
      scrolled: false
    }
  },
  methods: {
    handleScroll () {
      this.scrolled = window.scrollY > 10
    },
    handleBackToTop () {
      smoothScroll(this.target.$el)
    }
  },
  beforeMount () {
    this.scrolled = window.scrollY > 10
    window.addEventListener('scroll', this.handleScroll)
  },
  beforeDestroy () {
    window.removeEventListener('scroll', this.handleScroll)
  }
}
</script>

<style>
  .back-to-top {
    position: fixed;
    bottom: 20px;
    right: 20px;
    cursor: pointer;
  }
  .fade-enter-active, .fade-leave-active {
    transition: opacity .5s;
  }
  .fade-enter, .fade-leave-to {
    opacity: 0;
  }
</style>
