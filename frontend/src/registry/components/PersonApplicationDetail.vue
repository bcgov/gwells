<template>
  <div class="container-fluid">
    <div class="row" v-if="currentDriller != {}">
      <div class="col-xs-12 col-sm-8">
        <h2>{{ currentDriller.first_name }} {{ currentDriller.surname }}</h2>
      </div>
      <div class="col-xs-12" v-if="error">
        <api-error :error="error" resetter="setError"></api-error>
      </div>
      <div class="col-xs-12" v-if="classification.registries_subactivity">
        <h2>Certification - {{ classification.registries_subactivity.description }}</h2>
      </div>
    </div>
    <fieldset class="registry-section">
      <legend>Classification and Qualifications</legend>
      <div class="row" v-if="classification.registries_subactivity">
        <h4>Qualification: {{ classification.registries_subactivity.description }}&nbsp;
        <span class="registry-subtle">
          (<router-link :to="{ name: 'PersonDetail', params: { person_guid: currentDriller.person_guid }}">change</router-link>)
        </span></h4>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          <span class="registry-label">Issued by:</span>
        </div>
        <div class="col-xs-12 col-sm-4 registry-item">
          <span class="registry-label">Certificate number:</span>
        </div>
      </div>
      <div class="row">
        <h4>Qualified to drill under this license</h4>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4 col-md-3">
          <div class="qualification-item">
            <r-checkbox :checked="~qualCodeList.findIndex(q => q === 'WAT')"></r-checkbox> Water supply wells
          </div>
          <div class="qualification-item">
            <r-checkbox :checked="~qualCodeList.findIndex(q => q === 'MON')"></r-checkbox> Monitoring wells
          </div>
          <div class="qualification-item">
            <r-checkbox :checked="~qualCodeList.findIndex(q => q === 'RECH')"></r-checkbox> Recharge wells
          </div>
          <div class="qualification-item">
            <r-checkbox :checked="~qualCodeList.findIndex(q => q === 'RECH')"></r-checkbox> Injection wells
          </div>
        </div>
        <div class="col-xs-12 col-sm-4 col-md-3 registry-item">
          <div class="qualification-item">
            <r-checkbox :checked="~qualCodeList.findIndex(q => q === 'WAT')"></r-checkbox> Dewatering wells
          </div>
          <div class="qualification-item">
            <r-checkbox :checked="~qualCodeList.findIndex(q => q === 'REM')"></r-checkbox> Remediation wells
          </div>
          <div class="qualification-item">
            <r-checkbox :checked="~qualCodeList.findIndex(q => q === 'GEO')"></r-checkbox> Geotechnical wells
          </div>
          <div class="qualification-item">
            <r-checkbox :checked="~qualCodeList.findIndex(q => q === 'CLOS')"></r-checkbox> Closed-loop geoexchange wells
          </div>
        </div>
      </div>
    </fieldset>
    <fieldset class="registry-section">
      <legend>Adjudication</legend>
      <div class="row">
        <div class="col-xs-12 registry-item">
          <span class="registry-label">Date application received:</span>
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          <span class="registry-label">Approval outcome date:</span>
        </div>
        <div class="col-xs-12 col-sm-4 registry-item">
          <span class="registry-label">Approval outcome:</span>
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          <span class="registry-label">Register removal date:</span>
        </div>
        <div class="col-xs-12 col-sm-4 registry-item">
          <span class="registry-label">Reason denied:</span>
        </div>
      </div>
      <!-- <div class="row">
        <div class="col-xs-12 registry-item">
          <div class="checkbox form-inline">
            <label>
              <input type="checkbox" style="margin-top:-4px;" class="registry-disabled-item" disabled><span style="color: #808080">As Deputy Comptroller, I confirm I have reviewed the application or action and approved this registry update.</span>
            </label>
          </div>
        </div>
      </div> -->
    </fieldset>
  </div>
</template>

<script>
import APIErrorMessage from '@/common/components/APIErrorMessage'
import QualCheckbox from '@/common/components/QualCheckbox'
import { mapGetters } from 'vuex'
import { SET_DRILLER } from '@/registry/store/mutations.types'
import { FETCH_DRILLER } from '@/registry/store/actions.types'

export default {
  name: 'PersonApplicationDetail',
  components: {
    'api-error': APIErrorMessage,
    'r-checkbox': QualCheckbox
  },
  data () {
    return {}
  },
  computed: {
    classification () {
      let classification = {}
      if (this.currentDriller.applications && this.currentDriller.applications.length) {
        this.currentDriller.applications.forEach((app) => {
          if (app.classificationappliedfor_set && app.classificationappliedfor_set.length) {
            classification = app.classificationappliedfor_set.find((item) => {
              console.log(item.registries_subactivity.code.toLowerCase())
              console.log(this.$route.params.classCode)
              return item.registries_subactivity.code.toLowerCase() === this.$route.params.classCode
            })
            console.log(classification)
          }
        })
      }
      return classification
    },
    qualCodeList () {
      const qualList = []
      if (
        this.classification.registries_subactivity &&
        this.classification.registries_subactivity.qualificationcode_set
      ) {
        this.classification.registries_subactivity.qualificationcode_set.forEach((item) => {
          qualList.push(item.code)
        })
      }
      return qualList
    },
    ...mapGetters([
      'loading',
      'error',
      'currentDriller'
    ])
  },
  created () {
    if (this.currentDriller.person_guid !== this.$route.params.person_guid) {
      this.$store.commit(SET_DRILLER, {})
    }
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
.qualification-item {
  margin-bottom: 5px;
}
.registry-subtle {
  font-size: 0.9rem;
}
</style>
