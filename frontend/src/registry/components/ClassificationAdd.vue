<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-xs-12">
      <h3>Classification and Qualifications</h3>
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
                <label>
                  <input type="radio" name="activitySelector" id="activityDriller" v-model="qualType" value="GEOTHERM" style="margin-top: 0px" disabled> Geoexchange Driller
                </label>
              <div>
              </div>
                <label>
                  <input type="radio" name="activitySelector" id="activityInstaller" v-model="qualType" value="GEOTECH" style="margin-top: 0px" disabled> Geotechnical/Environmental Driller
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="form-group">
        <label class="col-xs-12 col-md-2 registry-form-label" for="issuedByOrg">Issued by: </label>
        <div class="col-xs-12 col-md-3 form-spacing">
          <select class="form-control" v-model="editClassification.issuedBy" id="issuedByOrg">
            <option value="">Select identification type</option>
            <option v-for="(item, index) in issuerOrgs" :key="`ident ${index}`" :value="item">{{ item }}</option>
          </select>
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
            <r-checkbox></r-checkbox> Water supply wells
          </div>
          <div class="qualification-item">
            <r-checkbox></r-checkbox> Monitoring wells
          </div>
          <div class="qualification-item">
            <r-checkbox></r-checkbox> Recharge wells
          </div>
          <div class="qualification-item">
            <r-checkbox></r-checkbox> Injection wells
          </div>
        </div>
        <div class="col-xs-12 col-sm-4 col-md-3 registry-item">
          <div class="qualification-item">
            <r-checkbox></r-checkbox> Dewatering wells
          </div>
          <div class="qualification-item">
            <r-checkbox></r-checkbox> Remediation wells
          </div>
          <div class="qualification-item">
            <r-checkbox></r-checkbox> Geotechnical wells
          </div>
          <div class="qualification-item">
            <r-checkbox></r-checkbox> Closed-loop geoexchange wells
          </div>
        </div>
      </div>
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
        <div class="col-xs-12 col-sm-4 registry-item">
          <span class="registry-label">Reason not approved:</span>
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-4 registry-item">
          <span class="registry-label">Register removal date:</span>
        </div>
      </div>
    </fieldset>
  </div>
</template>

<script>
export default {
  data () {
    return {
      editClassification: {
        issuedBy: '',
        qualCodes: []
      },
      issuerOrgs: [
        'Canadian Groundwater Association',
        'Province of BC',
        'N/A'
      ],
      qualCodes: [
        'WAT',
        'MON',
        'RECH',
        'RECH',
        'WAT',
        'REM',
        'GEO',
        'CLOS'
      ]
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
