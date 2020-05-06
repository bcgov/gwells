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

  return {
    LngLat,
    LngLatBounds
  }
})

jest.mock('@geolonia/mbgl-gesture-handling', () => {})
