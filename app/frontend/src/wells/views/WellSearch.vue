<template>
  <b-card class="container container-wide p-1">
    <h1 class="card-title">Well Search</h1>
    <p>
      Not all groundwater wells are registered with the province, as registration was voluntary until February 29, 2016. Data quality issues may impact search results.
    </p>
    <p>
      Search by one of the fields below, or zoom to a location on the map and select the "Search Wells in this Area" button.
    </p>
    <b-row class="mt-5">
      <b-col cols="12" lg="6">
        <b-row>
          <b-col>
            <form-input
              id="wellTagSearchBox"
              group-class="font-weight-bold"
              label="Well Tag Number or Well Identification Plate Number"
            ></form-input>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <form-input
              id="streetAddressSearchBox"
              group-class="font-weight-bold"
              label="Street Address"
            ></form-input>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <form-input
              id="lotNumberSearchBox"
              group-class="font-weight-bold"
              label="Legal Plan or Lot Number"
            ></form-input>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <form-input
              id="ownerNameSearchBox"
              group-class="font-weight-bold"
              label="Owner Name"
            ></form-input>
          </b-col>
        </b-row>
        <b-row class="my-3">
          <b-col>
            <b-btn variant="primary">Search</b-btn>
            <b-btn variant="dark" class="mx-2">Reset</b-btn>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <p>For additional search options, try:</p>
            <ul>
                <li><a href="http://maps.gov.bc.ca/ess/hm/wrbc/" id="BCWRAtlas">B.C. Water Resource Atlas</a></li>
                <li><a href="http://maps.gov.bc.ca/ess/hm/imap4m/" id="iMapBC">iMapBC</a></li>
            </ul>
          </b-col>
        </b-row>
      </b-col>
      <b-col cols="12" lg="6">
        This is a map.
      </b-col>
    </b-row>
    <b-row class="my-5">
      <b-col>
        <b-table
          :fields="['well_tag_number', 'well_ID_plate_number', 'owner_name', 'street_address', 'lot', 'plan', 'district_lot', 'land_district', 'PID', 'diameter', 'finished_well_depth']"
          show-empty
        ></b-table>
      </b-col>
    </b-row>
  </b-card>
</template>

<script>
export default {
  name: 'WellSearch'
}
</script>

<style>

</style>
