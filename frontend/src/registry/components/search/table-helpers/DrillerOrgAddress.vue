<template>
  <div>
    {{ company.address }}
    <div><span v-if="company.city">{{ company.city }}, </span>{{ company.prov }}</div>
    <div v-if="company.postalCode">{{ company.postalCode }}</div>
  </div>
</template>

<script>
export default {
  props: ['driller', 'activity'],
  data () {
    return {
    }
  },
  computed: {
    company () {
      const company = {}
      if (this.driller && this.driller.registrations && this.driller.registrations.length && this.activity) {
        const registration = this.driller.registrations.find((reg) => {
          return reg.activity === this.activity
        })
        if (registration && registration.organization) {
          company['city'] = registration.organization.city || null // default to null if not supplied (avoid undefined)
          company['address'] = registration.organization.street_address || null
          company['prov'] = registration.organization.province_state || null
          company['postalCode'] = registration.organization.postal_code || null
        }
      }
      return company
    }
  }
}
</script>

<style>

</style>
