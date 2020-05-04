// LayersControl is a MapBox control that allows layers to be toggled
export class LayersControl {
  constructor (options = {}) {
    this.layers = options.layers || []
    this.onChange = options.onChange || function () {}
  }

  onAdd (map) {
    this._map = map
    this._container = document.createElement('div')
    this._container.className = 'mapboxgl-ctrl mapboxgl-ctrl-group mapbox-control-layers'

    const ol = document.createElement('ol')
    this.layers.forEach((layer) => {
      const layerId = layer.id
      const li = document.createElement('li')
      li.className = 'mb-1'

      const checked = layer.show ? 'checked' : ''
      li.innerHTML =
      '<label>' +
        '<input type="checkbox" ' + checked + '>' +
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
    this._container.className = 'mapboxgl-ctrl mapboxgl-ctrl-group mapbox-control-legend'
    this._container.innerHTML = `<div class="m-1 text-center">Legend</div>`

    this._legendControlContent = document.createElement('div')

    this._legendControlContent.className = 'mapbox-control-legend-content'
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
