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
      <div class="form-group">
        <div class="row">
          <div class="col-xs-12">
            <label>Select qualification: &nbsp;</label>
          </div>
          <div class="col-xs-12 col-sm-4 col-md-3">
            <div class="radio">
              <div>
                <label>
                  <input type="radio" name="activitySelector" id="activityDriller" v-model="qualType" value="DRILL" style="margin-top: 0px"> Water Well Driller
                </label>
              <div>
              </div>
                <label>
                  <input type="radio" name="activitySelector" id="activityInstaller" v-model="qualType" value="PUMP" style="margin-top: 0px"> Pump Installer
                </label>
              </div>
            </div>
          </div>
          <div class="col-xs-12 col-sm-4 col-md-3 form-spacing">
            <div class="radio">
              <div>
                <label class="registry-disabled-item">
                  <input type="radio" class="registry-disabled-item" name="activitySelector" id="activityDriller" v-model="qualType" value="GEOTHERM" style="margin-top: 0px" disabled> Geoexchange Driller
                </label>
              <div>
              </div>
                <label class="registry-disabled-item">
                  <input type="radio" class="registry-disabled-item" name="activitySelector" id="activityInstaller" v-model="qualType" value="GEOTECH" style="margin-top: 0px" disabled> Geotechnical/Environmental Driller
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
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
        <h4>Qualified to drill</h4>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4 col-md-3">
          <div class="qualification-item">
            <r-checkbox checked="true"></r-checkbox> Water supply wells
          </div>
          <div class="qualification-item">
            <r-checkbox checked="false"></r-checkbox> Monitoring wells
          </div>
          <div class="qualification-item">
            <r-checkbox checked="false"></r-checkbox> Recharge wells
          </div>
          <div class="qualification-item">
            <r-checkbox checked="true"></r-checkbox> Injection wells
          </div>
        </div>
        <div class="col-xs-12 col-sm-4 col-md-3 registry-item">
          <div class="qualification-item">
            <r-checkbox checked="false"></r-checkbox> Dewatering wells
          </div>
          <div class="qualification-item">
            <r-checkbox checked="true"></r-checkbox> Remediation wells
          </div>
          <div class="qualification-item">
            <r-checkbox checked="false"></r-checkbox> Geotechnical wells
          </div>
          <div class="qualification-item">
            <r-checkbox checked="false"></r-checkbox> Closed-loop geoexchange wells
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
