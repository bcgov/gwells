<template>
  <div class="card">
    <div class="card-body">
      <h4 class="card-title">Well Activity Submission</h4>
      <p>Submit activity on a well that does not exist in the system. Try a search to see if the well exists in the system before submitting a report.</p>
      <b-form>
        <step01-type></step01-type>
      </b-form>
    </div>
  </div>
</template>

<script>
import Step01Type from '@/submissions/components/SubmissionForm/Step01Type.vue'
export default {
  name: 'SubmissionsHome',
  components: {
    Step01Type
  },
  data () {
    return {

    }
  }
}
</script>

<style>

</style>
