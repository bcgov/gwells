<template>
  <div>
    <div v-for="(contact, contactIndex) in contactSort(driller)" :key="`contact ${driller.person_guid} ${contactIndex}`">
      {{ contact }}
    </div>
  </div>
</template>

<script>
export default {
  props: ['driller'],
  methods: {
    contactSort (driller) {
      // sort a person's contact info into groups (tel numbers followed by emails)
      const tel = []
      const email = []
      driller.contact_info.forEach((item) => {
        if (item.contact_tel) {
          tel.push(item.contact_tel)
        }
        if (item.contact_email) {
          tel.push(item.contact_email)
        }
      })
      return tel.concat(email)
    }
  }
}
</script>

<style>

</style>
