const QS_AQUIFER_SEARCH_FEATURE = 'feature=aquifer-search-in-map'

const qs = window.location.search

export const SEARCH_IN_MAP_FEATURE_ENABLED = qs.indexOf(QS_AQUIFER_SEARCH_FEATURE) !== -1

const features = {
  searchInAquiferMap: SEARCH_IN_MAP_FEATURE_ENABLED
}

export default features
