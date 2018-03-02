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
    <fieldset class="registry-section">
      <legend>Certification</legend>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          Certificate number: {{ person.certNumber }}
        </div>
        <div class="col-xs-12 col-sm-4 registry-item">
          Issued by: {{ person.certAuthority }}
        </div>
      </div>
    </fieldset>
    <fieldset class="registry-section">
      <legend>Classification and Qualifications</legend>
      <div class="row">
        <h4>Qualification</h4>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          Issued by: {{ person.certAuthority }}
        </div>
        <div class="col-xs-12 col-sm-4 registry-item">
          Certificate number: {{ person.certNumber }}
        </div>
      </div>
      <div class="row">
        <h4>Classifications</h4>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4 col-md-3 col-lg-2" style="margin-bottom: -15px">
          <div class="checkbox">
            <label>
              <input type="checkbox" style="margin-top:-3px;" v-model="wellQualifications.supply">Water supply wells
            </label>
          </div>
          <div class="checkbox">
            <label>
              <input type="checkbox" style="margin-top:-3px;" v-model="wellQualifications.monitoring">Monitoring wells
            </label>
          </div>
          <div class="checkbox">
            <label>
              <input type="checkbox" style="margin-top:-3px;" v-model="wellQualifications.recharge">Recharge wells
            </label>
          </div>
          <div class="checkbox">
            <label>
              <input type="checkbox" style="margin-top:-3px;" v-model="wellQualifications.injection">Injection wells
            </label>
          </div>
        </div>
        <div class="col-xs-12 col-sm-4 col-md-3 col-lg-2 registry-item">
          <div class="checkbox">
            <label>
              <input type="checkbox" style="margin-top:-3px;" v-model="wellQualifications.dewatering">Dewatering wells
            </label>
          </div>
          <div class="checkbox">
            <label>
              <input type="checkbox" style="margin-top:-3px;" v-model="wellQualifications.remediation">Remediation wells
            </label>
          </div>
          <div class="checkbox">
            <label>
              <input type="checkbox" style="margin-top:-3px;" v-model="wellQualifications.geotechnical">Geotechnical wells
            </label>
          </div>
          <div class="checkbox">
            <label>
              <input type="checkbox" style="margin-top:-3px;" v-model="wellQualifications.geoexchange">Closed-loop geoexchange wells
            </label>
          </div>
        </div>
      </div>
    </fieldset>
    <fieldset class="registry-section">
      <legend>Adjudication</legend>
      <div class="row">
        <div class="col-xs-12 registry-item">
          Date application received:
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          Approval outcome date:
        </div>
        <div class="col-xs-12 col-sm-4 registry-item">
          Approval outcome:
        </div>
        <div class="col-xs-12 col-sm-4 registry-item">
          Reason denied:
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-3 registry-item">
          Register removal date:
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 registry-item">
          <div class="checkbox form-inline">
            <label>
              <input type="checkbox" style="margin-top:-4px;" class="registry-disabled-item" disabled><span style="color: #808080">As Deputy Comptroller, I confirm I have reviewed the application or action and approved this registry update.</span>
            </label>
          </div>
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
      },
      wellQualifications: {
        supply: true,
        monitoring: true,
        recharge: true,
        injection: true,
        dewatering: false,
        remediation: false,
        geotechnical: true,
        geoexchange: false
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
.registry-section {
  margin-top: 25px;
  margin-bottom: 20px;
}
.registry-item {
  margin-bottom: 20px;
}
.registry-disabled-item {
  color: #808080;
  cursor: auto!important;
}
</style>
