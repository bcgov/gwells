import { shallowMount, createLocalVue } from '@vue/test-utils'
import FormInput from '@/common/components/FormInput'

const localVue = createLocalVue()

describe('FormInput.vue', () => {
  const id = 'myFormField'

  it('renders an input field', () => {
    const wrapper = shallowMount(FormInput, {
      propsData: { id },
      localVue
    })
    const input = wrapper.find('#myFormFieldInput')

    expect(input.exists()).toBe(true)
  })
  it('renders a hint if passed a hint string', () => {
    const hint = 'This is a hint!'
    const wrapper = shallowMount(FormInput, {
      propsData: { id, hint },
      localVue
    })
    const text = wrapper.find('#myFormFieldHint').text()

    expect(text).toEqual(hint)
  })
})
