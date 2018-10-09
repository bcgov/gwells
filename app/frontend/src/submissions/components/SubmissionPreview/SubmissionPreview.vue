<template>
  <div>
    <h2>Well Submission Preview</h2>
    <div class="mt-3">
      <h3>Well Summary</h3>
      <b-row>
        <b-col cols="12" lg="4">Well Tag Number: {{form.well_tag_number}}</b-col>
        <b-col cols="12" lg="4">Well Status:</b-col>
        <b-col cols="12" lg="4">Observation Well Number:</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4">Well Tag Number:</b-col>
        <b-col cols="12" lg="4">Well Status:</b-col>
        <b-col cols="12" lg="4">Observation Well Number:</b-col>
      </b-row>
    </div>

  </div>
</template>

<script>
export default {
  name: 'SubmissionPreview',
  props: [
    'form'
  ]
}
</script>

<style>

</style>
