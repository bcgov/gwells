import Vue from 'vue'
import axios from 'axios'
const BASE_URL = 'http://localhost:8000/gwells/registries/'

const ApiService = {
  init () {
    Vue.use(axios)
    axios.defaults.baseURL = BASE_URL
  },
  query (resource, params) {
    return axios.get(resource, { params: params })
      .catch((error) => {
        throw new Error(`API query: ${error}`)
      })
  },
  get (resource, uuid) {
    if (uuid.length && uuid.length === 36) {
      return axios.get(`${resource}/${uuid}`)
        .catch((error) => {
          throw new Error(`API get: ${error}`)
        })
    }
    throw new Error(`API get: UUID required to fetch ${resource}`)
  },
  post (resource, params) {
    return axios.post(resource, params)
      .catch((error) => {
        throw new Error(`API post: ${error}`)
      })
  }
}

export default ApiService
