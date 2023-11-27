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
      return ApiService.post(url, formData)
        .then(() => {
          context.commit('setShapefileUploadSuccess', true)
          context.commit('setShapefileUploadMessage', '')
        })
        .catch(e => {
          context.commit('setShapefileUploading', false)
          context.commit('setShapefileUploadSuccess', false)
          console.error('failed to save shapefile', e.response)
          context.commit('setShapefileUploadMessage', e.response.data.message || 'Server Error')
          throw e
        })
    },
    uploadFiles (context, payload) {
      context.commit('setFilesUploading', true)
      let documentType = payload.documentType
      let recordId = payload.recordId
      const files = payload.files || context.state.upload_files
      const fileNames = payload.fileNames || []

      // Driller documents are always private
      let isPrivate = context.state.isPrivate
      if (documentType === 'drillers') {
        isPrivate = true
      }

      return files.reduce((previousPromise, file, i) => {
        return previousPromise.then((results) => {
          // use override file name if it exists
          let fileName;
          if(file.file){
            fileName = file.file.name;
            isPrivate = file.private;
            file = file.file;
          } else {
            fileName = fileNames[i] || file.name
          }
          return ApiService.presignedPutUrl(
            documentType,
            recordId,
            encodeURIComponent(fileName),
            isPrivate
          )
            .then(response => {
              let url = response.data.url
              let objectName = response.data.object_name

              let options = {
                headers: {
                  'Content-Type': file.type
                }
              }

              return ApiService.fileUpload(url, file, options)
                .then(() => {
                  console.log('successfully added file: ' + objectName)
                  if(documentType === "wells"){
                    const fileNameSplit = objectName.split("_");
                    const fileDocumentType = fileNameSplit.length > 2 ? `${fileNameSplit[0]}_${fileNameSplit[1]}` : fileNameSplit[0];
                    ApiService.incrementFileCount(`wells/${recordId}`, fileDocumentType)
                  }
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
            })
        })
      }, Promise.resolve())
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
    },
    clearUploadShapeFileMessage (context) {
      context.commit('setShapefileUploadMessage', '')
    },
    clearUploadFilesMessage (context) {
      context.commit('clearErrors')
    }
  },
  mutations: {
    addError (state, payload) {
      state.file_upload_errors.push(payload)
    },
    clearErrors (state) {
      state.file_upload_errors = []
      state.file_upload_error = false
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
      state.upload_files = state.upload_files.filter(item => item !== file)
    },
    setPrivate (state, payload) {
      state.isPrivate = payload
    }
  }
}
