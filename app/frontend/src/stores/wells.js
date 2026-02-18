import { defineStore } from 'pinia'
import axios from 'axios'
import ApiService from '@/common/services/ApiService.js'

const cleanParams = (payload) => {
	if (payload === undefined || payload === null) return {}
	return Object.entries(payload).filter(([key, value]) => {
		return !(value === undefined || value === '' || value === null)
	}).reduce((cleanedParams, [key, value]) => {
		cleanedParams[key] = value
		return cleanedParams
	}, {})
}

function buildSearchParams (state) {
	const params = { ...(state && state.searchParams ? state.searchParams : {}) }
	const filters = state && state.searchResultFilters ? state.searchResultFilters : {}

	if (Object.entries(filters).length > 0) {
		params['filter_group'] = JSON.stringify(filters)
	}

	return params
}

export const DEFAULT_COLUMNS = [
	'wellTagNumber',
	'identificationPlateNumber',
	'ownerName',
	'streetAddress',
	'legalLot',
	'legalPlan',
	'legalDistrictLot',
	'landDistrict',
	'legalPid',
	'diameter',
	'finishedWellDepth'
]
const DEFAULT_ORDERING = '-well_tag_number'
const DEFAULT_LIMIT = 10

export const useWellsStore = defineStore('wells', {
	state: () => ({
		error: null,
		drillerNames: [],
		lastSearchTrigger: null,
		locationSearchResults: [],
		organizationNames: [],
		pendingLocationSearch: null,
		pendingSearch: null,
		constrainSearch: true,
		hasSearched: false,
		searchBounds: {},
		searchErrors: {},
		searchLimit: DEFAULT_LIMIT,
		searchOffset: 0,
		searchOrdering: DEFAULT_ORDERING,
		searchParams: {},
		searchResultColumns: DEFAULT_COLUMNS,
		searchResultFilters: {},
		searchResults: null,
		searchResultCount: 0,
		wellId: null,
		wellRecord: {},
		recordLicence: {
			status: '',
			number: ''
		},
		searchMap: {
			centre: null,
			zoom: null
		},
		downloads: null
	}),

	getters: {
		drillerNames: (state) => state.drillerNames,
		lastSearchTrigger: (state) => state.lastSearchTrigger,
		locationSearchResults: (state) => state.locationSearchResults,
		organizationNames: (state) => state.organizationNames,
		constrainSearch: (state) => state.constrainSearch,
		pendingLocationSearch: (state) => state.pendingLocationSearch,
		hasSearched: (state) => state.hasSearched,
		pendingSearch: (state) => state.pendingSearch,
		searchInProgress: (state) => Boolean(state.pendingSearch),
		searchBounds: (state) => state.searchBounds,
		searchErrors: (state) => state.searchErrors,
		searchLimit: (state) => state.searchLimit,
		searchOffset: (state) => state.searchOffset,
		searchOrdering: (state) => state.searchOrdering,
		searchParams: (state) => state.searchParams,
		searchResultColumns: (state) => state.searchResultColumns,
		searchResultFilters: (state) => state.searchResultFilters,
		searchResultCount: (state) => state.searchResultCount,
		searchResults: (state) => state.searchResults,
		well: (state) => state.wellRecord,
		wellLicence: (state) => state.recordLicence,
		storedWellId: (state) => state.wellId,
		searchMapCentre: (state) => state.searchMap.centre,
		searchMapZoom: (state) => state.searchMap.zoom,
		wellFileDownloads: (state) => state.downloads
	},

	actions: {
		setSearchParams (payload) {
			this.searchParams = cleanParams(payload)
		},
		async fetchWellDownloadLinks () {
			if (this.downloads === null) {
				const response = await ApiService.query('wells/extracts')
				this.downloads = response.data
			}
		},

		async fetchDrillerNames () {
			if (this.drillerNames.length === 0) {
				try {
					const response = await ApiService.query('drillers/names')
					this.drillerNames = response.data
				} catch (err) {
					this.error = err.response
				}
			}
		},

		resetWellData () {
			this.wellRecord = {}
			this.recordLicence = { status: '', number: '' }
		},

		async fetchOrganizationNames () {
			if (this.organizationNames.length === 0) {
				try {
					const response = await ApiService.query('organizations/names')
					this.organizationNames = response.data
				} catch (err) {
					this.error = err.response
				}
			}
		},

		resetWellsSearch () {
			if (this.pendingLocationSearch && this.pendingLocationSearch.cancel) {
				this.pendingLocationSearch.cancel()
			}
			if (this.pendingSearch && this.pendingSearch.cancel) {
				this.pendingSearch.cancel()
			}
			if (!localStorage.getItem('userColumnPreferences')) {
				this.searchResultColumns = DEFAULT_COLUMNS
			}

			this.pendingLocationSearch = null
			this.hasSearched = false
			this.pendingSearch = null
			this.constrainSearch = true
			this.searchBounds = {}
			this.searchOrdering = DEFAULT_ORDERING
			this.searchLimit = DEFAULT_LIMIT
			this.searchOffset = 0
			this.searchParams = {}
			this.searchErrors = {}
			this.searchResults = null
			this.searchResultCount = 0
			this.locationSearchResults = []
			this.searchResultFilters = {}
			this.searchMap.centre = null
			this.searchMap.zoom = null
		},

		setSearchResultColumns (payload) {
			this.searchResultColumns = payload
		},

		setSearchResultFilters (payload) {
			this.searchResultFilters = cleanParams(payload || {})
		},

		setSearchOffset (payload) {
			this.searchOffset = payload
		},

		setSearchOrdering (payload) {
			this.searchOrdering = payload
		},

		setSearchLimit (payload) {
			if (!(payload === 10 || payload === 25 || payload === 50)) {
				return
			}
			this.searchLimit = payload
		},

		async searchWells ({ constrain = null, trigger = null } = {}) {
			this.lastSearchTrigger = trigger
			this.hasSearched = true

			if (this.pendingSearch && this.pendingSearch.cancel) {
				this.pendingSearch.cancel()
			}

			const cancelSource = axios.CancelToken.source()
			this.pendingSearch = cancelSource

			if (constrain !== null) {
				this.constrainSearch = constrain
			}

			const params = {
				...buildSearchParams(this),
				ordering: this.searchOrdering,
				limit: this.searchLimit,
				offset: this.searchOffset
			}

			if (this.constrainSearch) {
				Object.assign(params, this.searchBounds)
			}

			try {
				const response = await ApiService.query('wells', params, { cancelToken: cancelSource.token })
				this.searchErrors = {}
				this.searchResults = response.data.results
				this.searchResultCount = response.data.count
			} catch (err) {
				if (axios.isCancel(err)) {
					return
				}

				if (err.response && err.response.data) {
					this.searchErrors = err.response.data
				}
				this.searchResults = null
				this.searchResultCount = 0
			} finally {
				this.pendingSearch = null
			}
		}
	}
})

export default useWellsStore
