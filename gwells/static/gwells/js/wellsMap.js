/** First go at a wellsMap module, which provides core map functionality to the GWELLS application. Depends on Leaflet. */
/** This module is essentially a static class, providing options to create a wellsMap instance and then manipulate it by passing it into static functions. */
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

    // The DOM node of a form input corresponding to latitude.
    var _latNode = null;

    // The DOM node of a form input corresponding to longitude.
    var _longNode = null;

    /** Private methods */

    // TODO: Generalise to other ESRI layer types? Add 'type' switcher in wellsMapOptions.esriLayers objs?
    // TODO: Investigate ESRI leaflet layer controls
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

    /** Public methods */

    var setLatNode = function (nodeOrId) {
        // Stub.
        if (typeof nodeOrId === "string") {
        }
    }
    var setLongNode = function (nodeOrId) {
        // Stub.
    }

    // Places a marker
    var placeNewWellMarker = function (lat, long) {
        if (_newWellMarker !== null && _leafletMap !== null) {
            _leafletMap.removeLayer(_newWellMarker);
            _newWellMarker = null;
        }
        _newWellMarker = L.marker([lat, long], {
            draggable: true
        }).addTo(_leafletMap);
    }

    // TODO: More creation options?
    // Initialises the underlying Leaflet map.
    var initMap = function (mapNodeId) {
        if (_leafletMap) {
            _leafletMap = null;
        }
        var initLatLong = wellsMapOptions.initLatLong || [48.4284, -123.3656];
        var initZoom = wellsMapOptions.initZoom || 13;
        _leafletMap = L.map(mapNodeId).setView(initLatLong, initZoom);
        _loadEsriLayers(_leafletMap);
        _loadWmsLayers(_leafletMap);
    }

    return {
        initMap: initMap,
        placeNewWellMarker: placeNewWellMarker
    };
};