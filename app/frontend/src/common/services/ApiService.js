import axios from 'axios'
import qs from 'querystring'

const logging = process.env.NODE_ENV !== 'production'

const ApiService = {
  init () {
    axios.defaults.baseURL = process.env.AXIOS_BASE_URL

    axios.interceptors.request.use(function (request) {
      // log requests to console while logging is on
      logging && console.log(request)

      if (request.method === 'POST') {
        // send data as x-www-form-urlencoded
        request.data = qs.stringify(request.data)
      }
      return request
    }, function (error) {
      logging && console.log(error)
      return Promise.reject(error)
    })
    axios.interceptors.response.use(function (response) {
      logging && console.log(response)
      return response
    }, function (error) {
      logging && console.log(error)
      return Promise.reject(error)
    })
  },
  hasAuthHeader () {
    return !!axios.headers.common['Authorization']
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
  get (resource, record) {
    return axios.get(`${resource}/${record}/`)
  },
  post (resource, params) {
    return axios.post(resource + '/', params)
  },
  patch (resource, record, params) {
    return axios.patch(`${resource}/${record}/`, params)
  },
  options (resource) {
    return axios.options(resource)
  },
  delete (resource, record) {
    return axios.delete(`${resource}/${record}/`)
  },
  history (resource, record) {
    return axios.get(`${resource}/${record}/history/`)
  },
  presignedPutUrl (resource, record, filename) {
    return axios.get(`${resource}/${record}/presigned_put_url?filename=${filename}`)
  },
  // fileUpload uploads a file using a pre-signed S3 URL
  fileUpload (presignedUrl, file) {
    const config = {
      headers: {
        'Content-Type': file.type
      },
      transformRequest: (data, headers) => {
        // delete Authorization header for file upload requests (credentials are via a presigned link)
        delete headers.common['Authorization']
        return data
      }
    }
    return axios.put(presignedUrl, file, config)
  },
  deleteFile (resource) {
    return axios.delete(resource)
  }
}

export default ApiService
