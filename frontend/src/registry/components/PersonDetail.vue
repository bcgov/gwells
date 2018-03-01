<template>
  <div class="container-fluid">
    <div class="row" v-if="currentDriller != {}">
      <div class="col-xs-12 col-sm-8">
        <h2>{{ currentDriller.first_name }} {{ currentDriller.surname }} - {{ person.certNumber }}</h2>
      </div>
      <div class="col-xs-12" v-if="error">
        <api-error :error="error" resetter="setError"></api-error>
      </div>
      <div class="col-xs-12">
        <h2>Certification - {{ person.activityDescription }}</h2>
      </div>
    </div>
    <fieldset>
      <legend>Certification</legend>
      <div class="row">
        <div class="col-xs-12 col-sm-4">
          Certificate number: {{ person.certNumber }}
        </div>
        <div class="col-xs-12 col-sm-4">
          Issued by: {{ person.certAuthority }}
        </div>
      </div>
    </fieldset>
    <fieldset>
      <legend>Classification and Qualifications</legend>
      <div class="row">
        <h4>Qualification</h4>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4">
          Issued by: {{ person.certAuthority }}
        </div>
        <div class="col-xs-12 col-sm-4">
          Certificate number: {{ person.certNumber }}
        </div>
      </div>
    </fieldset>
    <fieldset>
      <legend>Adjudication</legend>
      <div class="row">
        <div class="col-xs-12">
          Date application received:
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4">
          Approval outcome date:
        </div>
        <div class="col-xs-12 col-sm-4">
          Approval outcome:
        </div>
        <div class="col-xs-12 col-sm-4">
          Reason denied:
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-3">
          Register removal date:
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12">
          As Deputy Comptroller, I confirm I have reviewed the application or action and approved this registry update.
        </div>
      </div>
    </fieldset>
  </div>
</template>

<script>
import APIErrorMessage from '@/common/components/APIErrorMessage'
import { mapGetters } from 'vuex'
import { SET_DRILLER } from '@/registry/store/mutations.types'
import { FETCH_DRILLER } from '@/registry/store/actions.types'

export default {
  name: 'person-detail',
  components: {
    'api-error': APIErrorMessage
  },
  data () {
    return {
      person: {
        name: 'John Bobert',
        certNumber: 'CGWA930209',
        certAuthority: 'Canadian Groundwater Association',
        qualificationCode: 'DRILL',
        activityDescription: 'Well Driller'
      }
    }
  },
  computed: {
    ...mapGetters([
      'loading',
      'error',
      'currentDriller'
    ])
  },
  created () {
    this.$store.commit(SET_DRILLER, {})
    this.$store.dispatch(FETCH_DRILLER, this.$route.params.person_guid)
  }
}
</script>

<style>
.panel-heading {
  padding-bottom: 0px!important;
  margin-bottom: 0px!important;
}
</style>
