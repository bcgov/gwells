<template>
  <b-container>
    <b-card title="Manage Organizations">

      <!-- Add company button (opens 'add company' modal) and success feedback -->
      <b-row>
        <b-col>
          <b-button
              type="button"
              v-b-modal.orgModal
              variant="light"
              size="sm"
              class="mb-3">
            <i class="fa fa-plus-square-o"></i> Add a company</b-button>
          <organization-add @newOrgAdded="newOrgHandler"></organization-add>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-alert variant="success" :show="companyAddSuccess" dismissible @dismissed="companyAddSuccess=false">Company added.</b-alert>
        </b-col>
      </b-row>

      <!-- Company selector (used to select company to edit) -->
      <b-row>
        <b-col cols="12" md="5">
          <v-select></v-select>
        </b-col>
      </b-row>
    </b-card>
  </b-container>
</template>

<script>
// import ApiService from '@/common/services/ApiService.js'
import OrganizationAdd from '@/registry/components/people/OrganizationAdd.vue'

export default {
  name: 'OrganizationEdit',
  components: {
    OrganizationAdd
  },
  data () {
    return {
      companyAddSuccess: false
    }
  },
  methods: {
    newOrgHandler () {
      this.companyAddSuccess = true
    }
  },
  created () {
    console.log('asdf')
  }
}
</script>

<style>

</style>
