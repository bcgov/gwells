/**
 * The WellsMap class provides a Leaflet map with different functionality, depending upon the context in which it is deployed.
 * It currently depends only on Leaflet, esri-leaflet, and JQuery, eschewing any other plugins libraries in the interest of maintainability.
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
 *   initCentre?: [float], // A two-element array representing the latitude and longitude of the centre of the map. If omitted, the map is fit to mapBounds, so one of these must exist.
 *   canZoom?: bool, // Whether the map can be zoomed. Defaults to true.
 *   canPan?: bool, // Whether the map can be panned after initial load. Defaults to true.
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
 *   wellPushpinInit?: { // An object for setting the latitude, longitude, and details of a wellPushpin on init.
 *      lat: float, // The initial latitude of the pushpin
 *      long: float, // The initial longitude of the pushpin
 *      wellDetails: {
 *          guid: string // The GUID of the well, for identification and special handling
 *      }
 *   },
 *   wellPushpinMoveCallback?: function, // Function to call when the map's wellPushpin moves 
 *   identifyWellsStartCallback?: function, // Function to call when an identifyWells operation is started
 *   identifyWellsEndCallback?: function // Function to call when an identifyWells operation ends
 * }
 */
function WellsMap (options) {
    'use strict';
    /** Private members */

    // The URL used to search for wells.
    var _searchUrl = '/ajax/map_well_search/';

    // The underlying Leaflet map.
    var _leafletMap = null;

    // The map's maximum bounds. This should be a Leaflet LatLngBounds object.
    var _maxBounds = null;

    // The map's maximum zoom level.
    var _maxZoom = null;

    // An object containing a pushpin marker and a data schematic for a particular well. This indicates a single well on the screen that may be editable.
    // The object conforms to:
    // {
    //     pushpinMarker: L.marker, // The Leaflet marker that points to the well's location
    //     wellDetails: {
    //         guid: string, // The well's globally-unique ID, to avoid drawing with other (non-interactive) wells
    //     }
    // }
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
    };

    // Convenience method for checking whether an object is an array.
    var _isArray = function (arr) {
        return _exists(arr.constructor) && arr.constructor === Array;
    };

    var _setMaxBounds = function (bounds) {
        var maxBounds = null;
        if (_exists(bounds) && _exists(bounds.north) && _exists(bounds.south) && _exists(bounds.west) && _exists(bounds.east)) {
            maxBounds = L.latLngBounds([L.latLng(bounds.north, bounds.west), L.latLng(bounds.south, bounds.east)]);
            if (bounds.padding) {
                maxBounds.pad(bounds.padding);
            }
        }
        return maxBounds;
    };

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
    };

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
    };

    // Handles the mousedown event during the identifyWells operation. Specifically, this function disables map dragging 
    // and sets the starting corner of the rectangle to be drawn, as well as subscribing the map to _mouseMoveForIdentifyWellsEvent.
    var _mouseDownForIdentifyWellsEvent = function (e) {
        _leafletMap.dragging.disable();
        _startCorner = e.latlng;
        _leafletMap.on('mousemove', _mouseMoveForIdentifyWellsEvent);
    };

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
    };

    // Determines whether a given latitude is within the map's bounds.
    var _isLatInBounds = function (lat) {
        if (_exists(_maxBounds)) {
            return _maxBounds.getSouth() <= lat && lat <= _maxBounds.getNorth();
        }
        // If _maxBounds doesn't exist, the latitude is valid.
        return true;
    };

    // Determines whether a given longitude is within the map's bounds.
    var _isLongInBounds = function (long) {
        if (_exists(_maxBounds)) {
            return _maxBounds.getWest() <= long && long <= _maxBounds.getEast();
        }
        // If _maxBounds doesn't exist, the longitude is valid.
        return true;
    };

    // Makes sure the latitude and longitude fit within the map's bounding box, if one exists. This is necessary since lat/long data may
    // only be correct up to a minus sign (especially longitude data in the Western hemisphere) due to users not knowing
    // to enter a minus sign (or potentially entering a minus sign erronneously).
    // If the lat and long are within the map's bounds, they are returned; if they can be corrected by flipping the sign,
    // the negated values are returned. Else { NaN, NaN } is returned along with a console error.
    // Takes a latLong parameter corresponding to { lat: number, long: number }
    var _ensureLatLongIsInBounds = function (latLong) {
        var lat = _exists(latLong.lat) ? latLong.lat : NaN;
        var long = _exists(latLong.long) ? latLong.long : NaN;
        if (long > 0) {
            // Even if there's not a bounding box, we'll flip positive longitudes.
            long = -long;
        }
        if (!_isLatInBounds(lat)){
            lat = NaN;
        }
        if (!_isLongInBounds(long)) {
            long = NaN;
        }
        if (isNaN(lat) || isNaN(long)) {
            console.log("Invalid latitude or longitude. (Lat,Long): ("+latLong.lat+","+latLong.long+")");
            return {lat: NaN, long: NaN};
        }
        return {lat: lat, long: long};
    };

    // Takes latitude and longitude and returns a Leaflet latLng object only if the lat/long are valid within the map's bounding box.
    var _getLatLngInBC = function (rawLat, rawLong) {
        var lat = parseFloat(rawLat);
        var long = parseFloat(rawLong);
        if (_exists(lat) && !isNaN(lat) && _exists(long) && !isNaN(long)) {
            var processedLatLong = _ensureLatLongIsInBounds({lat: lat, long: long});
            if (!isNaN(processedLatLong.lat) && !isNaN(processedLatLong.long)) {
                return L.latLng([processedLatLong.lat, processedLatLong.long]);
            }
        }
        return null;
    };

    // Submits an XHR to return all wells within the given latLngBounds.
    var _searchByAjax = function (url, latLngBounds, success) {
        var northWestLatLng = latLngBounds.getNorthWest();
        var southEastLatLng = latLngBounds.getSouthEast();
        var startLatLong = northWestLatLng.lat + "," + northWestLatLng.lng;
        var endLatLong = southEastLatLng.lat + "," + southEastLatLng.lng;
        $.ajax({
            url: url,
            data: {
                'start_lat_long': startLatLong,
                'end_lat_long': endLatLong
            },
            dataType: 'json',
            success: success,
            error: function (xhr, status, error) {
                var msg = "An error occurred while searching for wells. STATUS: " + status + ".  ERROR " + error + ".";
                console.log(msg);
            }
        });
    };

    // A wellMarker should only be added if it is not the same as the pushpinWell, which is handled differently.
    var _canDrawWell = function (pushpinWellGuid, wellToDrawGuid) {
        if (!(_exists(pushpinWellGuid) && _exists(wellToDrawGuid))) {
            return true;
        } else {
            return pushpinWellGuid !== wellToDrawGuid;
        }
    };

    // Draws wells that can be drawn. Currently a well cannot be drawn if it is associated with the wellPushpin.
    var _drawWells = function (wells) {
        var style = _wellMarkerStyle || void 0;
        var wellPushpinGuid = null;
        if (_exists(_wellPushpin) && _exists(_wellPushpin.wellDetails) && _exists(_wellPushpin.wellDetails.guid)) {
            wellPushpinGuid = _wellPushpin.wellDetails.guid;
        }
        wells.forEach(function (well){
            var latLong = _getLatLngInBC(well.latitude, well.longitude);
            var wellGuid = well.guid;            
            if (_exists(latLong) && _canDrawWell(wellPushpinGuid, wellGuid)) {
                var wellMarker = L.circleMarker(latLong, style);
                wellMarker.addTo(_leafletMap);
                _wellMarkers.push(wellMarker);
            }
        });
    };

    // Handles the results of an AJAX call to 'ajax/map_well_search/'. Currently the expected behaviour is to draw the wells
    // that can be drawn.
    var _searchByAjaxSuccessCallback = function (results) {
        var wells = JSON.parse(results);
        if (_isArray(wells)) {
            _drawWells(wells);
        } else {
            console.log("Could not parse wells data.");
        }
    };

    /** Public methods */

    // 
    // 
    // The options argument has type {lat: number, long: number}
    /**
     * Places a wellPushpin on the map to help refine the placement of a well.
     * When placed by a button click, the map pans and zooms to centre on the marker.
     * @param latLng A Leaflet latLng where the wellPushpin will be placed
     */    
    var placeWellPushpin = function (latLng, wellDetails) {
        // If the map or the latLng do not exist, bail out.
        if (!_exists(_leafletMap) || !_exists(latLng)) {
            return;
        }
        // We ensure the lat/long is in BC, in case it was passed in without checking.
        var latLong = _getLatLngInBC(latLng.lat, latLng.lng);
        // If the latitude and longitude do not fit within the map's maxBounds, bail out.
        if (!_exists(latLong)) {
            return;
        }
        // The map zooms to the its maxZoom to display the pushpin.
        var zoomLevel = _leafletMap.getMaxZoom();
        if (_exists(_wellPushpin)) {
            _wellPushpin.pushpinMarker.setLatLng(latLong);            
        } else {
            _wellPushpin = {};
            _wellPushpin.pushpinMarker = L.marker(latLong, {
                draggable: _exists(_wellPushpinMoveCallback) // The pin should only drag if the map's calling page has a hook to handle movement
            }).addTo(_leafletMap);
            _wellPushpin.pushpinMarker.on('move', _wellPushpinMoveEvent);
        }
        if (_exists(wellDetails) && _exists(wellDetails.guid)) {
            _wellPushpin.wellDetails = wellDetails;
        }
        _leafletMap.flyTo(latLong, zoomLevel);
    };

    // Removes the wellPushpin from the map.
    var removeWellPushpin = function () {
        if (!_exists(_leafletMap)) {
            return;
        }
        if (_exists(_wellPushpin)) {
            _leafletMap.removeLayer(_wellPushpin);
            _wellPushpin = null;
        }
    };

    // Displays wells and zooms to the bounding box to see all displayed wells. Note
    // the wells must have valid latitude and longitude data.
    var drawAndZoom = function (wells) {
        if (!_exists(_leafletMap) || !_exists(wells) || !_isArray(wells)) {
            return;
        }
        _drawWells(wells);
        var markerBounds = L.featureGroup(_wellMarkers).getBounds();
        _leafletMap.fitBounds(markerBounds,{
            maxZoom: _maxZoom || _leafletMap.getMaxZoom()
        });
    };

    // Starts the identifyWells operation. This operation comprises several events, generally initiated when a user clicks
    // an appropriate button on the Search page. The map's style is dynamically changed so that the mouse pointer turns to
    // crosshairs, and the map itself is prepared in this method to let a user draw a rectangle on it by clicking and dragging
    // over the map. Once the mouse is released, the starting and ending corners of the box are collected, added to the Search
    // form, and submitted for processing.
    var startIdentifyWells = function () {
        if (_exists(_leafletMap) && _isIdentifyingWells) {
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
    };

    // Searches for all wells in the map's current bounding box.
    var searchWellsInBoundingBox = function () {
        if (_exists(_leafletMap)) {
            var mapBounds = _leafletMap.getBounds();
            _searchByAjax(_searchUrl, mapBounds, _searchByAjaxSuccessCallback);
        }
    };

    /** IIFE for construction of a WellsMap */
    (function (options) {
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

        // Zoom and centre settings
        var minZoom = options.minZoom || 4;
        var maxZoom = options.maxZoom || 17;
        var initCentre = options.initCentre || null;

        // Bools need a stricter check because of JS lazy evaluation
        var canZoom = _exists(options.canZoom) ? options.canZoom : true;
        var canPan = _exists(options.canPan) ? options.canPan : true;
        _maxBounds = _setMaxBounds(options.mapBounds) || void 0;
        _leafletMap = L.map(mapNodeId, {
            minZoom: minZoom,
            maxZoom: maxZoom,
            maxBounds: _maxBounds,
            maxBoundsViscosity: 1.0,
            zoomControl: canZoom,
            scrollWheelZoom: canZoom
        });
        if (_exists(initCentre) && _isArray(initCentre) && initCentre.length === 2) {
            var rawLat = initCentre[0];
            var rawLong = initCentre[1];
            var centreLatLng = _getLatLngInBC(rawLat, rawLong);
            if (_exists(centreLatLng)) {
                _leafletMap.setView(centreLatLng, maxZoom);
            }
        } else if (_exists(_maxBounds)) {
            _leafletMap.fitBounds(_maxBounds);
        }

        if (!canPan) {
            _leafletMap.dragging.disable();
            _leafletMap.doubleClickZoom.disable();
        }

        if (_exists(options.esriLayers)) {
            _loadEsriLayers(options.esriLayers);
        }
        if (_exists(options.wmsLayers)) {
            _loadWmsLayers(options.wmsLayers);
        }

        // Callbacks and markers/pushpins
        _wellMarkerStyle = options.wellMarkerStyle || null;
        _wellPushpinMoveCallback = options.wellPushpinMoveCallback || null;    
        _identifyWellsStartCallback = options.identifyWellsStartCallback || null;
        _identifyWellsEndCallback = options.identifyWellsEndCallback || null;

        var wellPushpinInit = options.wellPushpinInit || null;
        if (_exists(wellPushpinInit) && _exists(wellPushpinInit.lat) && _exists(wellPushpinInit.long)) {
            var rawLat = wellPushpinInit.lat;
            var rawLong = wellPushpinInit.long;
            var pinPoint = _getLatLngInBC(rawLat, rawLong);
            var details = wellPushpinInit.wellDetails;
            placeWellPushpin(pinPoint, details);
        }
    }(options));

    // The public members and methods of a WellsMap.
    return {
        placeWellPushpin: placeWellPushpin,
        removeWellPushpin: removeWellPushpin,
        drawAndZoom: drawAndZoom,
        startIdentifyWells: startIdentifyWells,
        searchWellsInBoundingBox: searchWellsInBoundingBox
    };
}