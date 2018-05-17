import axios from 'axios'

const logging = process.env.NODE_ENV !== 'production'

const ApiService = {
  init () {
    axios.defaults.baseURL = process.env.AXIOS_BASE_URL
    if (logging) {
      console.log('turning on interceptors')
      axios.interceptors.request.use(function (request) {
        console.log(request)
        return request
      }, function (error) {
        console.log(error)
        return Promise.reject(error)
      })
      axios.interceptors.response.use(function (response) {
        console.log(response)
        return response
      }, function (error) {
        console.log(error)
        return Promise.reject(error)
      })
    }
  },
  authHeader (prefix, token) {
    // set auth header. Expects prefix to be "Bearer", "JWT" etc.
    // deletes auth header if called without a token (useful for logging out)
    if (prefix && token) {
      axios.defaults.headers.common['Authorization'] = `${prefix} ${token}`
    } else if (axios.defaults.headers.common['Authorization']) {
      delete axios.defaults.headers.common['Authorization']
    }
  },
  query (resource, params) {
    return axios.get(resource, { params: params })
  },
  get (resource, uuid) {
    if (uuid.length && uuid.length === 36) {
      return axios.get(`${resource}/${uuid}/`)
    }
    throw new Error(`API get: UUID required to fetch ${resource}`)
  },
  post (resource, params) {
    return axios.post(resource + '/', params)
  },
  patch (resource, record, params) {
    return axios.patch(`${resource}/${record}/`, params)
  }
}

export default ApiService
