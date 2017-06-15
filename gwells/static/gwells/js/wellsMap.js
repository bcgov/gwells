
var wMap = (function() {

    return {
        createMap: function(mapNodeId) {
            var myMap = L.map(mapNodeId).setView([48.4284, -123.3656], 13);
            L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(myMap);                    
        }
    }
})();