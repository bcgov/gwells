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

  function Map (options = {}) { } // NOSONAR
  Map.prototype.addControl = () => { }
  Map.prototype.on = () => {}

  function NavigationControl (options = {}) { }
  function GeolocateControl (options = {}) { }
  function ScaleControl (options = {}) { }
  function AttributionControl (options = {}) { }
  function supported () { return true }

  return {
    LngLat,
    LngLatBounds,
    Map,
    NavigationControl,
    GeolocateControl,
    ScaleControl,
    AttributionControl,
    supported
  }
})

jest.mock('@geolonia/mbgl-gesture-handling', () => {
  class GestureHandling {
    // eslint-disable-next-line
    constructor (options = {}) { }
    addTo = (map) => { }
  }
  return GestureHandling
})
