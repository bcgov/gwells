/**
 * The WellsMap class provides a Leaflet map with different functionality, depending upon the context in which it is deployed.
 * It currently depends only on Leaflet, eschewing any plugins or other libraries in the interest of maintainability.
 * 
 * A NOTE ON FUNCTIONALITY: This class can be initialised in different ways, which exposes its functionality differently.
 * If sufficient hooks are supplied in map construction, the map can perform the following tasks:
 *  - Supply a single draggable marker which, when moved, advertises the marker's new lat/long coordinates
 *  - Allow the user to draw a rectangle which, when finished drawing, advertises the rectangle's opposing corners
 *      in lat/long terms
 * @param options An object conforming to the following scheme (using TS notation):
 * {
 *   mapNodeId: string, // The DOM ID of the div into which the Leaflet map will be placed
 *   esriLayers: [ // ESRI layers associated with the map
 *       {
 *          url: string // A URL to an Esri MapServer map service.
 *       }
 *   ],
 *   wmsLayers: [ // WMS layers associated with the map
 *       {
 *          rootUrl: string, // URL to the OWS service of the WMS layer; e.g., 'https://openmaps.gov.bc.ca/geo/pub/WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW/ows?'
 *          format: string, // Format of the tiles; e.g., 'image/png'
 *          layers: string, // Layers of the OWS service; e.g., 'pub:WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW'.
 *          styles: string, // Styles of the OWS service; e.g., 'PMBC_Parcel_Fabric_Cadastre_Outlined'
 *          transparent: boolean // Whether the tiles are transparent (other than the features drawn upon them)
 *      } 
 *   ],
 *   minZoom?: number,  // The minimum zoom level of the map (i.e., how far it can be zoomed out)
 *   maxZoom?: number,  // The maximum zoom level of the map (i.e., how far it can be zoomed in)
 *   mapBounds?: { // Latitude and longitude extremes of the bounding rectangle for the map.
 *      north: float, // The top latitude of the map
 *      south: float, // The bottom latitude of the map
 *      west: float, // The leftmost longitude of the map
 *      east: float, // The rightmost longitude of the map
 *      padding: int // Margin beyond extremes to pad the bounds with, as a percentage of the total bounding box.     
 *   },
 *   wellMarkerStyle?: { // Settings for a Leaflet circleMarker
 *      radius: int, // The radius of the circleMarker
 *      color: string, // The hex string for the colour of the circleMarker
 *      fillOpacity: float // How transparent the circleMarker's fill is
 *   },
 *   wellPushpinMoveCallback?: function, // Function to call when the map's wellPushpin moves 
 *   identifyWellsStartCallback?: function, // Function to call when an identifyWells operation is started
 *   identifyWellsEndCallback?: function // Function to call when an identifyWells operation ends
 * }
 */
function WellsMap (options) {
    /** Private members */
    
    // The underlying Leaflet map.
    var _leafletMap = null;

    // The map's maximum bounds. This should be a Leaflet LatLngBounds object.
    var _maxBounds = null;

    // The map's maximum zoom level.
    var _maxZoom = null;

    // A pushpin marker for a particular well. This indicates a single well on the screen that may be editable.
    var _wellPushpin = null;

    // The callback function for _wellPushpin's move event.
    var _wellPushpinMoveCallback = null;

    // Markers used to denote wells.
    var _wellMarkers = [];

    // Leaflet style for the _wellMarkers
    var _wellMarkerStyle = null;

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

    var _setMaxBounds = function (bounds) {
        var maxBounds = void 0;
        if (_exists(bounds) && _exists(bounds.north) && _exists(bounds.south) && _exists(bounds.west) && _exists(bounds.east)) {
            maxBounds = L.latLngBounds([L.latLng(bounds.north, bounds.west), L.latLng(bounds.south, bounds.east)]);
            if (bounds.padding) {
                maxBounds.pad(bounds.padding);
            }
        }
        return maxBounds;
    }

    // Loads ESRI MapServer services.
    var _loadEsriLayers = function (esriLayers) {
        if (_exists(_leafletMap)) {
            esriLayers.forEach(function (esriLayer){
                if (esriLayer && esriLayer.url) {
                    L.esri.tiledMapLayer({
                    url: esriLayer.url
                    }).addTo(_leafletMap);                               
                }
            });
        }
    };

    // Loads WMS layers.
    var _loadWmsLayers = function (wmsLayers) {
        if (_exists(_leafletMap)) {
            wmsLayers.forEach(function (wmsLayer) {
                if (wmsLayer && wmsLayer.rootUrl) {
                    L.tileLayer.wms(wmsLayer.rootUrl, {
                        format: wmsLayer.format || 'image/png',
                        layers: wmsLayer.layers || '',
                        styles: wmsLayer.styles || '',
                        transparent: wmsLayer.transparent || true
                    }).addTo(_leafletMap);
                }
            });
        }
    };
    
    // Passes the wellPushpin's updated lat/long coordinates to the provided callback function, if it exists.
    var _wellPushpinMoveEvent = function (moveEvent) {
        if (_exists(_wellPushpinMoveCallback)) {
            _wellPushpinMoveCallback(moveEvent.latlng);
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
        if (_exists(_maxBounds)) {
            return _maxBounds.getSouth() <= lat && lat <= _maxBounds.getNorth();
        }
        // If _maxBounds doesn't exist, the latitude is valid.
        return true;
    }

    // Determines whether a given longitude is within the map's bounds.
    var _isLongInBounds = function (long) {
        if (_exists(_maxBounds)) {
            return _maxBounds.getWest() <= long && long <= _maxBounds.getEast();
        }
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

    // 
    // 
    // The options argument has type {lat: number, long: number}
    /**
     * Places a wellPushpin on the map to help refine the placement of a well.
     * When placed by a button click, the map pans and zooms to centre on the marker.
     * @param options An object conforming to:
     * {
     *  lat: float,
     *  long: float
     * }
     */    
    var placeWellPushpin = function (options) {
        // If the map does not exist or we do not have both latitude and longitude, bail out.
        if (!_exists(_leafletMap) || !_exists(_maxBounds) || !_exists(options) || !_exists(options.lat) || !_exists(options.long)) {
            return;
        }

        var latLong = _getLatLngInBC(options.lat, options.long);

        // If the latitude and longitude do not fit within the map's maxBounds, bail out.
        if (!_exists(latLong)) {
            return;
        }
        // Zoom default.
        var zoomLevel = 17;
        if (_exists(_wellPushpin)) {
            _wellPushpin.setLatLng(latLong);
        }
        else {
            _wellPushpin = L.marker(latLong, {
                draggable: true
            }).addTo(_leafletMap);
            _wellPushpin.on('move', _wellPushpinMoveEvent);
        }
        _leafletMap.flyTo(latLong, zoomLevel);
    }

    // Removes the wellPushpin from the map.
    var removeWellPushpin = function () {
        if (!_exists(_leafletMap)) {
            return;
        }
        if (_exists(_wellPushpin)) {
            _leafletMap.removeLayer(_wellPushpin);
            _wellPushpin = null;
        }
    }

    // Displays wells and zooms to the bounding box to see all displayed wells. Note
    // the wells must have valid latitude and longitude data.
    var drawAndZoom = function (wells) {
        if(!_exists(_leafletMap) || !_exists(wells) || !_isArray(wells)) {
            return;
        }
        var style = _wellMarkerStyle || void 0;
        wells.forEach(function (well){
            var rawLat = parseFloat(well.latitude);
            var rawLong = parseFloat(well.longitude);
            var latLong = _getLatLngInBC(rawLat, rawLong);
            if (_exists(latLong)) {
                var wellMarker = L.circleMarker(latLong, style);
                wellMarker.addTo(_leafletMap);
                _wellMarkers.push(wellMarker);
            }
        });

        var markerBounds = L.featureGroup(_wellMarkers).getBounds();
        _leafletMap.fitBounds(markerBounds,{
            maxZoom: _maxZoom || _leafletMap.getMaxZoom()
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

    /** Construction */

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
    var minZoom = options.minZoom || 4;  // Fallback default to whole-province view in small map box.
    var maxZoom = options.maxZoom || 17;
    var maxBounds = _setMaxBounds(options.mapBounds);
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
    var esriLayers = options.esriLayers;
    var wmsLayers = options.wmsLayers;
    if (_exists(esriLayers)) {
        _loadEsriLayers(esriLayers);
    }
    if (_exists(wmsLayers)) {
        _loadWmsLayers(wmsLayers);
    }

    /** Optional properties */

    // Style properties
    _wellMarkerStyle = options.wellMarkerStyle || null;

    // Callbacks
    _wellPushpinMoveCallback = options.wellPushpinMoveCallback || null;    
    _identifyWellsStartCallback = options.identifyWellsStartCallback || null;
    _identifyWellsEndCallback = options.identifyWellsEndCallback || null;
        
    // The public members and methods of a WellsMap.
    return {
        placeWellPushpin: placeWellPushpin,
        removeWellPushpin: removeWellPushpin,
        drawAndZoom: drawAndZoom,
        startIdentifyWells: startIdentifyWells
    };
};