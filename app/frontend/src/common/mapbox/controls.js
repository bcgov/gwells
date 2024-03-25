import mapboxgl from 'mapbox-gl'
import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder'

import { CENTRE_LNG_LAT_BC, DEFAULT_MAP_ZOOM } from './geometry'

// LayersControl is a MapBox control that allows layers to be toggled
export class LayersControl {
  constructor (options = {}) {
    this.layers = options.layers || []
    this.onChange = options.onChange || function () {}
  }

  onAdd (map) {
    this._map = map
    this._container = document.createElement('div')
    this._container.className = 'mapboxgl-ctrl mapboxgl-ctrl-group mapbox-ctrl-layers'

    const ol = document.createElement('ol')
    const totalNumLayers = this.layers.length
    this.layers.forEach((layer, i) => {
      const layerId = layer.id
      const li = document.createElement('li')
      li.className = (totalNumLayers - 1 === i) ? '' : 'mb-1'

      const checked = layer.show ? 'checked' : ''
      li.innerHTML =
      '<label>' +
        `<input data-layer-id="${layerId}" type="checkbox" ${checked}>` +
        '<span> ' + layer.label + '</span>' +
      '</label>'
      const checkbox = li.querySelector('input')
      checkbox.onchange = (e) => {
        this.onChange(layerId, e.currentTarget.checked)
      }

      ol.appendChild(li)
    })

    this._container.appendChild(ol)

    return this._container
  }

  update () {
    this.layers.forEach((layer) => {
      const checkbox = this._container.querySelector(`input[data-layer-id="${layer.id}"]`)
      if (checkbox) {
        checkbox.checked = layer.show
      }
    })
  }

  onRemove () {
    this._container.parentNode.removeChild(this._container)
    this._map = undefined
  }
}

// LegendControl is a MapBox control to display the legend of visible layers
export class LegendControl {
  constructor (options = {}) {
    this.layers = options.layers || []
  }

  onAdd (map) {
    this._map = map
    this._container = document.createElement('div')
    this._container.className = 'mapboxgl-ctrl mapboxgl-ctrl-group mapbox-ctrl-legend'
    this._container.innerHTML = `<div class="m-1 text-center">Legend</div>`

    this._legendControlContent = document.createElement('div')

    this._legendControlContent.className = 'mapbox-ctrl-legend-content'
    this._container.appendChild(this._legendControlContent)

    this.update()

    return this._container
  }

  onRemove () {
    this._container.parentNode.removeChild(this._container)
    this._map = undefined
  }

  update () {
    let html = []
    html.push('<ul class="p-0 m-0">')
    this.layers.forEach((l) => {
      if (l.show) {
        if (l.legend) {
          html.push('<ol class="p-0 m-0">')
          l.legend.forEach((subItem) => {
            html.push(`<li class="m-1 p-0"><img src="${subItem.imageSrc}">${l.label} – ${subItem.label}`)
          })
          html.push('</ol>')
          html.push('</li>')
        } else {
          html.push(`<li class="m-1"><img src="${l.imageSrc}">${l.label}</li>`)
        }
      }
    })
    html.push('</ul>')

    this._legendControlContent.innerHTML = html.join('\n')
  }
}

// BoxZoomControl is a MapBox control allows the user to draw a box to zoom to
export class BoxZoomControl {
  constructor (options = {}) {
    this.onZoom = options.onZoom || function () {}
    this.enabled = false
    this.suppressClickEvent = options.suppressClickEvent || false

    this._start = null
    this._current = null
    this._box = null
    this._canvas = null

    this.toggleBoxZoom = this.toggleBoxZoom.bind(this)
    this.onMouseDown = this.onMouseDown.bind(this)
    this.onMouseMove = this.onMouseMove.bind(this)
    this.onMouseUp = this.onMouseUp.bind(this)
    this.onKeyDown = this.onKeyDown.bind(this)
  }

  onAdd (map) {
    this._map = map

    this._canvas = this._map.getCanvasContainer()

    this._container = document.createElement('div')
    this._container.className = 'mapboxgl-ctrl mapboxgl-ctrl-group mapboxgl-ctrl-box-zoom'

    const button = document.createElement('button')
    button.type = 'button'
    button.ariaLabel = 'Zooms to box'
    button.title = 'Zooms to box'
    button.innerHTML = '<span class="mapboxgl-ctrl-icon" aria-hidden="true"></span>'

    button.onclick = this.toggleBoxZoom

    this._container.appendChild(button)

    return this._container
  }

  onRemove () {
    this.finish() // cleanup events
    this._container.parentNode.removeChild(this._container)
    this._map = undefined

    this._start = null
    this._current = null
    this._box = null
    this._canvas = null
    this.enabled = false
  }

  toggleBoxZoom () {
    if (!this.enabled) {
      this.startBoxZoom()
    } else {
      this.endBoxZoom()
    }
  }

  startBoxZoom () {
    this.enabled = true

    this._map.boxZoom.disable()
    this._map.dragPan.disable()

    this._canvas.addEventListener('mousedown', this.onMouseDown, true)

    this._container.classList.add('active')
  }

  endBoxZoom () {
    this.enabled = false

    this._map.boxZoom.enable()
    this._map.dragPan.enable()

    this._canvas.removeEventListener('mousedown', this.onMouseDown, true)

    this._container.classList.remove('active')

    this._container.firstChild.blur()
  }

  onMouseDown (e) {
    // Call functions for the following events
    document.addEventListener('mousemove', this.onMouseMove)
    document.addEventListener('mouseup', this.onMouseUp)
    document.addEventListener('keydown', this.onKeyDown)

    // Capture the first xy coordinates
    this._start = this.mousePos(e)
  }

  // Return the xy coordinates of the mouse position
  mousePos (e) {
    var rect = this._canvas.getBoundingClientRect()
    const x = e.clientX - rect.left - this._canvas.clientLeft
    const y = e.clientY - rect.top - this._canvas.clientTop
    return new mapboxgl.Point(x, y)
  }

  onMouseMove (e) {
    // Capture the ongoing xy coordinates
    const current = this.mousePos(e)

    // Append the box element if it doesnt exist
    if (!this._box) {
      this._box = document.createElement('div')
      this._box.className = 'boxdraw'
      this._canvas.appendChild(this._box)
    }

    const minX = Math.min(this._start.x, current.x)
    const maxX = Math.max(this._start.x, current.x)
    const minY = Math.min(this._start.y, current.y)
    const maxY = Math.max(this._start.y, current.y)

    // Adjust width and xy position of the box element ongoing
    const pos = 'translate(' + minX + 'px,' + minY + 'px)'
    this._box.style.transform = pos
    this._box.style.WebkitTransform = pos
    this._box.style.width = maxX - minX + 'px'
    this._box.style.height = maxY - minY + 'px'
  }

  onMouseUp (e) {
    if (this.enabled && this.suppressClickEvent) {
      // Listen for the click event so we can stop it from propagating.
      // In some cases, this may allow the control to interoperate better
      // with other controls and map event handlers.
      document.addEventListener('click', this.suppressClick, true)
    }
    // Capture xy coordinates
    this.finish(this.mousePos(e))
  }

  onKeyDown (e) {
    // If the ESC key is pressed
    if (e.keyCode === 27) {
      this.finish()
    }
  }

  suppressClick = (clickEvent) => {
    // Stop a click event from being propagated.
    clickEvent.stopPropagation()
    // Remove this event handler so future click events are
    // processed normally
    document.removeEventListener('click', this.suppressClick, true)
  }

  finish (endPoint) {
    // Remove these events now that finish has been called.
    document.removeEventListener('mousemove', this.onMouseMove)
    document.removeEventListener('mouseup', this.onMouseUp)
    document.removeEventListener('keydown', this.onKeyDown)

    if (this._box) {
      this._box.parentNode.removeChild(this._box)
      this._box = null
    }

    if (this._start && endPoint) { // NOTE: this._start is null when vue hot reloads the map component
      var startLngLat = this._map.unproject(this._start)
      var endLngLat = this._map.unproject(endPoint)
      this.onZoom(new mapboxgl.LngLatBounds(startLngLat, endLngLat))
    }

    this.endBoxZoom()
  }
}

// SearchAreaControl is a MapBox control to trigger a search in a specific area
export class SearchAreaControl {
  constructor (options = {}) {
    this.onClick = options.onClick || function () {}
    this.isShown = !!options.show
  }

  onAdd (map) {
    this._map = map
    this._container = document.createElement('div')
    this._container.className = 'mapboxgl-ctrl mapboxgl-ctrl-group mapboxgl-ctrl-search-area' + (this.isShown ? 'show' : '')

    const button = document.createElement('button')
    button.type = 'button'
    button.className = 'btn btn-default'
    button.innerHTML = 'Search this area'
    button.onclick = this.onClick

    this._container.appendChild(button)

    return this._container
  }

  onRemove () {
    this._container.parentNode.removeChild(this._container)
    this._map = undefined
  }

  hide () {
    this.isShown = false
    this._container.classList.remove('show')
  }

  show () {
    this.isShown = true
    this._container.classList.add('show')
  }
}

// DataBCGeocoder is the MapboxGeocoder which uses DataBC to geocode addresses
export class DataBCGeocoder extends MapboxGeocoder {
  constructor (options = {}) {
    super({
      // fake access token copied from:
      // https://github.com/mapbox/parse-mapbox-token/blob/c84408f016b9b540f3dc341e332db0613713f2ca/test.js#L8
      accessToken: 'pk.eyJ1IjoiZmFrZXVzZXIiLCJhIjoicHBvb2xsIn0.sbihZCZJ56-fsFNKHXF8YQ',
      // Use our API endpoint to query DataBC
      origin: process.env.VUE_APP_AXIOS_BASE_URL,
      collapsed: true,
      ...options,
      mapboxgl
    })
  }
}

// ViewBCControl is a MapBox control which zooms to fit BC on the map
export class ViewBCControl {
  onAdd (map) {
    this._map = map
    this._container = document.createElement('div')
    this._container.className = 'mapboxgl-ctrl mapboxgl-ctrl-group mapboxgl-ctrl-view-bc'

    const button = document.createElement('button')
    button.type = 'button'
    button.className = 'btn btn-default'
    button.innerHTML = 'View all of BC'
    button.onclick = this.zoomToBC

    this._container.appendChild(button)

    return this._container
  }

  onRemove () {
    this._container.parentNode.removeChild(this._container)
    this._map = undefined
  }

  zoomToBC () {
    this._map.flyTo({ center: CENTRE_LNG_LAT_BC, zoom: DEFAULT_MAP_ZOOM })
  }
}

// SearchOnMoveControl is a MapBox control for the map's search as I move behaviour
export class SearchOnMoveControl {
  constructor (options = {}) {
    this.options = options

    this._onSearchThisArea = this.options.onSearchThisArea || function () {}
    this._onSearchAsIMove = this.options.onSearchAsIMove || function () {}
    this._searchOnMapMove = Boolean(options.searchOnMapMove) || true
    this._loading = false
    this._showSearchAreaButton = false
    this._isShown = options.show === undefined ? true : !!options.show // show control by default
  }

  onAdd (map) {
    this._map = map
    this._container = document.createElement('div')
    this._container.className = 'mapboxgl-ctrl mapboxgl-ctrl-group mapboxgl-ctrl-search-on-move'
    this._container.hidden = !this._isShown

    this._loadingEl = document.createElement('div')
    this._loadingEl.className = 'm-2'
    this._loadingEl.innerHTML = '' +
      '<div class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></div>' +
      '<strong class="pl-1">Loading...</strong>'

    this._searchAreaButtonEl = document.createElement('button')
    this._searchAreaButtonEl.type = 'button'
    this._searchAreaButtonEl.className = 'btn btn-light btn-sm p-2'
    this._searchAreaButtonEl.innerHTML = 'Search this area <span class="pl-1 fa fa-refresh" />'
    this._searchAreaButtonEl.onclick = (e) => this.searchAreaButtonClicked(e)

    this._searchOnMoveEl = document.createElement('div')
    this._searchOnMoveEl.className = 'custom-control custom-checkbox m-2'
    this._searchOnMoveEl.innerHTML = '' +
      '<input id="search-as-i-move-checkbox" type="checkbox" autocomplete="off" class="custom-control-input">' +
      '<label for="search-as-i-move-checkbox" class="custom-control-label">' +
      '  Search as I move the map' +
      '</label>'

    this._searchAsIMoveCheckbox = this._searchOnMoveEl.querySelector('#search-as-i-move-checkbox')
    this._searchAsIMoveCheckbox.checked = this._searchOnMapMove
    this._searchAsIMoveCheckbox.onchange = (e) => this.onSearchAsIMoveChange(e)

    this._container.appendChild(this._loadingEl)
    this._container.appendChild(this._searchAreaButtonEl)
    this._container.appendChild(this._searchOnMoveEl)

    this.update()

    return this._container
  }

  onRemove () {
    this._container.parentNode.removeChild(this._container)
    this._map = undefined
    this._loadingEl = undefined
    this._searchAreaButtonEl = undefined
    this._searchOnMoveEl = undefined

    this._loading = false
    this._showSearchAreaButton = false
  }

  searchAreaButtonClicked (e) {
    this._onSearchThisArea(e)
  }

  onSearchAsIMoveChange (e) {
    this._showSearchAreaButton = !e.currentTarget.checked
    this.update()
    this._onSearchAsIMove(e)
  }

  loading (isLoading) {
    this._isLoading = Boolean(isLoading)
    this.update()
  }

  showSearchAreaButton (show) {
    this._showSearchAreaButton = Boolean(show)
    this._searchAsIMoveCheckbox.checked = !show
    this.update()
  }

  update () {
    if (this._isLoading) {
      this._loadingEl.removeAttribute('hidden')
      this._searchAreaButtonEl.setAttribute('hidden', true)
      this._searchOnMoveEl.setAttribute('hidden', true)
    } else if (this._showSearchAreaButton) {
      this._loadingEl.setAttribute('hidden', true)
      this._searchAreaButtonEl.removeAttribute('hidden')
      this._searchOnMoveEl.setAttribute('hidden', true)
    } else {
      this._loadingEl.setAttribute('hidden', true)
      this._searchAreaButtonEl.setAttribute('hidden', true)
      this._searchOnMoveEl.removeAttribute('hidden')
    }
  }

  toggleShow (show) {
    this._isShown = show === undefined ? !this._isShown : !!show
    this._container.hidden = !this._isShown
  }
}

// ClearSearchCriteriaControl is a MapBox control for a button to clear the search criteria
export class ClearSearchCriteriaControl {
  constructor (options = {}) {
    this._onClearClick = options.onClearClick || function () {}
    this._isShown = options.show === undefined ? true : !!options.show // show control by default
  }

  onAdd (map) {
    this._map = map
    this._container = document.createElement('div')
    this._container.className = 'mapboxgl-ctrl mapboxgl-ctrl-clear-search-criteria ml-5'
    this._container.hidden = !this._isShown

    const messageEl = document.createElement('div')
    messageEl.className = 'mapboxgl-ctrl-clear-search-criteria-active-search-info py-1 px-3 mb-1 font-weight-bold'
    messageEl.innerHTML = 'Wells that match active search criteria are highlighted.'

    const button = document.createElement('button')
    button.type = 'button'
    button.className = 'btn btn-light btn-sm mb-1 ml-2'
    button.innerHTML = 'Clear search criteria'
    button.onclick = (e) => this.clearClicked(e)

    this._container.appendChild(messageEl)
    this._container.appendChild(button)

    return this._container
  }

  onRemove () {
    this._container.parentNode.removeChild(this._container)
    this._map = undefined
  }

  clearClicked (e) {
    this._onClearClick(e)
  }

  toggleShow (show) {
    this._isShown = show === undefined ? !this._isShown : !!show
    this._container.hidden = !this._isShown
  }
}
