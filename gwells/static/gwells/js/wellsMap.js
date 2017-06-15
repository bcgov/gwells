/** First go at a wellsMap module, which provides core map functionality to the GWELLS application. Depends on Leaflet. */
var wellsMap = (function() {
    /** Consts and objects. */

    // Options for creating a wellsMap
    var wellsMapOptions = {
        initLatLong: [48.4284, -123.3656],
        initZoom: 13,
        esriLayers: [
            {
                url: 'http://maps.gov.bc.ca/arcgis/rest/services/province/web_mercator_cache/MapServer/'
            },
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

    /** Private methods */

    // Loads ESRI layers. Assumes MapServer. 
    // TODO: Generalise to other ESRI layer types? Add 'type' switcher in wellsMapOptions.esriLayers objs?
    // TODO: Investigate ESRI leaflet layer controls
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

    // TODO: FILL OUT OPTIONS?
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

    // TODO: More creation options?
    var createMap = function (mapNodeId) {
        var initLatLong = wellsMapOptions.initLatLong || [48.4284, -123.3656];
        var initZoom = wellsMapOptions.initZoom || 13;
        var map = L.map(mapNodeId).setView(initLatLong, initZoom);
        _loadEsriLayers(map);
        _loadWmsLayers(map);
        return map;
    }
    return {
        createMap: createMap
    };
})();