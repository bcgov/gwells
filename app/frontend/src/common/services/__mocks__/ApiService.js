let response = null
let patch = null

const ApiService = {
  query: function () {
    return new Promise((resolve, reject) => {
      resolve({ data: ['mock list item 1'] })
    })
  },
  get: function (resource, uuid) {
    return new Promise((resolve, reject) => {
      resolve({ data: response })
    })
  },
  patch: function (resource, record, params) {
    patch = {
      record, params
    }
    return new Promise((resolve, reject) => {
      resolve({data: response})
    })
  },
  post (resource, params) {
    return new Promise((resolve, reject) => {
      resolve({data: response})
    })
  },
  options (resource) {
    return new Promise((resolve, reject) => {
      resolve({data: response})
    })
  },
  delete (resource, record) {
    return new Promise((resolve, reject) => {
      resolve({data: response})
    })
  },
  history (resource, record) {
    return new Promise((resolve, reject) => {
      resolve({data: response})
    })
  },
  __setMockResponse: function (newResponse) {
    response = newResponse
  },
  __getMockPatch: function () {
    return patch
  }

}

export default ApiService
