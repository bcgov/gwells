<template>
  <div class="container">
    <b-card no-body class="mb-3">
        <b-breadcrumb :items="breadcrumbs" class="py-0 my-2"></b-breadcrumb>
    </b-card>
    <div class="card">
      <div class="card-body">
        <div v-if="currentDriller != {}">

            <h5 class="card-title" id="titlePersonName">{{ currentDriller.first_name }} {{ currentDriller.surname }}</h5>

          <div class="col-12" v-if="error">
            <api-error :error="error" resetter="SET_ERROR"></api-error>
          </div>
          <div class="col-12" v-if="classification && classification.registries_subactivity">
            <h2>Certification - {{ classification.registries_subactivity.description }}</h2>
          </div>
        </div>
          <h5>Classification and Qualifications</h5>
          <div class="row" v-if="classification && classification.registries_subactivity">
            <div class="col-12 registry-item">
              <h4>Qualification: {{ classification.registries_subactivity.description }}&nbsp;
              <span class="registry-subtle">
                (<router-link :to="{ name: 'PersonDetail', params: { person_guid: currentDriller.person_guid }}">change</router-link>)
              </span></h4>
            </div>
          </div>
          <div class="row">
            <div class="col-12 col-sm-4 registry-item">
              <span class="registry-label">Issued by:</span>
            </div>
            <div class="col-12 col-sm-4 registry-item">
              <span class="registry-label">Certificate number:</span>
            </div>
          </div>
          <div class="row">
            <div class="col-12 registry-item">
              <h6>Qualified to drill under this classification</h6>
            </div>
          </div>
          <div class="row">
            <div class="col-12 col-sm-4 col-md-3">
              <div class="qualification-item">
                <r-checkbox :checked="qualCodeList.some(q => q === 'WAT')"></r-checkbox> Water supply wells
              </div>
              <div class="qualification-item">
                <r-checkbox :checked="qualCodeList.some(q => q === 'MON')"></r-checkbox> Monitoring wells
              </div>
              <div class="qualification-item">
                <r-checkbox :checked="qualCodeList.some(q => q === 'RECH')"></r-checkbox> Recharge wells
              </div>
              <div class="qualification-item">
                <r-checkbox :checked="qualCodeList.some(q => q === 'RECH')"></r-checkbox> Injection wells
              </div>
            </div>
            <div class="col-12 col-sm-4 col-md-3 registry-item">
              <div class="qualification-item">
                <r-checkbox :checked="qualCodeList.some(q => q === 'WAT')"></r-checkbox> Dewatering wells
              </div>
              <div class="qualification-item">
                <r-checkbox :checked="qualCodeList.some(q => q === 'REM')"></r-checkbox> Remediation wells
              </div>
              <div class="qualification-item">
                <r-checkbox :checked="qualCodeList.some(q => q === 'GEO')"></r-checkbox> Geotechnical wells
              </div>
              <div class="qualification-item">
                <r-checkbox :checked="qualCodeList.some(q => q === 'CLOS')"></r-checkbox> Closed-loop geoexchange wells
              </div>
            </div>
          </div>
          <h5>Adjudication</h5>
          <div class="row">
            <div class="col-12 registry-item">
              <span class="registry-label">Date application received:</span>
            </div>
          </div>
          <div class="row">
            <div class="col-12 col-sm-4 registry-item">
              <span class="registry-label">Approval outcome date:</span>
            </div>
            <div class="col-12 col-sm-4 registry-item">
              <span class="registry-label">Approval outcome:</span>
            </div>
            <div class="col-12 col-sm-4 registry-item">
              <span class="registry-label">Reason not approved:</span>
            </div>
          </div>
          <div class="row">
            <div class="col-12 col-sm-4 registry-item">
              <span class="registry-label">Register removal date:</span>
            </div>
          </div>
          <!-- <div class="row">
            <div class="col-12 registry-item">
              <div class="checkbox form-inline">
                <label>
                  <input type="checkbox" style="margin-top:-4px;" class="registry-disabled-item" disabled><span style="color: #808080">As Deputy Comptroller, I confirm I have reviewed the application or action and approved this registry update.</span>
                </label>
              </div>
            </div>
          </div> -->
      </div>
    </div>
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
    return {
      breadcrumbs: [
        {
          text: 'Registry',
          to: { name: 'SearchHome' }
        },
        {
          text: 'Profile',
          to: { name: 'PersonDetail', params: { person_guid: this.$route.params.person_guid } }
        },
        {
          text: `Classification (${this.$route.params.classCode})`,
          active: true
        }
      ]
    }
  },
  computed: {
    classification () {
      let classification = {}
      if (this.currentDriller.applications && this.currentDriller.applications.length) {
        this.currentDriller.applications.forEach((app) => {
          if (app.classificationappliedfor_set && app.classificationappliedfor_set.length) {
            classification = app.classificationappliedfor_set.find((item) => {
              if (item.registries_subactivity && item.registries_subactivity.code) {
                return item.registries_subactivity.code.toLowerCase() === this.$route.params.classCode
              }
            })
          }
        })
      }
      return classification
    },
    qualCodeList () {
      const qualList = []
      if (
        this.classification &&
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
