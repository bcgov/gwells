let response = null

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
  __setMockResponse: function (newResponse) {
    response = newResponse
  }

}

export default ApiService
