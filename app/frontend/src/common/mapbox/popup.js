// Add onclick handler to use vue router to route to the link for all anchors in a popup
export function wireUpAnchors (el, $router, routes) {
  function onClick (e) {
    if (!e.ctrlKey) {
      e.preventDefault()
      const routeName = e.currentTarget.getAttribute('data-route-name')
      $router.push(routes[routeName])
    }
  }

  const anchors = el.querySelectorAll('a')
  for (let i = 0; i < anchors.length; i++) {
    anchors[i].addEventListener('click', onClick)
  }

  return el
}
