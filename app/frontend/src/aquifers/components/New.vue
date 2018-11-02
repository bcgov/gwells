/*
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/

<template>
  <div>
    <b-card no-body class="p-3 mb-4">
      <api-error v-if="error" :error="error"/>
      <b-alert variant="success" :show="showSaveSuccess">Record successfully updated</b-alert>

      <b-container>
        <b-row class="border-bottom mb-3 pb-2">
          <b-col><h5>Add new Aquifer</h5></b-col>
        </b-row>

        <aquifer-form
          v-on:save="save"
          v-on:cancel="navigateToView"
          :record="record"
          :fieldErrors="fieldErrors"
          />

      </b-container>
    </b-card>
  </div>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import APIErrorMessage from '@/common/components/APIErrorMessage'
import AquiferForm from './Form'

export default {
  components: {
    'api-error': APIErrorMessage,
    'aquifer-form': AquiferForm
  },
  data () {
    return {
      error: undefined,
      fieldErrors: {},
      loading: false,
      record: {},
      showSaveSuccess: false
    }
  },
  methods: {
    navigateToView () {
      this.$router.push({ name: 'home' })
    },
    handleSuccess ({data}) {
      this.$router.push({ name: 'view', params: { id: data.aquifer_id } })
    },
    handleError (error) {
      if (error.response) {
        if (error.response.status === 400) {
          this.fieldErrors = error.response.data
        } else {
          this.error = error.response
        }
      } else {
        this.error = error.message
      }
    },
    save () {
      this.showSaveSuccess = false
      this.fieldErrors = {}

      ApiService.post('aquifers', this.record)
        .then(this.handleSuccess)
        .catch(this.handleError)
    }
  }
}
</script>
