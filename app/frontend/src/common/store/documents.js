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

export default {
  namespaced: true,
  state: {
    isPrivate: false,
    upload_files: [],
    files_uploading: false,
    file_upload_errors: [],
    file_upload_error: false,
    file_upload_success: false,
    shapefile_uploading: false,
    shapefile_upload_message: '',
    shapefile_upload_success: false,
    shapefile: null
  },
  actions: {
    uploadShapefile (context, payload) {
      const file = context.state.shapefile
      let formData = new FormData()
      formData.append('geometry', file)
      const url = `${payload.documentType}/${payload.recordId}/geometry`
      context.commit('setShapefileUploading', true)
      ApiService.post(url, formData)
        .then(response => {
          context.commit('setShapefileUploadSuccess', true)
          context.commit('setShapefileUploadMessage', '')
          setTimeout(() => {
            context.commit('setShapefileUploadSuccess', false)
          }, 5000)
        })
        .catch(e => {
          context.commit('setShapefileUploadSuccess', false)
          console.error('failed to save shapefile', e.response)
          context.commit('setShapefileUploadMessage', e.response.data.message)
        })
    },
    uploadFiles (context, payload) {
      context.commit('setFilesUploading', true)
      let documentType = payload.documentType
      let recordId = payload.recordId

      // Driller documents are always private
      let isPrivate = context.state.isPrivate
      if (documentType === 'drillers') {
        isPrivate = true
      }

      let uploadPromises = []

      context.state.upload_files.forEach(file => {
        uploadPromises.push(
          ApiService.presignedPutUrl(
            documentType,
            recordId,
            file.name,
            isPrivate
          )
            .then(response => {
              let url = response.data.url
              let objectName = response.data.object_name
              let filename = response.data.filename
              let file = context.state.upload_files.filter(
                file => file.name === objectName
              )

              if (file.length !== 1) {
                context.commit('addError', 'Error uploading file: ' + filename)
                return Promise.reject(
                  new Error('Error uploading file' + filename)
                )
              }

              file = file[0]

              let options = {
                headers: {
                  'Content-Type': file.type
                }
              }

              return ApiService.fileUpload(url, file, options)
                .then(() => {
                  console.log('successfully added file: ' + objectName)
                })
                .catch(error => {
                  console.log(error)
                  context.commit('addError', error)
                  return Promise.reject(error)
                })
            })
            .catch(error => {
              console.log(error)
              context.commit('addError', error)
              return Promise.reject(error)
            })
        )
      })

      return Promise.all(uploadPromises)
    },
    fileUploadSuccess (context) {
      context.commit('setFilesUploading', false)
      context.commit('setFileUploadSuccess', true)
      context.commit('setFiles', [])
      context.commit('setPrivate', false)
      setTimeout(() => {
        context.commit('setFileUploadSuccess', false)
      }, 5000)
    },
    fileUploadFail (context) {
      context.commit('setFilesUploading', false)
      context.commit('setFileUploadError', true)
      context.commit('setFileUploadSuccess', false)
      context.commit('setFiles', [])
      context.commit('setPrivate', false)
    },
    shapefileUploadSuccess (context) {
      context.commit('setShapefileUploadSuccess')
    },
    shapefileUploadFail (context) {
      context.commit('setShapefileUploadSuccess')
    },
    resetUploadFiles (context) {
      context.commit('setFiles', [])
    }
  },
  mutations: {
    addError (state, payload) {
      state.file_upload_errors.push(payload)
    },
    setShapefileUploadMessage (state, payload) {
      state.shapefile_upload_message = payload
    },
    setFilesUploading (state, payload) {
      state.files_uploading = payload
    },
    setShapefileUploading (state, payload) {
      state.shapefile_uploading = payload
    },
    setFileUploadError (state, payload) {
      state.file_upload_error = payload
    },
    setFileUploadSuccess (state, payload) {
      state.file_upload_success = payload
    },
    setShapefileUploadSuccess (state, payload) {
      state.shapefile_uploading = false
      state.shapefile_upload_success = payload
    },
    setFiles (state, payload) {
      if (payload.length > 0) {
        state.upload_files.push(...payload)
      } else {
        state.upload_files = payload
      }
    },
    setShapefile (state, payload) {
      state.shapefile = payload
    },
    removeFile (state, file) {
      state.upload_files = state.upload_files.filter(item => item.name !== file)
    },
    setPrivate (state, payload) {
      state.isPrivate = payload
    }
  }
}
