import mapboxgl from 'mapbox-gl'

export class PulsingDotImage {
  constructor (map, options = {}) {
    this._map = map
    const {
      size = 90,
      dotColour = 'rgba(255, 255, 255, 0.1)',
      dotStrokeColour = 'rgba(0, 0, 0, 0.1)',
      pulseColour = 'rgba(255, 255, 255, %d)'
    } = options

    this._size = size
    this._dotColour = dotColour
    this._dotStrokeColour = dotStrokeColour
    this._pulseColour = pulseColour
    this.width = size
    this.height = size
    this.data = new Uint8Array(size * size * 4)
  }

  // get rendering context for the map canvas when layer is added to the map
  onAdd () {
    var canvas = document.createElement('canvas')
    canvas.width = this._size
    canvas.height = this._size
    this.context = canvas.getContext('2d')
  }

  // called once before every frame where the icon will be used
  render () {
    var duration = 1000
    var t = (performance.now() % duration) / duration

    var radius = (this._size / 2) * 0.3
    var outerRadius = (this._size / 2) * 0.7 * t + radius
    var context = this.context

    // draw outer circle
    context.clearRect(0, 0, this._size, this._size)
    context.beginPath()
    context.arc(
      this._size / 2,
      this._size / 2,
      outerRadius,
      0,
      Math.PI * 2
    )
    context.fillStyle = this._pulseColour.replace('%d', (1 - t))
    context.fill()

    // draw inner circle
    context.beginPath()
    context.arc(
      this._size / 2,
      this._size / 2,
      radius - 2,
      0,
      Math.PI * 2
    )
    context.fillStyle = this._dotColour
    context.strokeStyle = this._dotStrokeColour
    context.lineWidth = 3
    context.fill()
    context.stroke()

    // pulse circle
    context.beginPath()
    context.strokeStyle = 'rgba(255, 255, 255, 0.5)'
    context.arc(
      this._size / 2,
      this._size / 2,
      radius,
      0,
      Math.PI * 2
    )
    context.lineWidth = 2 + 4 * (1 - t)
    context.stroke()

    // update this image's data with data from the canvas
    this.data = context.getImageData(0, 0, this._size, this._size).data

    // continuously repaint the map, resulting in the smooth animation of the dot
    this._map.triggerRepaint()

    // return `true` to let the map know that the image was updated
    return true
  }
}

export class PulsingWellImage extends PulsingDotImage {
  constructor (map) {
    super(map, {
      size: 90,
      dotColour: 'rgba(0, 173, 252, 1)',
      dotStrokeColour: 'rgba(0, 0, 0, 1)',
      pulseColour: 'rgba(243, 255, 255, %d)'
    })
  }
}

export class PulsingArtesianWellImage extends PulsingDotImage {
  constructor (map) {
    super(map, {
      size: 90,
      dotColour: 'rgba(0, 173, 252, 1)',
      dotStrokeColour: 'rgba(218, 25, 200, 1)',
      pulseColour: 'rgba(255, 235, 253, %d)'
    })
  }
}

export function buildLeafletStyleMarker (longitude, latitude, options = {}) {
  const element = document.createElement('div')
  element.className = 'map-pin'

  const marker = new mapboxgl.Marker({ element, anchor: 'bottom', ...options })
  if (longitude && latitude) {
    marker.setLngLat([longitude, latitude])
  }

  const spinner = document.createElement('span')
  spinner.className = 'map-pin-spinner'
  element.appendChild(spinner)

  return marker
}
