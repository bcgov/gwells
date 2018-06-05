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
  __setMockResponse: function (newResponse) {
    response = newResponse
  },
  __getMockPatch: function () {
    return patch
  }

}

export default ApiService
