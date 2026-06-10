import { defineStore } from 'pinia'
import ApiService from '@/common/services/ApiService.js'

export const useSubmissionStore = defineStore('submission', {
	state: () => ({
		error: null,
		_codes: null,
		wells: null
	}),

	getters: {
		codes: (state) => state._codes || {
			land_district_codes: {}
		},
		globalError: (state) => state.error
	},

	actions: {
		async fetchCodes () {
			if (this._codes === null) {
				try {
					const response = await ApiService.query('submissions/options')
					this._codes = response.data
				} catch (err) {
					this.error = err.response
				}
			}
		},

		async fetchWellTags () {
			if (this.wells === null) {
				try {
					const response = await ApiService.query('wells/tags?ordering=well_tag_number')
					this.wells = response.data
				} catch (err) {
					this.error = err.response
				}
			}
		}
	}
})

export default useSubmissionStore
