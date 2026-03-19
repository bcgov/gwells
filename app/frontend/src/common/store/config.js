import ApiService from '@/common/services/ApiService.js'

export const SET_CONFIG = 'SET_CONFIG'
export const FETCH_CONFIG = 'FETCH_CONFIG'

const config = ({
  state: {
    config: null
  },
  getters: {
    config (state) {
      return state.config
    }
  },
  actions: {
    FETCH_CONFIG (params) {
      // We only fetch config if we don't have a copy cached
      if (this.getters.config === null) {
        return new Promise((resolve, reject) => {
          ApiService.query('config', params)
            .then((response) => {
              this.SET_CONFIG(response.data)
            })
            .catch((error) => {
              reject(error)
            })
        })
      }
    },
    SET_CONFIG (payload) {
      this.config = payload
    }
  }
})

export default config
