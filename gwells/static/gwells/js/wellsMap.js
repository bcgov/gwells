/** First go at a wellsMap module, which provides core map functionality to the GWELLS application. Depends on Leaflet. */
function WellsMap () {
    /** Constants. */

    // Options for creating a wellsMap
    var wellsMapOptions = {
        // Initial centre of the map
        //initLatLong: [48.4284, -123.3656], VICTORIA COORDINATES
        // Minimum zoom level of the map (i.e., how far it can be zoomed out)
        minZoom: 4,
        // Bounding lats and longs of the map; corresponds to the lat/long extremes of BC. TODO: Refine?
        mapBounds: {
            top:  60.0223,
            bottom: 48.2045556,
            left: -139.0736706,
            right: -114.0338224,
            padding: 5 // Margin beyond extremes to pad the bounds with, as a percentage of the total bounding box.
        },
        // ESRI layers associated with the map
        esriLayers: [
            /*{ // This is an alternate basemap.
                url: 'http://maps.gov.bc.ca/arcgis/rest/services/province/web_mercator_cache/MapServer/'
            },*/
            {
                url: 'http://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer'
            }
        ],
        // WMS layers associated with the map
        wmsLayers: [
            {
                rootUrl: 'https://openmaps.gov.bc.ca/geo/pub/WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW/ows?',
                format: 'image/png',
                layers: 'pub:WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW',
                styles: 'PMBC_Parcel_Fabric_Cadastre_Outlined', // TODO: Verify style
                transparent: true
            }/*,
            {   // This is the DataBC Wells layer as viewed in iMap. Its data is updated daily, but not continuously, so it is likely not suitable for the GWELLS application.
                rootUrl: 'https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW/ows?',
                format: 'image/png',
                layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
                styles: 'Water_Wells_All',
                transparent: true
            } */
        ]
    };

    /** Private members */
    
    // The underlying Leaflet map.
    var _leafletMap = null;

    // A marker for a prospective well.
    var _newWellMarker = null;

    // The callback function for _newWellMarker's move event
    var _newWellMarkerMoveCallback = null;

    // The map's maximum bounds. This should be a Leaflet LatLngBounds object.
    var _maxBounds = null;

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
    
    // Passes the newWellMarker's updated lat/long coordinates to the provided callback function, if it exists.
    var _newWellMarkerMoveEvent = function (moveEvent) {
        if (_exists(_newWellMarkerMoveCallback)) {
            _newWellMarkerMoveCallback(moveEvent.latlng);
        }
    }

    /** Public methods */

    // Determines whether the map is 'open' (i.e., loaded and functional), using the nullity of _leafletMap as a proxy.
    var isOpen = function () {
        return _leafletMap !== null;
    };

    // Places a newWellMarker on the map to help refine the placement of a new well.
    // When placed by a button click, the map pans and zooms to centre on the marker.
    // The options argument has type {lat: number, long: number}
    var placeNewWellMarker = function (options) {
        // If the map does not exist or we do not have both latitude and longitude, bail out.
        if (!_exists(_leafletMap) || !_exists(options) || !_exists(options.lat) || !_exists(options.long)) {
            return;
        }

        var lat = options.lat;
        var long = options.long;
        var latLong = L.latLng([lat, long]);

        // If the latitude and longitude do not fit within the map's maxBounds, bail out.
        if (!_exists(_maxBounds) || !_maxBounds.contains(latLong)) {
            return;
        }
        // Zoom default.
        var zoomLevel = 17;
        if (_exists(_newWellMarker)) {
            _newWellMarker.setLatLng(latLong);
        }
        else {
            _newWellMarker = L.marker(latLong, {
                draggable: true
            }).addTo(_leafletMap);
            _newWellMarker.on('move', _newWellMarkerMoveEvent);
        }
        _leafletMap.flyTo(latLong, zoomLevel);
    }

    // Removes the newWellMarker from the map.
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
    // The options argument has type {mapNodeId: string, newWellMarkerMoveCallback: function}
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
        var initLatLong = wellsMapOptions.initLatLong || [53.7267, -127.6476]; // Fallback default to geographic centre of BC.
        var minZoom = wellsMapOptions.minZoom || 4;  // Fallback default to whole-province view in small map box.
        var bounds = wellsMapOptions.mapBounds || void 0; // If no bounds provided in options, don't fit to a bounding box.
        // TODO: Break maxBounds generation into its own private method.
        var maxBounds = void 0;
        if (_exists(bounds.top) && _exists(bounds.bottom) && _exists(bounds.left) && _exists(bounds.right)) {
            maxBounds = L.latLngBounds([L.latLng(bounds.top, bounds.left), L.latLng(bounds.bottom, bounds.right)]);
            if (bounds.padding) {
                maxBounds.pad(bounds.padding);
            }
        }
        _leafletMap = L.map(mapNodeId, {
            minZoom: minZoom,
            maxBounds: maxBounds,
            maxBoundsViscosity: 1.0
        });
        if (_exists(maxBounds)) {
            _leafletMap.fitBounds(maxBounds);
            _maxBounds = maxBounds;
        }
        _loadEsriLayers(_leafletMap);
        _loadWmsLayers(_leafletMap);

        // Optional properties.
        _newWellMarkerMoveCallback = options.newWellMarkerMoveCallback || null;
    }

    // The public members and methods of a wellsMap.
    return {
        isOpen: isOpen,
        initMap: initMap,
        placeNewWellMarker: placeNewWellMarker,
        removeNewWellMarker: removeNewWellMarker
    };
};