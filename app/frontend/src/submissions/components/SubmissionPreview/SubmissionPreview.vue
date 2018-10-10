<template>
  <div>
    <h2>Well Submission Preview</h2>
    <div class="my-3">
      <h3>Well Summary</h3>
      <b-row>
        <b-col cols="12" lg="4">Well Tag Number:</b-col>
        <b-col cols="12" lg="4">Well Status:</b-col>
        <b-col cols="12" lg="4">Observation Well Number:</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4">Well Identification Plate Number:</b-col>
        <b-col cols="12" lg="4">Well Class:</b-col>
        <b-col cols="12" lg="4">Observation Well Status:</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4">Owner Name:</b-col>
        <b-col cols="12" lg="4">Well Subclass:</b-col>
        <b-col cols="12" lg="4">Environmental Monitoring System (EMS) ID:</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4">Licensed Status:</b-col>
        <b-col cols="12" lg="4">Intended Water Use:</b-col>
        <b-col cols="12" lg="4">Aquifer Number:</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="6">Alternative specs submitted (if required):</b-col>
      </b-row>
    </div>
    <div class="my-3">
      <h3>Location Information</h3>
      <b-row>
        <b-col cols="12" lg="6" xl="4">
          <b-row>
            <b-col>Street Address: 123 LING COD WAY</b-col>
          </b-row>
          <b-row>
            <b-col>Town/City: MUDGE ISLAND</b-col>
          </b-row>
          <b-row>
            <b-col>
              <div>Legal Description:</div>
              <table class="table table-sm table-striped">
                <tbody>
                  <tr>
                    <th>Lot</th>
                    <td>12</td>
                  </tr>
                  <tr>
                    <th>Plan</th>
                    <td>122</td>
                  </tr>
                  <tr>
                    <th>District Lot</th>
                    <td>122</td>
                  </tr>
                  <tr>
                    <th>Block</th>
                    <td>122</td>
                  </tr>
                  <tr>
                    <th>Section</th>
                    <td>122</td>
                  </tr>
                  <tr>
                    <th>Township</th>
                    <td>122</td>
                  </tr>
                  <tr>
                    <th>Range</th>
                    <td>122</td>
                  </tr>
                  <tr>
                    <th>Land District</th>
                    <td>122</td>
                  </tr>
                  <tr>
                    <th>Property Identification Description (PID)</th>
                    <td>122</td>
                  </tr>
                </tbody>
              </table>

            </b-col>
          </b-row>
        </b-col>
        <b-col cols="12" lg="6" xl="6" offset-xl="2">
          <div class="mb-5">This is a map.</div>
          <div class="my-5">&nbsp;</div>
          <div>Geographic Coordinates - North American Datum of 1983 (NAD 83)</div>
          <b-row>
            <b-col cols="12" lg="4">Latitude: 11222</b-col>
            <b-col cols="12" lg="6">Longitude: 11222</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="4">UTM Easting: 11222</b-col>
            <b-col cols="12" lg="6">UTM Northing: 11222</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="4">Zone: 7</b-col>
            <b-col cols="12" lg="6">Location Accuracy Code: J</b-col>
          </b-row>
        </b-col>
      </b-row>
    </div>
    <div class="my-3">
      <h3>Well Activity</h3>
    </div>
    <div class="my-3">
      <h3>Well Completion Data</h3>
    </div>
    <div class="my-3">
      <h3>Lithology</h3>
    </div>
    <div class="my-3">
      <h3>Casing Details</h3>
    </div>
    <div class="my-3">
      <h3>Surface Seal and Backfill Details</h3>
    </div>
    <div class="my-3">
      <h3>Liner Details</h3>
    </div>
    <div class="my-3">
      <h3>Screen Details</h3>
    </div>
    <div class="my-3">
      <h3>Well Development</h3>
    </div>
    <div class="my-3">
      <h3>Well Yield</h3>
    </div>
    <div class="my-3">
      <h3>Well Decommissioning</h3>
    </div>
    <div class="my-3">
      <h3>Comments</h3>
    </div>
    <div class="my-3">
      <h3>Documentation</h3>
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
