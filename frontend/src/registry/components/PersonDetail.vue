<template>
  <div class="container-fluid">
    <div class="row" v-if="currentDriller != {}">
      <div class="col-xs-12 col-sm-8">
        <h2>{{ currentDriller.first_name }} {{ currentDriller.surname }} - {{ person.certNumber }}</h2>
      </div>
      <div class="col-xs-12" v-if="error">
        <api-error :error="error" resetter="setError"></api-error>
      </div>
    </div>
    <fieldset class="registry-section">
      <legend>Classifications</legend>
      <div>
        <div>Geoexchange Driller</div>
        <div>Water Well Driller</div>
      </div>
    </fieldset>
    <fieldset class="registry-section">
      <legend>Personal Information</legend>
      <div class="row">
        <div class="col-xs-12 col-sm-4">
          Last name: {{ currentDriller.surname }}
        </div>
        <div class="col-xs-12 col-sm-8">
          First name: {{ currentDriller.first_name }}
        </div>
      </div>
    </fieldset>
    <fieldset class="registry-section">
      <legend>Current Company Information</legend>
      <div class="row">
        <div class="col-xs-12 registry-item">
          Date application received:
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          Company name: {{ company.organization_name }}
        </div>
        <div class="col-xs-12 col-sm-8 registry-item">
          Street address: {{ company.street_address }}
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          City: {{ company.city }}
        </div>
        <div class="col-xs-12 col-sm-8 registry-item">
          Province: {{ company.province_state }}
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          Postal Code: {{ company.postal_code }}
        </div>
        <div class="col-xs-12 col-sm-8 registry-item">
          Telephone: {{ company.contact_tel }}
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          Email address: {{ company.contact_email }}
        </div>
        <div class="col-xs-12 col-sm-8 registry-item">
          Website: {{ company.contact_email }}
        </div>
      </div>
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
  name: 'person-detail',
  components: {
    'api-error': APIErrorMessage,
    'r-checkbox': QualCheckbox
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
      qualType: 'DRILL',
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
    company () {
      if (this.currentDriller && this.currentDriller.companies && this.currentDriller.companies.length) {
        return this.currentDriller.companies[0]
      }
      return {}
    },
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
.qualification-item {
  margin-bottom: 5px;
}
</style>
