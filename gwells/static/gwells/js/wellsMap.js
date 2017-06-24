/**
 * The WellsMap class provides a Leaflet map with different functionality, depending upon the context in which it is deployed.
 * It currently depends only on Leaflet, eschewing any plugins or other libraries in the interest of maintainability. 
 * 
 */
function WellsMap () {
    /** Constants. */

    // Options for creating a wellsMap
    var wellsMapOptions = {
        // Initial centre of the map
        //initLatLong: [48.4284, -123.3656], VICTORIA COORDINATES
        // Minimum zoom level of the map (i.e., how far it can be zoomed out)
        minZoom: 4,
        // Maximum zoom of the map (i.e., how far it can be zoomed in)
        maxZoom: 17,
        // Bounding lats and longs of the map, corresponding to the lat/long extremes of BC. TODO: Refine?
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

    // The callback function for _newWellMarker's move event.
    var _newWellMarkerMoveCallback = null;

    // The map's maximum bounds. This should be a Leaflet LatLngBounds object.
    var _maxBounds = null;

    // Markers used to denote wells that have been searched for.
    var _searchMarkers = [];

    // Whether the map is undergoing an identifyWells operation.
    var _isIdentifyingWells = false;

    // The callback function for the beginning of an identifyWells operation.
    var _identifyWellsStartCallback = null;

    // the callback function for the end of an identifyWells operation.
    var _identifyWellsEndCallback = null;

    // The rectangle to draw on the map during an identifyWells operation.
    var _identifyWellsRectangle = null;

    // The starting corner of the identifyWellsRectangle
    var _startCorner = null;

    // The ending corner of the (final) identifyWellsRectangle 
    var _endCorner = null;

    /** Private functions */

    // Convenience method for checking whether a property exists (i.e., is neither null nor undefined)
    var _exists = function (prop) {
        return prop !== null && prop !== void 0;
    }

    // Convenience method for checking whether an object is an array.
    var _isArray = function (arr) {
        return _exists(arr.constructor) && arr.constructor === Array;
    }

    var _setMaxBounds = function () {
        var maxBounds = void 0;
        var bounds = wellsMapOptions.mapBounds || void 0; // If no bounds provided in options, don't fit to a bounding box.
        if (_exists(bounds.top) && _exists(bounds.bottom) && _exists(bounds.left) && _exists(bounds.right)) {
            maxBounds = L.latLngBounds([L.latLng(bounds.top, bounds.left), L.latLng(bounds.bottom, bounds.right)]);
            if (bounds.padding) {
                maxBounds.pad(bounds.padding);
            }
        }
        return maxBounds;
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

    // Handles the mousemove event during the identifyWells operation. Specifically, this function draws the interstitial
    // rectangles to help the user see the extent they're querying for wells.
    var _mouseMoveForIdentifyWellsEvent = function (e) {
        if (!_exists(_leafletMap) || !_exists(_startCorner)) {
            return;
        }
        var tempCorner = e.latlng;
        if (_exists(_identifyWellsRectangle)) {
            _leafletMap.removeLayer(_identifyWellsRectangle);
        }
        _identifyWellsRectangle = L.rectangle([_startCorner, tempCorner]);
        _identifyWellsRectangle.addTo(_leafletMap);
    }

    // Handles the mousedown event during the identifyWells operation. Specifically, this function disables map dragging 
    // and sets the starting corner of the rectangle to be drawn, as well as subscribing the map to _mouseMoveForIdentifyWellsEvent.
    var _mouseDownForIdentifyWellsEvent = function (e) {
        _leafletMap.dragging.disable();
        _startCorner = e.latlng;
        _leafletMap.on('mousemove', _mouseMoveForIdentifyWellsEvent);
    }

    // Handles the mouseup event during the identifyWells operation. Specifically, this function re-enables dragging, sets
    // the ending corner of the rectangle, unsubscribes the map from the events, passes the corner info to the callback,
    // and resets the private members associated with the operation.
    var _mouseUpForIdentifyWellsEvent = function (e) {
        _leafletMap.dragging.enable();
        _endCorner = e.latlng;

        _leafletMap.off('mousedown', _mouseDownForIdentifyWellsEvent);
        _leafletMap.off('mouseup', _mouseUpForIdentifyWellsEvent);
        _leafletMap.off('mousemove', _mouseMoveForIdentifyWellsEvent);
        if (_exists(_identifyWellsRectangle)) {
            _leafletMap.removeLayer(_identifyWellsRectangle);
            _identifyWellsRectangle = null;
        }       
        _isIdentifyingWells = false;
        if(_exists(_identifyWellsEndCallback)) {
            _identifyWellsEndCallback(_startCorner, _endCorner);
        }
        _startCorner = null;
        _endCorner = null;
    }

    // Determines whether a given latitude is within the map's bounds.
    var _isLatInBounds = function (lat) {
        return wellsMapOptions.mapBounds.bottom <= lat && lat <= wellsMapOptions.mapBounds.top;
    }

    // Determines whether a given longitude is within the map's bounds.
    var _isLongInBounds = function (long) {
        return wellsMapOptions.mapBounds.left <= long && long <= wellsMapOptions.mapBounds.right;
    }

    // Makes sure the latitude and longitude fit within the map's bounding box. This is necessary since lat/long data may
    // only be correct up to a minus sign (especially longitude data in the Western hemisphere) due to users not knowing
    // to enter a minus sign (or potentially entering a minus sign erronneously).
    // If the lat and long are within the map's bounds, they are returned; if they can be corrected by flipping the sign,
    // the negated values are returned. Else { NaN, NaN } is returned along with a console error.
    // Takes a latLong parameter corresponding to { lat: number, long: number }
    var _ensureLatLongIsInBounds = function (latLong) {
        var lat = _exists(latLong.lat) ? latLong.lat : NaN;
        var long = _exists(latLong.long) ? latLong.long : NaN;
        if (!_isLatInBounds(lat)){
            lat = -lat;
            if (!_isLatInBounds(lat)) {
                lat = NaN;
            }
        }
        if (!_isLongInBounds(long)) {
            long = -long;
            if (!_isLongInBounds(long)) {
                long = NaN;
            }
        }

        if (isNaN(lat) || isNaN(long)) {
            console.log("Invalid latitude or longitude. (Lat,Long): ("+latLong.lat+","+latLong.long+")");
            return { lat: NaN, long: NaN };
        }

        return { lat: lat, long: long };
    }

    // Takes latitude and longitude and returns a Leaflet latLng object only if the lat/long are valid within the map's bounding box.
    var _getLatLngInBC = function (lat, long) {
        var processedLatLong = _ensureLatLongIsInBounds({lat: lat, long: long});
        if (!isNaN(processedLatLong.lat) && !isNaN(processedLatLong.long)) {
            return L.latLng([processedLatLong.lat, processedLatLong.long]);
        }
        return null;
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

    // Displays wells and zooms to the bounding box to see all displayed wells. Note
    // the wells must have valid latitude and longitude data.
    var drawAndZoom = function (wells) {
        if(!_exists(_leafletMap) || !_exists(wells) || !_isArray(wells)) {
            return;
        }
        wells.forEach(function (well){
            var rawLat = parseFloat(well.latitude);
            var rawLong = parseFloat(well.longitude);
            var latLong = _getLatLngInBC(rawLat, rawLong);
            if (_exists(latLong)) {
                var searchMarker = L.circleMarker(latLong);
                searchMarker.addTo(_leafletMap);
                _searchMarkers.push(searchMarker);
            }
        });

        var markerBounds = L.featureGroup(_searchMarkers).getBounds();
        console.log(markerBounds);

        _leafletMap.fitBounds(markerBounds,{
            maxZoom: wellsMapOptions.maxZoom
        });
    }

    // Starts the identifyWells operation. This operation comprises several events, generally initiated when a user clicks
    // an appropriate button on the Search page. The map's style is dynamically changed so that the mouse pointer turns to
    // crosshairs, and the map itself is prepared in this method to let a user draw a rectangle on it by clicking and dragging
    // over the map. Once the mouse is released, the starting and ending corners of the box are collected, added to the Search
    // form, and submitted for processing.
    var startIdentifyWells = function () {
        if (_isIdentifyingWells) {
            // If the map is in the midst of an Identify, don't start a new one.
            return;
        }
        _isIdentifyingWells = true;
        _startCorner = null;
        _endCorner = null;
        if (_exists(_identifyWellsStartCallback)) {
            _identifyWellsStartCallback();
        }
        _leafletMap.on('mousedown', _mouseDownForIdentifyWellsEvent);
        _leafletMap.on('mouseup', _mouseUpForIdentifyWellsEvent);
        // TODO: Subscribe to 'mouseout' & treat it like 'mouseup'?
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
        var maxZoom = wellsMapOptions.maxZoom || 17;

        var maxBounds = _setMaxBounds();
        _leafletMap = L.map(mapNodeId, {
            minZoom: minZoom,
            maxZoom: maxZoom,
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
        _identifyWellsStartCallback = options.identifyWellsStartCallback || null;
        _identifyWellsEndCallback = options.identifyWellsEndCallback || null;
    }

    // The public members and methods of a wellsMap.
    return {
        isOpen: isOpen,
        initMap: initMap,
        placeNewWellMarker: placeNewWellMarker,
        removeNewWellMarker: removeNewWellMarker,
        drawAndZoom: drawAndZoom,
        startIdentifyWells: startIdentifyWells
    };
};