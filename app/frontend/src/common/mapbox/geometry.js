import mapboxgl from 'mapbox-gl'
import { pick } from 'lodash'

import ApiService from '@/common/services/ApiService.js'
import intersect from '@turf/intersect'

export const CENTRE_LNG_LAT_BC = new mapboxgl.LngLat(-126.495, 54.459)
export const DEFAULT_MAP_ZOOM = 4
export const BC_LAT_LNG_BOUNDS = new mapboxgl.LngLatBounds(new mapboxgl.LngLat(-114.0541379, 60.0023), new mapboxgl.LngLat(-139.0536706, 48.2245556))

// Builds a MapBox LngLat from the feature's geometry
export function getLngLatOfPointFeature (feature) {
  return new mapboxgl.LngLat(...feature.geometry.coordinates)
}

// Extends the bounds based on an array of lng / lat points
export function computeBoundsFromCoords (coords) {
  return coords.reduce((bounds, coord) => {
    return bounds.extend(coord)
  }, new mapboxgl.LngLatBounds(coords[0], coords[0]))
}

// Computes the bounds of a MultiPolygon geometry
export function computeBoundsFromMultiPolygon (coordinates) {
  const bounds = new mapboxgl.LngLatBounds()

  // Loop through MultiPolygon → Polygon → Line array to compute bounds
  coordinates.forEach((polygonCoords) => {
    polygonCoords.forEach((coords) => {
      bounds.extend(computeBoundsFromCoords(coords))
    })
  })

  return bounds
}

export function containsBounds (containerBounds, testBounds) {
  if (!containerBounds.contains(testBounds.getSouthWest())) {
    return false
  } else if (!containerBounds.contains(testBounds.getNorthEast())) {
    return false
  } else if (!containerBounds.contains(testBounds.getNorthWest())) {
    return false
  } else if (!containerBounds.contains(testBounds.getSouthEast())) {
    return false
  }

  return true
}

export function peopleToGeoJSON (people = []) {
  // Converts a list of people from a search of registered well drillers
  // and pump installers into a GeoJSON feature collection.
  // If a person is registered with multiple organizations, it will
  // result in multiple features (because in the source data
  // geospatial location is associated with the organization, not the
  // person)

  const personFeatures = []
  people.forEach(person => {
    person.registrations.forEach(reg => {
      const feature = personOrganizationToGeoJSON(person, reg.organization)
      if (feature.geometry) {
        personFeatures.push(feature)
      }
    })
  })

  return { type: 'FeatureCollection', features: personFeatures }
}

export function personOrganizationToGeoJSON (person, org) {
  // Combines a person and an organization into a single
  // GeoJSON Feature.  (Properties come from the person,
  // geometry comes from the organization.)
  const feature = Object.assign({
    type: 'Feature',
    properties: Object.assign({}, person),
    geometry: null
  })

  if (org && org.longitude && org.latitude) {
    feature.geometry = {
      coordinates: [org.longitude, org.latitude],
      type: 'Point'
    }
  }
  return feature
}

export function buildWellsGeoJSON (wells = [], properties = []) {
  const features = wells.map((well) => {
    return {
      type: 'Feature',
      properties: properties.length > 0 ? pick(well, properties) : properties,
      geometry: {
        type: 'Point',
        coordinates: [well.longitude, well.latitude]
      }
    }
  })

  return {
    type: 'FeatureCollection',
    features
  }
}

export function convertLngLatBoundsToDirectionBounds (lngLatBounds) {
  const sw = lngLatBounds.getSouthWest()
  const ne = lngLatBounds.getNorthEast()

  return {
    sw_lat: sw.lat,
    sw_long: sw.lng,
    ne_lat: ne.lat,
    ne_long: ne.lng
  }
}

export function boundsCompletelyContains (boundsOuter, boundsInner) {
  const boundsPoints = [
    boundsInner.getSouthWest(),
    boundsInner.getSouthEast(),
    boundsInner.getNorthEast(),
    boundsInner.getNorthWest()
  ]

  return boundsPoints.every((coordinate) => {
    return boundsOuter.contains(coordinate)
  })
}

export function isViewingBC (bounds) {
  return containsBounds(bounds, BC_LAT_LNG_BOUNDS)
}

const coordinateLookup = {}

export function fetchInsideBCCheck (longitude, latitude, options) {
  // We use a dictionary to reduce network traffic, by storing and checking for coordinates locally.
  const key = `${latitude};${longitude}`

  if (coordinateLookup[key]) {
    return coordinateLookup[key]
  }

  // We don't a previous request for this lat / lng pair
  const promise = new Promise((resolve, reject) => {
    const params = { latitude, longitude }
    ApiService.query('gis/insidebc', params, options).then((response) => {
      resolve(response.data.inside)
    }, reject)
  })

  coordinateLookup[key] = promise

  return promise
}

export function checkCoordsAreTheSame (lngLat1, lngLat2, precision = 0.00001) {
  if (!lngLat1 || !lngLat2) { return null }

  const { lng: lng1, lat: lat1 } = lngLat1
  const { lng: lng2, lat: lat2 } = lngLat2
  return Math.abs(lat1 - lat2) <= precision && Math.abs(lng1 - lng2) <= precision
}

export function doPolygonsIntersect (f1, f2) {
  const intersection = intersect(f1, f2)
  return (intersection !== null)
}
