jest.mock('mapbox-gl', () => {
  function LngLat (lng, lat) {
    this.lng = lng
    this.lat = lat
  }

  function LngLatBounds (sw, ne) {
    this.sw = sw
    this.ne = ne
  }

  LngLatBounds.prototype.extend = () => {}

  LngLatBounds.prototype.getSouthWest = () => ({ lat: 0, lng: 0 })
  LngLatBounds.prototype.getSouthWest = () => ({ lat: 0, lng: 0 })
  LngLatBounds.prototype.getNorthEast = () => ({ lat: 0, lng: 0 })
  LngLatBounds.prototype.getNorthEast = () => ({ lat: 0, lng: 0 })

  return {
    LngLat,
    LngLatBounds
  }
})

jest.mock('@geolonia/mbgl-gesture-handling', () => {})
