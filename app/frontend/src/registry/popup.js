import { REGISTRY_FILL_LAYER_ID, SEARCHED_REGISTRIES_LAYER_ID, toggleRegistryHover } from '../common/mapbox/layers'
import { popupItems, popupItem } from '../common/mapbox/popup'
import { uniqBy } from 'lodash'

export function createRegistrySearchResultPopupElement (features, map, $router, options = { pageSize: 1 }) {
  // Creates a DOM element that will hold the popup content for
  // the given list of features.  If there are many features, it
  // may not be possible to show all in the popup simultaneously.
  // In this case, only a subset are shown at any given time, and
  // paging controls are shown ('next' and 'previous'  buttons)
  // param features: a list of features on the map that are
  // below the mouse cursor

  const domElement = document.createElement('div')
  domElement.setAttribute('class', 'mapbox-popup-items mt-1')
  const currentPageElement = document.createElement('div')
  domElement.appendChild(currentPageElement)
  const personDomElements = []
  features.forEach(feature => {
    if (feature.layer.id === SEARCHED_REGISTRIES_LAYER_ID) {
      const personDomElement = createPersonElement(feature, $router)
      personDomElements.push(personDomElement)
    }
  })

  const drawPage = (items) => {
    currentPageElement.innerHTML = ''
    items.forEach(item => currentPageElement.appendChild((item)))
  }

  const pageHandler = createPageHandler(personDomElements, options.pageSize)
  pageHandler.listen(drawPage)

  // add paging controls
  if (features.length > 1) {
    domElement.appendChild(createPagingElement(pageHandler))
  }

  pageHandler.notify()

  return domElement
}

function createPageHandler (items, pageSize = 1) {
  // Create an object which stores state related to search result "paging".
  // For example, it stores the curent (visible) page.  It also includes
  // functions to advance to the next or previous page.

  function PageHandler (items, pageSize) {
    this.items = items
    this.pageSize = pageSize
    this.numPages = Math.ceil(items.length / pageSize)
    this.currentPage = 0
    this.itemStartIndex = null
    this.itemEndIndex = null
    this.listeners = []

    this.prev = () => { if (!this.isFirstPage()) { this.currentPage--; this.onPageChanged() } }
    this.next = () => { if (!this.isLastPage()) { this.currentPage++; this.onPageChanged() } }
    this.onPageChanged = () => {
      this.itemStartIndex = this.currentPage * this.pageSize
      this.itemEndIndex = Math.min(this.itemStartIndex + this.pageSize - 1, this.items.length - 1)
      this.notify()
    }
    this.isFirstPage = () => this.currentPage === 0
    this.isLastPage = () => this.currentPage === this.numPages - 1
    this.notify = () => this.listeners.forEach(callback => { callback(this.items.slice(this.itemStartIndex, this.itemEndIndex + 1)) })
    this.listen = (callback) => this.listeners.push(callback)

    // initialize
    this.onPageChanged()
  }

  return new PageHandler(items, pageSize)
}

function createPersonElement (person, $router) {
  const canInteract = true
  const parentElement = document.createElement('div')
  parentElement.setAttribute('class', 'card mb-1 p-1')

  const personProps = person.properties

  // The 'registrations' property is serialized as a JSON string.
  // Deserialize it.
  const registrations = JSON.parse(person.properties.registrations)

  // Use the organization from the first registration
  const org = registrations[0].organization

  const contactItems = [
    {
      prefix: 'Name: ',
      text: `${personProps.surname}, ${personProps.first_name}`
    },
    {
      prefix: 'Company: ',
      text: org.name
    },
    {
      prefix: 'Address: ',
      text: `${org.street_address}, ${org.city}`
    },
    {
      prefix: 'Phone: ',
      text: org.main_tel
    },
    {
      prefix: 'Email: ',
      url: `mailto:${org.website_url}`,
      text: org.email
    },
    {
      prefix: 'Website: ',
      url: org.website_url,
      text: org.website_url
    }
  ]
  const contactElement =
    popupItems(contactItems, $router, { canInteract })
  parentElement.appendChild(contactElement)
  parentElement.appendChild(createRegistrationsElement(registrations))
  return parentElement
}

function createPagingElement (pageHandler) {
  const parentElement = document.createElement('div')

  const onPageChanged = (data) => {
    parentElement.innerHTML = '' // clear children
    if (!pageHandler.isFirstPage()) {
      const prevButton = createButton('Prev.', pageHandler.prev, 'mr-1')
      parentElement.appendChild(prevButton)
    }
    parentElement.appendChild(document.createTextNode(`showing ${pageHandler.itemStartIndex + 1} ${pageHandler.pageSize > 1 ? 'to ' + (pageHandler.itemEndIndex + 1) : ''} of ${pageHandler.items.length}`))
    if (!pageHandler.isLastPage()) {
      const nextButton = createButton('Next', pageHandler.next, 'ml-1')
      parentElement.appendChild(nextButton)
    }
  }
  pageHandler.listen(onPageChanged)

  return parentElement
}

function createButton (name = '', clickFunction = () => { }, classes = '') {
  const btnElement = document.createElement('button')
  btnElement.appendChild(document.createTextNode(name))
  btnElement.setAttribute('class', `btn btn-sm ${classes}`)
  btnElement.onclick = clickFunction
  return btnElement
}

function createRegistrationsElement (registrations) {
  const parentElement = document.createElement('div')
  registrations.forEach(reg => {
    const activity = reg.activity === 'DRILL' ? 'Well driller' : 'Pump installer'
    const subActivities = reg.applications.map(application =>
      application.subactivity.description
    ).join(',')
    if (subActivities) {
      // if there are subactivities, show them
      parentElement.appendChild(document.createTextNode(`Activity: ${subActivities}`))
    } else {
      // if there are no subactivities, just show the primary activity
      parentElement.appendChild(document.createTextNode(`Activity: ${activity}`))
    }
  })
  return parentElement
}

// Creates a <div> for the registry's popup content
export function createRegistryRegionPopupElement (features, map, $router, options = {}) {
  const canInteract = Boolean(options.canInteract)
  const registryLayerIds = options.registryLayerIds || [ REGISTRY_FILL_LAYER_ID ]

  const container = document.createElement('div')
  container.className = 'mapbox-popup-registry'
  const ul = document.createElement('ul')
  ul.className = `m-0 p-0 text-center mapbox-${canInteract ? 'popup' : 'tooltip'}`
  ul.style.listStyle = 'none'
  container.appendChild(ul)

  // Filter the features to only the registry layers we care about
  const onlyRegistryFeatures = features.filter((feature) => registryLayerIds.indexOf(feature.layer.id) !== -1)

  uniqBy(onlyRegistryFeatures, 'id').map((feature) => {
    const {
      name
    } = feature.properties

    const item = {
      text: `Registry Region: ${name}`
    }

    const li = popupItem(item, $router, { canInteract })

    if (canInteract) {
      // highlight this registry reion on mouseover of the name in the popup
      li.onmouseenter = () => {
        toggleRegistryHover(map, name, true)
      }
      li.onmouseleave = () => {
        toggleRegistryHover(map, name, false)
      }
    }

    ul.appendChild(li)
  })

  return container
}
