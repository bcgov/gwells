const inputFormatMixin = {
  methods: {
    formatTel (value) {
      return value.replace(/[^0-9]/g, '').replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3')
    }
  }
}

export default inputFormatMixin
