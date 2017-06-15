/** First go at a wellsMap module, which provides core map functionality to the GWELLS application. Depends on Leaflet. */
var wMap = (function() {
    // TODO: Incorporate esri-leaflet, get layer list loading.
    var createMap = function(mapNodeId) {
        var myMap = L.map(mapNodeId).setView([48.4284, -123.3656], 13);
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(myMap);                    
    }
    return {
        createMap: createMap
    };
})();