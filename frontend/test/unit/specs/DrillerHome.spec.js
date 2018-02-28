import Vue from 'vue'
import RegisterHome from '@/registry/components/RegisterHome'

describe('RegisterHome.vue', () => {
  it('renders the correct title', () => {
    const Constructor = Vue.extend(RegisterHome)
    const vm = new Constructor().$mount()
    expect(vm.$el.querySelector('#registry-title h2').textContent)
      .to.equal('Register of Well Drillers and Well Pump Installers')
  })
})
