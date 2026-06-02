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
    <b-card class="container p-1">
      <api-error v-if="error" :error="error"/>

      <b-container>
        <b-row class="border-bottom mb-4 pb-2 pt-2">
          <b-col><h4>Add new Aquifer</h4></b-col>
        </b-row>

        <aquifer-form
          :isNew="true"
          :record="record"
          :fieldErrors="fieldErrors"
          @save="save"
          @cancel="navigateToView"
          />
      </b-container>
    </b-card>
  </div>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import APIErrorMessage from '@/common/components/APIErrorMessage.vue'
import AquiferForm from './Form.vue'
import { useCommonStore } from '@/stores/common.js'

export default {
  components: {
    'api-error': APIErrorMessage,
    'aquifer-form': AquiferForm
  },
  computed: {
    commonStore () { return useCommonStore() },
  },
  data () {
    return {
      error: undefined,
      fieldErrors: {},
      record: {
        resources: [],
        effective_date: '9999-12-31T23:59:59.999Z'
      }
    }
  },
  methods: {
    navigateToView () {
      this.$router.push({ name: 'home' })
    },
    handleSuccess ({ data }) {
      if (this.commonStore.uploadFiles.length > 0) {
        this.commonStore.uploadTheFiles({
          documentType: 'aquifers',
          recordId: data.aquifer_id
        }).then((values) => {
          this.commonStore.fileUploadSucceeded()
          this.$router.push({ name: 'aquifers-view', params: { id: data.aquifer_id } })
        }).catch((error) => {
          this.commonStore.fileUploadFail()
          console.error(error)
        })
      } else {
        this.$router.push({ name: 'aquifers-view', params: { id: data.aquifer_id } })
      }
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
