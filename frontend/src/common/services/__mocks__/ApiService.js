const ApiService = {
  query: function () {
    return new Promise((resolve, reject) => {
      resolve({ data: ['mock list item 1'] })
    })
  }
}

export default ApiService
