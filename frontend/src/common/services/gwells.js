import axios from 'axios'
const BASE_URL = 'http://localhost:8000/gwells/registries/'

const ApiService = {
  init () {
    axios.defaults.baseURL = BASE_URL
  },
  query (resource, params) {
    return axios.get(resource, { params: params })
  },
  get (resource, uuid) {
    if (uuid.length && uuid.length === 36) {
      return axios.get(`${resource}/${uuid}`)
    }
    throw new Error(`API get: UUID required to fetch ${resource}`)
  },
  post (resource, params) {
    return axios.post(resource, params)
  }
}

export default ApiService
