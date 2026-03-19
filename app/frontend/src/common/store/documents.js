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
import { defineStore } from 'pinia'

export default defineStore({
  state: () => ({
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
  }),
  actions: {
    uploadShapefile (payload) {
      const file = this.state.shapefile
      let formData = new FormData()
      formData.append('geometry', file)
      const url = `${payload.documentType}/${payload.recordId}/geometry`
      this.commit('setShapefileUploading', true)
      return ApiService.post(url, formData)
        .then(() => {
          this.commit('setShapefileUploadSuccess', true)
          this.commit('setShapefileUploadMessage', '')
        })
        .catch(e => {
          this.commit('setShapefileUploading', false)
          this.commit('setShapefileUploadSuccess', false)
          console.error('failed to save shapefile', e.response)
          this.commit('setShapefileUploadMessage', e.response.data.message || 'Server Error')
          throw e
        })
    },
    uploadFiles (payload) {
      this.commit('setFilesUploading', true)
      let documentType = payload.documentType
      let recordId = payload.recordId
      const files = payload.files || this.state.upload_files
      const fileNames = payload.fileNames || []

      // Driller documents are always private
      let isPrivate = this.state.isPrivate
      if (documentType === 'drillers') {
        isPrivate = true
      }

      return files.reduce((previousPromise, file, i) => {
        return previousPromise.then((results) => {
          // use override file name if it exists
          let fileName
          if (file.file) {
            fileName = file.file.name
            isPrivate = file.private
            file = file.file
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
                  if (documentType === 'wells') {
                    const fileNameSplit = objectName.split('_')
                    const fileDocumentType = fileNameSplit.length > 2 ? `${fileNameSplit[0]}_${fileNameSplit[1]}` : fileNameSplit[0]
                    ApiService.incrementFileCount(`wells/${recordId}`, fileDocumentType)
                  }
                })
                .catch(error => {
                  console.log(error)
                  this.commit('addError', error)
                  return Promise.reject(error)
                })
            })
            .catch(error => {
              console.log(error)
              this.commit('addError', error)
            })
        })
      }, Promise.resolve())
    },
    fileUploadSuccess () {
      this.commit('setFilesUploading', false)
      this.commit('setFileUploadSuccess', true)
      this.commit('setFiles', [])
      this.commit('setPrivate', false)
      setTimeout(() => {
        this.commit('setFileUploadSuccess', false)
      }, 5000)
    },
    fileUploadFail () {
      this.commit('setFilesUploading', false)
      this.commit('setFileUploadError', true)
      this.commit('setFileUploadSuccess', false)
      this.commit('setFiles', [])
      this.commit('setPrivate', false)
    },
    shapefileUploadSuccess () {
      this.commit('setShapefileUploadSuccess')
    },
    shapefileUploadFail () {
      this.commit('setShapefileUploadSuccess')
    },
    resetUploadFiles () {
      this.commit('setFiles', [])
    },
    clearUploadShapeFileMessage () {
      this.commit('setShapefileUploadMessage', '')
    },
    clearUploadFilesMessage () {
      this.commit('clearErrors')
    },
    addError (payload) {
      this.file_upload_errors.push(payload)
    },
    clearErrors () {
      this.file_upload_errors = []
      this.file_upload_error = false
    },
    setShapefileUploadMessage (payload) {
      this.shapefile_upload_message = payload
    },
    setFilesUploading (payload) {
      this.files_uploading = payload
    },
    setShapefileUploading (payload) {
      this.shapefile_uploading = payload
    },
    setFileUploadError (payload) {
      this.file_upload_error = payload
    },
    setFileUploadSuccess (payload) {
      this.file_upload_success = payload
    },
    setShapefileUploadSuccess (payload) {
      this.shapefile_uploading = false
      this.shapefile_upload_success = payload
    },
    setFiles (payload) {
      if (payload.length > 0) {
        this.upload_files.push(...payload)
      } else {
        this.upload_files = payload
      }
    },
    setShapefile (payload) {
      this.shapefile = payload
    },
    removeFile (file) {
      this.upload_files = this.upload_files.filter(item => item !== file)
    },
    setPrivate (payload) {
      this.isPrivate = payload
    }
  }
})
