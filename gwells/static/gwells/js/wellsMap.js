/** First go at a wellsMap module, which provides core map functionality to the GWELLS application. Depends on Leaflet. */
function WellsMap () {
    /** Constants. */

    // Options for creating a wellsMap
    var wellsMapOptions = {
        initLatLong: [48.4284, -123.3656],
        initZoom: 13,
        esriLayers: [
            /*{
                url: 'http://maps.gov.bc.ca/arcgis/rest/services/province/web_mercator_cache/MapServer/'
            },*/
            {
                url: 'http://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer'
            }
        ],
        wmsLayers: [
            {
                rootUrl: 'https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW/ows?',
                format: 'image/png',
                layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
                styles: 'Water_Wells_All',
                transparent: true
            }
        ]
    };

    /** Private members */
    
    // The underlying Leaflet map.
    var _leafletMap = null;

    // A marker for a prospective well.
    var _newWellMarker = null;

    // The JQuery selector of a form input corresponding to latitude.
    var _latNodeSelector = null;

    // The JQuery of a form input corresponding to longitude.
    var _longNodeSelector = null;

    /** Private methods */

    // Convenience method for checking whether a property exists (i.e., is neither null nor undefined)
    var _exists = function (prop) {
        return prop !== null && prop !== void 0;
    }

    // TODO: Generalise to other ESRI layer types? Add 'type' switcher in wellsMapOptions.esriLayers objs?
    // Loads ESRI layers. Currently ssumes MapServer. 
    var _loadEsriLayers = function (map) {
        var esriLayers = wellsMapOptions.esriLayers;
        esriLayers.forEach(function (esriLayer){
            if (esriLayer && esriLayer.url) {
                L.esri.tiledMapLayer({
                url: esriLayer.url
                }).addTo(map);                               
            }
        });
    };

    // Loads WMS layers.
    var _loadWmsLayers = function (map) {
        var wmsLayers = wellsMapOptions.wmsLayers;
        wmsLayers.forEach(function (wmsLayer) {
            if (wmsLayer && wmsLayer.rootUrl) {
                L.tileLayer.wms(wmsLayer.rootUrl, {
                    format: wmsLayer.format || 'image/png',
                    layers: wmsLayer.layers || '',
                    styles: wmsLayer.styles || '',
                    transparent: wmsLayer.transparent || true
                }).addTo(map);
            }
        });
    };

    // The move event of the newWellMarker. This event updates
    // the latitude and longitude fields associated with the new well.
    var _newWellMarkerMoveEvent = function (moveEvent) {
        var newLatLng = moveEvent.latlng;
        if (_latNodeSelector !== null) {
            $(_latNodeSelector).val(newLatLng.lat);
        }
        if (_longNodeSelector !== null) {
            $(_longNodeSelector).val(newLatLng.lng);
        }
    }

    /** Public methods */

    // Places a newWellMarker on the map to help refine the placement of a new well.
    // The options argument has type {lat: number, long: number}
    var placeNewWellMarker = function (options) {
        if (!_exists(_leafletMap)) {
            return;
        }
        options = options || {};
        var lat = options.lat || _leafletMap.getCenter().lat;
        var long = options.long || _leafletMap.getCenter().lng;
        if (_exists(_newWellMarker)) {
            _newWellMarker.setLatLng([lat, long]);
        }
        else {
            _newWellMarker = L.marker([lat, long], {
                draggable: true
            }).addTo(_leafletMap);
            _newWellMarker.on('move', _newWellMarkerMoveEvent);
        }
    }

    // Removes the newWelMarker from the map.
    var removeNewWellMarker = function () {
        if (!_exists(_leafletMap)) {
            return;
        }
        if (_exists(_newWellMarker)) {
            _leafletMap.removeLayer(_newWellMarker);
            _newWellMarker = null;
        }
    }

    // Initialises the underlying Leaflet map. The mapNodeId is mandatory; other properties are optional.
    // The options argument has type {mapNodeId: string, latNodeSelector: string, longNodeSelector: string}
    var initMap = function (options) {
        options = options || {};
        var mapNodeId = options.mapNodeId;
        if (!_exists(mapNodeId)) {
            // If there's no mapNodeId, we shouldn't initialise the map.
            console.log("ERROR: Map initialisation called but no map node ID provided.")
            return;
        }
        if (_exists(_leafletMap)) {
            // If we already have a map associated with this instance, we remove it.
            _leafletMap.remove();
            _leafletMap = null;
        }
        // Basic initialisation.
        var initLatLong = wellsMapOptions.initLatLong || [48.4284, -123.3656];
        var initZoom = wellsMapOptions.initZoom || 13;
        _leafletMap = L.map(mapNodeId).setView(initLatLong, initZoom);
        _loadEsriLayers(_leafletMap);
        _loadWmsLayers(_leafletMap);

        // Set optional initial props.
        var latNodeSelector = options.latNodeSelector;
        var longNodeSelector = options.longNodeSelector;
        if (_exists(latNodeSelector) && typeof (latNodeSelector) === "string") {
            _latNodeSelector = latNodeSelector;
        }
        if (_exists(longNodeSelector) && typeof (longNodeSelector) === "string") {
            _longNodeSelector = longNodeSelector;
        }
    }

    // The public members and methods of a wellsMap.
    return {
        initMap: initMap,
        placeNewWellMarker: placeNewWellMarker,
        removeNewWellMarker: removeNewWellMarker,
    };
};