/**
 * The WellsMap class provides a Leaflet map with different functionality, depending upon the context in which it is deployed.
 * It currently depends only on Leaflet, esri-leaflet, and JQuery, eschewing any other plugins libraries in the interest of maintainability.
 *
 * A NOTE ON FUNCTIONALITY: This class can be initialised in different ways, which exposes its functionality differently.
 * If sufficient parameters are supplied in map construction, the map can perform the following tasks:
 *  - Draw a single pushpin (i.e., a Leaflet marker akin to a Google marker) which causes the map to emit AJAX requests to show all wells
 *      in the bounding box (except the well that is being represented by the pushpinm which the pin itself has coupled). The map will
 *      reissue queries for wells in the bounding box whenever the map is panned or zoomed, provided the pushpin is present.
 *      If the map is beneath a certain zoom level, it will draw a rectangle to show queried wells and refrain from querying further
 *      until zoomed beyond the minimum (in order to prevent querying and rendering an inordinate number of wells).
 *      The pushpin can be fed into the map's initialisation options via wellPushpinInit or added/moved
 *      programmatically through the public method placeWellPushpin(). It may be removed via removeWellPushpin().
 *      If the wellPushpinMoveCallback is supplied on map init, the pushpin can be moved by dragging, which advertises the
 *      pushpin's latitude and longitude to the callback. The map will centre on the pushpin and reissue queries for surrounding
 *      wells whenever the pushpin is moved.
 *  - Allow the map to search wells via the searchWellsByExtent() method. If the map init supplies a searchWellsByExtentCallback,
 *      the map advertises a pair of latitude/longitude coordinates corresponding to extreme corners of the rectangle's bounding box.
 *      If the corners of a rectangle are passed to the map via initialExtentRectangle, the map initialises fit to this rectangle.
 *  - Display an ESRI MapServer layer as a base layer.
 *  - Display an array of WMS tile layers as overlays.
 * The map is able to pan and zoom by default, but this behaviour can be disabled by passing appropriate booleans. Note that if zooming is allowed,
 * the map will always zoom into and out of the centre of the map, regardless if the zoom event arises from zoom buttons or the mouse wheel. Also,
 * the constructor allows the map to set its zoom levels, as well as the initial centre or a bounding box to fit (precisely one of these is required 
 * for a given instance).
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
 *   centreZoom?: bool, // Whether the map zoom always tracks the centre of the map. Defaults to false.
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
 *   wellPushpinInit?: { // An object for setting the latitude, longitude, and details of a wellPushpin on init.
 *      lat: float, // The initial latitude of the pushpin
 *      long: float, // The initial longitude of the pushpin
 *      wellDetails: {
 *          guid: string // The GUID of the well, for identification and special handling
 *      }
 *   },
 *   wellPushpinMoveCallback?: function, // Function to call when the map's wellPushpin moves
 *   // Indicates the map should be drawn with an 'identify' rectangle to start with. Overwritten by the identifyWellsOperation.
 *   initialExtentRectangle?: {
 *      startCorner: string, // Comma-separated string of theform 'lat,long' denoting the rectangle's starting corner
 *      endCorner: string // Comma-separated string of theform 'lat,long' denoting the rectangle's ending corner
 *   },
 *   externalQueryCallback?: function, // Function to call when the map's bounding box is bundled into an external query
 *   externalAttributionNodeId?: string // ID of the DOM node (exterior to the map) where the map's attribution will be displayed.
 * }
 */
function WellsMap(options) {
    'use strict';
    /** Class constants */

    // The URL used to search for wells.
    var _SEARCH_URL = '/ajax/map_well_search/';

    // The zoom level beyond which the map issues AJAX queries for wells, and beneath which removes AJAX-queried wells.
    var _SEARCH_MIN_ZOOM_LEVEL = 14;

    // Leaflet style for the _wellMarkers
    var _WELL_MARKER_STYLE = {
          radius: 3, // The radius of the circleMarker
          color: '#0147b7', // The color of the circleMarker
          fillOpacity: 1.0 // How transparent the circleMarker's fill is
    };

    var _WELL_PUSHPIN_WELL_MARKER_STYLE = {
        radius: 3,
        weight: 1,
        color: '#FF0000',
        fillColor: '#0147b7',
        fill: true,
        fillOpacity: 1.0
    };

    /** Private members dynamically set */

    // The underlying Leaflet map.
    var _leafletMap = null;

    // The map's maximum bounds. This should be a Leaflet LatLngBounds object.
    var _maxBounds = null;

    // An object containing a pushpin marker and a data schematic for a particular well. This indicates a single well on the screen that may be editable.
    // The object conforms to:
    /* {
     *     pushpinMarker: L.marker, // The Leaflet marker that points to the well's location
     *     wellDetails: {
     *         guid: string, // The well's globally-unique ID, to avoid drawing with other (non-interactive) wells
     *     },
     *     wellMarker: L.circleMarker // The Leaflet circleMarker that represents the well itself.
     * }
     * */
    var _wellPushpin = null;

    // The callback function for _wellPushpin's move event.
    var _wellPushpinMoveCallback = null;

    // Markers used to denote wells. This var should only be accessed directly, so do not write var newArr = _wellMarkers anywhere in the class.
    var _wellMarkers = [];

    // The rectangle to be drawn when the zoom level is below the search minimum, delimiting
    // the extent of the queried wells to be displayed.
    var _searchMinRectangle = null;

    // Callback for the external query
    var _externalQueryCallback = null;

    /** Private functions */

    // Convenience method for checking whether a property exists (i.e., is neither null nor undefined)
    var _exists = function (prop) {
        return prop !== null && prop !== void 0;
    };

    // Convenience method for checking whether an object is an array.
    var _isArray = function (arr) {
        return _exists(arr) && _exists(arr.constructor) && arr.constructor === Array;
    };

    var _setMaxBounds = function (bounds) {
        var maxBounds = null;
        if (_exists(bounds.north) && _exists(bounds.south) && _exists(bounds.west) && _exists(bounds.east)) {
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
        var latLng = moveEvent.latlng;
        if (_exists(_wellPushpinMoveCallback)) {
            _wellPushpinMoveCallback(latLng);
        }
        _wellPushpin.wellMarker.setLatLng(latLng);
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

    // Makes sure the latitude and longitude fit within the map's bounding box, if one exists.
    // If the lat and long are within the map's bounds, they are returned; if they can be corrected by flipping the sign,
    // the negated values are returned. Else { NaN, NaN } is returned along with a console error.
    // Takes a latLong parameter corresponding to { lat: number, long: number }
    var _ensureLatLongIsInBounds = function (latLong) {
        var lat = _exists(latLong.lat) ? latLong.lat : NaN;
        var long = _exists(latLong.long) ? latLong.long : NaN;
        if (!_isLatInBounds(lat)){
            lat = NaN;
        }
        if (!_isLongInBounds(long)) {
            long = NaN;
        }
        if (isNaN(lat) || isNaN(long)) {
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
            success: success
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

    // Clears the _wellMarkers from the map and resets the array.
    var _clearWells = function () {
        if (_exists(_leafletMap) && _isArray(_wellMarkers)) {
            _wellMarkers.forEach(function (wellMarker) {
                _leafletMap.removeLayer(wellMarker);
            });
        }
        // We can confidently overwrite the array because the class should never create any references to _wellMarkers.
        _wellMarkers = [];
    };

    // Parses the input to generate an internal URL to the well details summary page. If the input is not a number (or null),
    // an empty string is returned.
    var _generateWellTagUrl = function (tagNum) {
        var num = parseInt(tagNum);
        if (!_exists(num) || isNaN(num)) {
            return '';
        }
        return '<a href="/well/' + num + '">' + num + '</a>';
    };

    // Generates a popup content HTML string for a well marker, based on the data that well has available.
    var _generateWellMarkerPopupContents = function (well) {
        if (!_exists(well)) {
            return;
        }
        // contentObj is a dictionary whose keys correspond to the display names of
        // well data attributes and whose values correspond to the specific well's data.
        // This dictionary's values will in general consist of a (potentially processed)
        // subset of the JSON returned by the Python well search service.
        var contentObj = {
            'Well Tag Number': _generateWellTagUrl(well.well_tag_number), // We turn the well tag number into a local URL to the summary page.
            'Identification Plate Number': well.identification_plate_number || '',
            'Street Address': well.street_address || ''
        };

        // We build the contentString from the contentObj dictionary, using paragraphs as property delimiters.
        var contentString = '';
        $.each(contentObj, function (contentKey, contentVal) {
            contentString += '' + contentKey + ': ' + contentVal + '<br />';
        });
        return contentString;
    };

    // Draws wells that can be drawn. Currently a well cannot be drawn if it is associated with the wellPushpin.
    var _drawWells = function (wells) {
        // First we clear any extant markers
        _clearWells();

        // Markers should only be clickable when there is no wellPushpin available.
        var style = $.extend({}, _WELL_MARKER_STYLE, {interactive: !_wellPushpin});
        var wellPushpinGuid = null;
        // Now we draw the wells, checking to prevent a marker from being drawn where a pushpin will be.
        if (_exists(_wellPushpin) && _exists(_wellPushpin.wellDetails) && _exists(_wellPushpin.wellDetails.guid)) {
            wellPushpinGuid = _wellPushpin.wellDetails.guid;
        }
        wells.forEach(function (well) {
            var latLong = _getLatLngInBC(well.latitude, well.longitude);
            var wellGuid = well.guid;
            if (_exists(latLong) && _canDrawWell(wellPushpinGuid, wellGuid)) {
                var wellMarker = L.circleMarker(latLong, style);
                wellMarker.bindPopup(_generateWellMarkerPopupContents(well));
                wellMarker.addTo(_leafletMap);
                _wellMarkers.push(wellMarker);
            }
        });
    };

    // Handles the results of an AJAX call to 'ajax/map_well_search/'.
    var _searchByAjaxSuccessCallback = function (results) {
        var wells = JSON.parse(results);
        if (_isArray(wells)) {
            _drawWells(wells);
        }
    };

    // Searches for all wells in the map's current bounding box, provided the map is beyond the minimum searching zoom level.
    // We clear the extant wells before re-querying, for simplicity.
    var _searchWellsInBoundingBox = function () {
        if (_exists(_leafletMap) && _leafletMap.getZoom() >= _SEARCH_MIN_ZOOM_LEVEL) {
            _clearWells();
            var mapBounds = _leafletMap.getBounds();
            _searchByAjax(_SEARCH_URL, mapBounds, _searchByAjaxSuccessCallback);
        }
    };

    // When the map is zoomed and there is a wellPushpin, we only query for wells while the map
    // is within the searchMinRectangle. Thus we need to draw the rectangle when the map is zoomed
    // beyond the search minimum, or destroy it when the map is zoomed within.
    var _handleSearchMinRectangle = function () {
        if (_leafletMap.getZoom() === _SEARCH_MIN_ZOOM_LEVEL) {
            if (_exists(_searchMinRectangle)) {
                _leafletMap.removeLayer(_searchMinRectangle);
                _searchMinRectangle = null;
            }
            _searchMinRectangle = L.rectangle(_leafletMap.getBounds(), {
                fillOpacity: 0,
                interactive: false
            }).addTo(_leafletMap);            
        } else if (_leafletMap.getZoom() > _SEARCH_MIN_ZOOM_LEVEL && _exists(_searchMinRectangle)) {
            _leafletMap.removeLayer(_searchMinRectangle);
            _searchMinRectangle = null;
        }
    };

    // Issues a query to fetch wells in the bounding box, meant to subscribe to
    // the map's moveend event while a wellPushpin is present on the map.
    var _searchBoundingBoxOnMoveEnd = function () {
        _searchWellsInBoundingBox();
        _handleSearchMinRectangle();
    };

    // When the wellPushpin is moved, pan to re-centre the pushpin.
    var _wellPushpinMoveEndEvent = function () {
        _leafletMap.panTo(_wellPushpin.pushpinMarker.getLatLng());
    };

    // Remporarily remove the _wellPushpin's wellMarker during zoom to keep the marker from
    // potentially dominating the map view.
    var _wellPushpinZoomStartEvent = function () {
        _leafletMap.removeLayer(_wellPushpin.wellMarker);
    };

    // When the map is zoomed with a wellPushpin, pan to re-centre the pushpin (which
    // is needed if the map is near the bounding box), and clear the surrounding wells
    // if the zoom level is below the minimum search level.
    var _wellPushpinZoomEndEvent = function () {
        _leafletMap.panTo(_wellPushpin.pushpinMarker.getLatLng());
        _wellPushpin.wellMarker.addTo(_leafletMap);
    };

    /** Public methods */

    /**
     * Places a wellPushpin on the map to help refine the placement of a well.
     * When placed by a button click, the map pans and zooms to centre on the marker.
     * @param latLongArray An array of [lat, long], where lat and long specify where the wellPushpin will be placed
     * @param wellDetails An object conforming to the _wellPushpin's wellDetails property.
     */
    var placeWellPushpin = function (latLongArray, wellDetails) {
        // If the map or the latLng do not exist, bail out.
        if (!_exists(_leafletMap) || !_isArray(latLongArray)) {
            return;
        }
        // We ensure the lat/long is in BC, in case it was passed in without checking.
        var latLong = _getLatLngInBC(latLongArray[0], latLongArray[1]);
        // If the latitude and longitude do not fit within the map's maxBounds, bail out.
        if (!_exists(latLong)) {
            return;
        }
        // The map zooms to the its maxZoom to display the pushpin.
        var zoomLevel = _leafletMap.getMaxZoom();
        // If the pushpin exists and the movement is substantive, move the pin. Else if
        // the pushpin does not exist, create it and place it at the coordinates.
        if (_exists(_wellPushpin) && _exists(_wellPushpin.pushpinMarker) && !_wellPushpin.pushpinMarker.getLatLng().equals(latLong)) {
            _wellPushpin.pushpinMarker.setLatLng(latLong);
            _wellPushpin.wellMarker.setLatLng(latLong);
        } else {
            _wellPushpin = {};
            _wellPushpin.pushpinMarker = L.marker(latLong, {
                draggable: _exists(_wellPushpinMoveCallback) // The pin should only drag if the map's caller has a hook to handle movement
            }).addTo(_leafletMap);
            // Assign the wellMarker to the _wellPushpin
            _wellPushpin.wellMarker = L.circleMarker(latLong, _WELL_PUSHPIN_WELL_MARKER_STYLE).addTo(_leafletMap);

            // The pin should subscribe to move events.
            _wellPushpin.pushpinMarker.on('move', _wellPushpinMoveEvent);
            _wellPushpin.pushpinMarker.on('moveend', _wellPushpinMoveEndEvent);
        }
        // Assign wellDetails to the _wellPushpin.
        _wellPushpin.wellDetails = wellDetails;

        // If the pin exists, the map should refresh the wells it displays when it is moved, to provide
        // more information to aid in well placement without having to load too many wells at once.
        _leafletMap.on('moveend', _searchBoundingBoxOnMoveEnd);

        // If the pin exists, zoomstart should remove the pin's wellMarker, since it's a part of the map itself
        // and so zooming can cause it to dominate the map view temporarily.
        _leafletMap.on('zoomstart', _wellPushpinZoomStartEvent);
        
        // If the pin exists, zoomend should re-centre the pin and replace the pin's wellMarker.
        _leafletMap.on('zoomend', _wellPushpinZoomEndEvent);

        // Finally, the map should fly to the pin.
        _leafletMap.flyTo(latLong, zoomLevel);
    };

    // Removes the wellPushpin from the map and clears it of any extant wells.
    var removeWellPushpin = function () {
        if (!_exists(_leafletMap)) {
            return;
        }
        if (_exists(_wellPushpin) && _exists(_wellPushpin.pushpinMarker)) {
            // Unsubscribe from the pushpin-related events.
            _leafletMap.off('moveend', _searchBoundingBoxOnMoveEnd);
            _leafletMap.off('zoomend', _wellPushpinZoomEndEvent);
            _leafletMap.removeLayer(_wellPushpin.pushpinMarker);
            _leafletMap.removeLayer(_wellPushpin.wellMarker);
            _wellPushpin.pushpinMarker = null;
            _wellPushpin.wellMarker = null;
            _wellPushpin = null;
            _clearWells();
        }
    };

    // Displays wells and zooms to the to see all displayed wells.
    // Note the wells must have valid latitude and longitude data.
    var drawAndFitBounds = function (wells) {
        if (!_exists(_leafletMap) || !_exists(wells) || !_isArray(wells)) {
            return;
        }
        _drawWells(wells);

        // Once wells are drawn, we draw a (static) rectangle that encompasses them, with a bit of
        // a padded buffer to include wells on the edges of the rectangle.
        var buffer = 0.00005;
        var padding = 0.01;
        
        // With the above constants, we get the bounds of the _wellMarkers and pad them with the buffer and padding.
        var markerBounds = L.featureGroup(_wellMarkers).getBounds();
        var northWestCorner = L.latLng(markerBounds.getNorthWest().lat + buffer, markerBounds.getNorthWest().lng - buffer);
        var southEastCorner = L.latLng(markerBounds.getSouthEast().lat - buffer, markerBounds.getSouthEast().lng + buffer);
        markerBounds = L.latLngBounds([northWestCorner, southEastCorner]).pad(padding);

        // Now that we have the right bounds, fit the map to them.
        _leafletMap.fitBounds(markerBounds);
    };

    var searchWellsByExtent = function () {
        if (_exists(_externalQueryCallback))
        var boundingBox = _leafletMap.getBounds();
        var northWestCorner = boundingBox.getNorthWest();
        var southEastCorner = boundingBox.getSouthEast();
        
    };

    /** IIFE for construction of a WellsMap */
    (function (options) {
        options = options || {};
        var mapNodeId = options.mapNodeId;
        if (!_exists(mapNodeId)) {
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
        var centreZoom = _exists(options.centreZoom) ? options.centreZoom : false;
        var canPan = _exists(options.canPan) ? options.canPan : true;
        _maxBounds = _exists(options.mapBounds) ? _setMaxBounds(options.mapBounds) : void 0;
        _leafletMap = L.map(mapNodeId, {
            minZoom: minZoom,
            maxZoom: maxZoom,
            maxBounds: _maxBounds,
            maxBoundsViscosity: 1.0,
            scrollWheelZoom: centreZoom ? 'center' : true, // We want the map to stay centred on scrollwheel zoom if zoom is enabled.
            keyboardPanDelta: canPan ? 80 : 0
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

        // Callbacks
        _wellPushpinMoveCallback = options.wellPushpinMoveCallback || null;
        _externalQueryCallback = options.externalQueryCallback || null;

        // Initial graphics
        var wellPushpinInit = options.wellPushpinInit || null;
        if (_exists(wellPushpinInit) && _exists(wellPushpinInit.lat) && _exists(wellPushpinInit.long)) {
            var details = wellPushpinInit.wellDetails;
            placeWellPushpin([wellPushpinInit.lat, wellPushpinInit.long], details);
        }

        // If given an external DOM node to display the map's attribution, hook it up here.
        if (_exists(options.externalAttributionNodeId)) {
           $("#" + options.externalAttributionNodeId).append(_leafletMap.attributionControl.getContainer());
        }
    }(options));

    // The public members and methods of a WellsMap.
    return {
        placeWellPushpin: placeWellPushpin,
        removeWellPushpin: removeWellPushpin,
        drawAndFitBounds: drawAndFitBounds,
        // TODO: Remove this when custom control is within the map
        searchWellsByExtent: searchWellsByExtent
    };
}