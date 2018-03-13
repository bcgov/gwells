<template>
  <div class="container-fluid no-pad">
    <div class="row no-pad">
      <div class="col-xs-12">
        <form class="form-horizontal">
          <h3 id="classificationAddHeading">Classification and Qualifications</h3>
          <div class="form-group">
            <div class="col-xs-12">
              <label>Select qualification: &nbsp;</label>
            </div>
            <div class="col-xs-12">
              <div class="radio form-group">
                <label class="col-xs-12">
                  <input type="radio" name="activitySelector" id="activityDriller" v-model="qualType" value="DRILL" style="margin-top: 0px"> Water Well Driller
                </label>
                <label class="col-xs-12">
                  <input type="radio" name="activitySelector" id="activityInstaller" v-model="qualType" value="PUMP" style="margin-top: 0px"> Pump Installer
                </label>
                <label class="col-xs-12">
                  <input type="radio" name="activitySelector" id="activityDriller" v-model="qualType" value="GEOTHERM" style="margin-top: 0px"> Geoexchange Driller
                </label>
                <label class="col-xs-12">
                  <input type="radio" name="activitySelector" id="activityInstaller" v-model="qualType" value="GEOTECH" style="margin-top: 0px"> Geotechnical/Environmental Driller
                </label>
              </div>
            </div>
          </div>
          <div class="form-group">
            <label class="col-xs-12 col-md-1 registry-form-label" for="issuedByOrg">Issued by: </label>
            <div class="col-xs-12 col-md-3 form-spacing">
              <select class="form-control" v-model="editClassification.issuedBy" id="issuedByOrg">
                <option value="">Select issuing authority</option>
                <option v-for="(item, index) in issuerOrgs" :key="`ident ${index}`" :value="item">{{ item }}</option>
              </select>
            </div>
            <label class="col-xs-12 col-md-2 col-md-offset-1" for="certNumber">Certificate number:</label>
            <div class="col-xs-12 col-md-3 form-spacing">
              <input type="text" id="certNumber" placeholder="Enter certificate number" v-model="editClassification.certNo">
            </div>
          </div>
          <div class="form-group">
            <h4>Qualified to drill under this classification</h4>
          </div>
          <div class="form-group">
            <div class="col-xs-12 col-sm-4 col-md-3">
              <div class="checkbox">
                <label>
                  <input type="checkbox" v-model="editClassification.qualCodes.wat"> Water supply wells
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" v-model="editClassification.qualCodes.mon"> Monitoring wells
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" v-model="editClassification.qualCodes.rech"> Recharge wells
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" v-model="editClassification.qualCodes.inj"> Injection wells
                </label>
              </div>
            </div>
            <div class="col-xs-12 col-sm-4 col-md-3 registry-item">
              <div class="checkbox">
                <label>
                  <input type="checkbox" v-model="editClassification.qualCodes.dewat"> Dewatering wells
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" v-model="editClassification.qualCodes.rem"> Remediation wells
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" v-model="editClassification.qualCodes.geo"> Geotechnical wells
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" v-model="editClassification.qualCodes.clos"> Closed-loop geoexchange wells
                </label>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
    <fieldset class="registry-section">
      <legend>Adjudication</legend>
      <form class="form-horizontal">
        <div class="form-group">
          <label class="col-xs-12 col-md-1" for="dateAppReceived">Date application received:</label>
          <div class="col-xs-12 col-md-3 form-spacing">
            <input type="text" id="dateAppReceived" placeholder="Select date" v-model="editClassification.application.receivedDate">
          </div>
        </div>
        <div class="form-group">
          <label class="col-xs-12 col-md-1" for="approvalOutcomeDate">Approval outcome date:</label>
          <div class="col-xs-12 col-md-3 form-spacing">
            <input type="text" id="approvalOutcomeDate" placeholder="Select date" v-model="editClassification.application.approvalOutcomeDate">
          </div>
          <label class="col-xs-12 col-md-1" for="approvalOutcome">Approval outcome:</label>
          <div class="col-xs-12 col-md-3 form-spacing">
            <input type="text" id="approvalOutcome" placeholder="Enter approval outcome" v-model="editClassification.application.approvalOutcome">
          </div>
            <label class="col-xs-12 col-md-1" for="reasonDenied">Reason not approved:</label>
            <div class="col-xs-12 col-md-3 form-spacing">
              <input type="text" id="reasonDenied" placeholder="Enter reason not approved" v-model="editClassification.application.reasonDenied">
            </div>
        </div>
        <div class="form-group">
          <label class="col-xs-12 col-md-1" for="removalDate">Register removal date:</label>
          <div class="col-xs-12 col-md-3 form-spacing">
            <input type="text" id="removalDate" placeholder="Select removal date" v-model="editClassification.application.removalDate">
          </div>
        </div>
      </form>
    </fieldset>
  </div>
</template>

<script>
export default {
  data () {
    return {
      editClassification: {
        issuedBy: '',
        qualCodes: {
          wat: false,
          mon: false,
          rech: false,
          inj: false,
          dewat: false,
          rem: false,
          geo: false,
          clos: false
        },
        application: {
          receivedDate: '',
          approvalOutcomeDate: '',
          approvalOutcome: '',
          reasonDenied: '',
          removalDate: ''
        }
      },
      issuerOrgs: [
        'Canadian Groundwater Association',
        'Province of BC',
        'N/A'
      ],
      qualCodes: [
        {
          activity: 'DRILL',
          quals: ['WAT', 'MON', 'RECH', 'DEWAT', 'REM', 'GEO']
        },
        {
          activity: 'GEOTECH',
          quals: ['MON', 'REM', 'GEO']
        },
        {
          activity: 'GEOTHERM',
          quals: ['CLOS']
        },
        {
          activity: 'PUMP',
          quals: []
        }
      ],
      qualType: 'DRILL'
    }
  },
  computed: {
    quals () {
      const quals = []
      const activity = this.qualCodes.find(item => item.activity === this.qualType)
      return activity ? activity.quals : quals
    }
  },
  watch: {
    qualType: function () {
      const qualList = this.quals.map(item => item.toLowerCase())
      for (let key in this.editClassification.qualCodes) {
        this.editClassification.qualCodes[key] = false
      }
      for (let i = 0; i < qualList.length; i++) {
        if (qualList[i] in this.editClassification.qualCodes) {
          this.editClassification.qualCodes[qualList[i]] = true
        }
      }
    }
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
