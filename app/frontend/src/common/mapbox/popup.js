import mapboxgl from 'mapbox-gl'

import { getLngLatOfPointFeature } from './geometry'

export function setupFeatureTooltips (map, layers, options = {}) {
  const popup = new mapboxgl.Popup()

  const tooltip = new mapboxgl.Popup({ className: 'mapboxgl-popup-no-interaction' })
  let currentLayerId = null
  let currentFeatureId = null

  const layerIds = Object.keys(layers)
  layerIds.reverse()

  map.on('mousemove', (e) => {
    const features = map.queryRenderedFeatures(e.point, { layers: layerIds })

    if (features.length > 0) {
      const feature = features[0]

      const layer = layers[feature.layer.id]

      if (layer.id !== currentLayerId && feature.id !== currentFeatureId) {
        const contentDiv = layer.createTooltipContent(features, { canInteract: false })
        tooltip.setDOMContent(contentDiv)
        currentFeatureId = feature.id

        // Only show tooltip when stuck popup is not open
        if (!tooltip.isOpen() && !popup.isOpen()) {
          map.getCanvas().style.cursor = 'pointer'

          tooltip.addTo(map)
        }
      }

      const lngLat = layer.snapToCenter ? getLngLatOfPointFeature(feature) : e.lngLat

      tooltip.setLngLat(lngLat)
    } else {
      currentLayerId = null
      currentFeatureId = null
      tooltip.remove()
      map.getCanvas().style.cursor = ''
    }
  })

  map.on('click', (e) => {
    const features = map.queryRenderedFeatures(e.point, { layers: layerIds })

    if (features.length > 0) {
      const feature = features[0]
      const layerId = feature.layer.id
      const layer = layers[layerId]

      const contentDiv = layer.createTooltipContent(features, { canInteract: true })

      popup
        .setDOMContent(contentDiv)
        .setLngLat(tooltip.getLngLat())
        .addTo(map)
      tooltip.remove()
    }
  })

  map.on('reset', () => {
    popup.remove()
    tooltip.remove()
  })
}

// Creates a list of popup items
export function popupItems (items, $router, options = {}) {
  const canInteract = Boolean(options.canInteract)
  const ol = document.createElement(options.nodeName || 'ol')
  ol.className = (options.className || '') + ` mapbox-${canInteract ? 'popup' : 'tooltip'}-items`

  items.forEach((item) => {
    if (item) {
      ol.appendChild(popupItem(item, $router, options))
    }
  })

  return ol
}

// Creates a popup item with an optional prefix and suffix and link
export function popupItem (item, $router, options = {}) {
  const canInteract = Boolean(options.canInteract)

  const li = document.createElement('li')

  if (typeof item === 'object') {
    li.className = item.className || ''
    if (item.prefix) {
      const prefixEl = document.createElement('span')
      prefixEl.className = 'mapbox-popup-prefix'
      prefixEl.textContent = item.prefix
      li.appendChild(prefixEl)
    }
    if (item.url || item.route) {
      // { name: 'aquifers-view', params: { id: aquiferId } }
      if (canInteract) {
        const anchor = popupLink(item.url || item.route, $router, item.text)
        li.appendChild(anchor)
      } else {
        li.appendChild(document.createTextNode(item.text))
      }
    } else if (item.text) {
      li.appendChild(document.createTextNode(item.text))
    }
    if (item.el) {
      li.appendChild(item.el)
    }
    if (item.suffix) {
      const suffixEl = document.createElement('span')
      suffixEl.className = 'mapbox-popup-suffix'
      suffixEl.textContent = item.suffix
      li.appendChild(suffixEl)
    }
  } else {
    li.innerText = item
  }

  return li
}

// Creates an HTML anchor to a Vue route or URL
export function popupLink (route, $router, text) {
  const anchor = document.createElement('a')
  let url = route

  if (typeof route === 'string') {
    if (url && url.startsWith('http')) {
      anchor.setAttribute('target', '_blank')
    }
  } else {
    url = $router.resolve(route).href
    anchor.onclick = (e) => {
      if (!e.ctrlKey) {
        e.preventDefault()
        $router.push(route)
      }
    }
  }

  anchor.setAttribute('href', url)
  anchor.textContent = text || ''

  return anchor
}
