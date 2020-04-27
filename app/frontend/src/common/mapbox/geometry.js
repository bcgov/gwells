import mapboxgl from 'mapbox-gl'

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
