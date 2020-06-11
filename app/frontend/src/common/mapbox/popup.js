import mapboxgl from 'mapbox-gl'

import { getLngLatOfPointFeature } from './geometry'

// Add onclick handler to use vue router to route to the link for all anchors in a popup
export function wireUpAnchors (el, $router, routes) {
  function onClick (e) {
    if (!e.ctrlKey) {
      e.preventDefault()
      const routeName = e.currentTarget.getAttribute('data-route-name')
      if (!routeName) {
        throw new Error('Anchor without a data-route-name')
      }
      const route = routes[routeName] || null
      if (!route) {
        throw new Error(`Route named "${routeName}" not found in routes`)
      }
      $router.push(route)
    }
  }

  const anchors = el.querySelectorAll('a:not([target="_blank"])')
  for (let i = 0; i < anchors.length; i++) {
    anchors[i].addEventListener('click', onClick)
  }

  return el
}

export function setupFeatureTooltips (map, layers, options = {}) {
  const popup = new mapboxgl.Popup()

  const tooltip = new mapboxgl.Popup({ className: 'mapboxgl-popup-no-interaction' })
  let currentFeature = null

  const layerIds = Object.keys(layers)
  layerIds.reverse()

  map.on('mousemove', (e) => {
    const features = map.queryRenderedFeatures(e.point, { layers: layerIds })

    if (features.length > 0) {
      const feature = features[0]

      const layer = layers[feature.layer.id]

      if (feature !== currentFeature) {
        const contentDiv = layer.createTooltipContent(features, { canInteract: false })
        tooltip.setDOMContent(contentDiv)
        currentFeature = feature

        // Only show tooltip when stuck popup is not open
        if (!tooltip.isOpen() && !popup.isOpen()) {
          map.getCanvas().style.cursor = 'pointer'

          tooltip.addTo(map)
        }
      }

      const lngLat = layer.snapToCenter ? getLngLatOfPointFeature(feature) : e.lngLat

      tooltip.setLngLat(lngLat)
    } else {
      if (currentFeature !== null) {
        currentFeature = null
        tooltip.remove()
        map.getCanvas().style.cursor = ''
      }
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
