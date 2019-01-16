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

import ApiService from '@/common/services/ApiService.js'
import axios from 'axios'

export default {
  namespaced: true,
  state: {
    aquifer_files: [],
    files_uploading: false,
    file_upload_errors: [],
    file_upload_success: false
  },
  actions: {
    uploadFiles (context, aquiferId) {
      context.commit('setFilesUploading', true)

      let uploadPromises = []

      context.state.aquifer_files.forEach((file) => {
        uploadPromises.push(
          ApiService.presigned_put_url('aquifers', aquiferId, file.name)
            .then((response) => {
              let url = response.data.url
              let objectName = response.data.object_name
              let filename = response.data.filename
              let file = context.state.aquifer_files.filter(file => file.name === objectName)

              if (file.length !== 1) {
                context.commit('addError', 'Error uploading file: ' + filename)
                return
              }

              file = file[0]

              let options = {
                headers: {
                  'Content-Type': file.type
                }
              }

              axios.put(url, file, options)
                .then((response) => {
                  console.log('successfully added file: ' + objectName)
                })
                .catch((error) => {
                  console.log(error)
                  context.commit('addError', error)
                })
            })
            .catch((error) => {
              console.log(error)
              context.commit('addError', error)
            })
        )
      })

      Promise.all(uploadPromises)
        .then(function (values) {
          context.commit('setFilesUploading', false)
          context.commit('setFileUploadSuccess', true)
          context.commit('setFiles', [])
          setTimeout(() => {
            context.commit('setFileUploadSuccess', false)
          }, 5000)
        })
    }
  },
  mutations: {
    addError (state, payload) {
      state.file_upload_errors.push(payload)
    },
    setFilesUploading (state, payload) {
      state.files_uploading = payload
    },
    setFileUploadSuccess (state, payload) {
      state.file_upload_success = payload
    },
    setFiles (state, payload) {
      state.aquifer_files = payload
    }
  }
}
