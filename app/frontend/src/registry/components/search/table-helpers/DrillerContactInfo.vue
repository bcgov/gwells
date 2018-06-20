<template>
  <div>
    <div v-if="driller.contact_tel">{{driller.contact_tel}}</div>
    <div v-if="driller.contact_cell">{{driller.contact_cell}}</div>

    <!-- for backwards compatibility - new applicants use driller.contact_tel  -->
    <div v-for="(contact, contactIndex) in contactSort(driller)" :key="`contact ${driller.person_guid} ${contactIndex}`">
      <span v-if="contact.type === 'tel'">{{ contact.value }}</span>
      <span v-if="contact.type === 'email'"><a :href="`mailto:${contact.value}`">{{contact.value}}</a></span>
    </div>

    <div v-if="driller.contact_email"><a :href="`mailto:${driller.contact_email}`">{{driller.contact_email}}</a></div>
  </div>
</template>

<script>
export default {
  props: ['driller'],
  methods: {
    contactSort (driller) {
      // sort a person's contact info into groups (tel numbers followed by emails)
      // for old contact info only (will be removed at a later date)
      const tel = []
      const email = []
      if (driller.contact_info) {
        driller.contact_info.forEach((item) => {
          if (item.contact_tel) {
            tel.push({
              type: 'tel',
              value: item.contact_tel
            })
          }
          if (item.contact_email) {
            email.push({
              type: 'email',
              value: item.contact_email
            })
          }
        })
      }
      return tel.concat(email)
    }
  }
}
</script>

<style>

</style>
