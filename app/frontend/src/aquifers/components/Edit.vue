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
        <b-row v-if="!loading" class="border-bottom mb-3 pb-2">
          <b-col><h5>Aquifer {{record.aquifer_id}} Summary - Edit</h5></b-col>
        </b-row>

        <b-row v-if="loading" class="border-bottom mb-3 pb-2">
          <b-col><h5>Loading...</h5></b-col>
        </b-row>

        <aquifer-form :record="record" :fieldErrors="fieldErrors" showId />

        <b-row class="mt-4">
          <b-col cols="auto">
            <b-button
              :disabled="loading"
              variant="secondary"
              v-b-modal.confirmSave>
              Save
            </b-button>

            <b-button
              :disabled="loading"
              variant="secondary"
              v-b-modal.confirmCancel>
              Cancel
            </b-button>
          </b-col>
        </b-row>
      </b-container>
    </b-card>

    <b-modal
      v-on:ok="save()"
      id="confirmSave">
      <p>Are you sure you would like to save this record?</p>
    </b-modal>

    <b-modal
      v-on:ok="view"
      id="confirmCancel">
      <p>Are you sure you want to quit editing this record?</p>
    </b-modal>
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
  created () {
    this.fetch()
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
    handlePatchError (error) {
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
    save (id = this.id) {
      this.showSaveSuccess = false
      this.fieldErrors = {}

      ApiService.patch('aquifers', id, this.record)
        .then(() => { this.showSaveSuccess = true })
        .catch(this.handlePatchError)
    },
    view () {
      this.$router.push({ name: 'view', params: { id: this.id } })
    },
    fetch (id = this.id) {
      this.loading = true
      this.error = undefined

      ApiService.query(`aquifers/${id}`)
        .then((response) => {
          this.record = response.data
        })
        .then(() => { this.loading = false })
        .catch((error) => { this.error = error.response })
    }
  },
  props: ['id']
}
</script>
