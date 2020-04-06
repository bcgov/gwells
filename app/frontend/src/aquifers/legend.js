export function buildLegendHTML (items) {
  let html = []
  html.push('<div class="m-1 text-center">Legend</div>')
  html.push('<ul class="p-0 m-0" style="list-style-type: none;">')
  Object.keys(items).forEach((name) => {
    const l = items[name]
    if (l.show) {
      if (typeof l.legend === 'string') {
        html.push(`<li class="m-1"><img src="${l.legend}">${l.layerName}</li>`)
      } else {
        html.push('<ol class="p-0 m-0" style="list-style-type: none;">')
        Object.keys(l.legend).forEach((subName) => {
          const subItem = l.legend[subName]
          html.push(`<li class="m-1 p-0"><img src="${subItem.imageSrc}">${l.layerName} - ${subItem.name}`)
        })
        html.push('</ol>')
        html.push('</li>')
      }
    }
  })
  html.push('</ul>')

  return html.join('\n')
}
