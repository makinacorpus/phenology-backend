

var phenoclim = phenoclim || {};
var geojsonMarkerOptions = {
    radius: 8,
    fillColor: "#ff7800",
    color: "#000",
    weight: 1,
    opacity: 1,
    clickable: false,
    fillOpacity: 0.3
};
var phenoMarker = L.AwesomeMarkers.icon({
  icon: 'tree-deciduous',
  markerColor: 'green'
});

phenoclim.map = function(options){
	self = this;
	
	function onEachFeature(feature, layer) {
	    // does this feature have a property named popupContent?
	    if (feature.properties && feature.properties.draggable === true) {
	        layer.options.draggable = true;
    		layer.on("dragend", function(e){
    			var latlng = e.target.getLatLng();
    			$("[name=lat]").val(latlng.lat);
    			$("[name=lon]").val(latlng.lng);
    		});
	    }
	}

	// initialize the map on the "map" div with a given center and zoom
    this._map = L.map('map', {
        center: [51.505, -0.09],
        zoom: 11,
        maxZoom: 19
    });
    this.geojson = undefined;
    // add an OpenStreetMap tile layer
	L.tileLayer('http://{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png', {
	    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(this._map);
    
    L.control.scale({ imperial : false }).addTo(self._map);
    console.log("sfds")
    var bounds2 = [[46.38, -1.51],[42.71, 7.95]];
    if(options.geojson && options.geojson.features && options.geojson.features.length > 0){
      self.geojson = L.geoJson(options.geojson,{
          pointToLayer: function (feature, latlng) {
            var ftype = feature.properties.object
            console.log(feature.properties)
            if(ftype)
            {
              if(ftype == "individual"){
                  return L.marker(latlng, {icon: phenoMarker});
              }
              else{
                  return L.circle(latlng, 500, geojsonMarkerOptions);
              }
            }
          },
          onEachFeature: onEachFeature
      }
      ).addTo(self._map);
      var bounds = self.geojson.getBounds();
      self._map.fitBounds(bounds, { maxZoom: 18, padding: [10, 10] });
    }
    else{
      self._map.fitBounds(bounds2);
    }

     $(".change_position").on("click",function(event){
     	var rel = $(this).attr("data-rel");
     	var id = $(this).attr("data-id");
     	var layers = self.geojson.getLayers();
        for (var i = 0; i < layers.length; i++) {
        	var properties = layers[i].feature.geometry.properties;
        	if(properties.object == rel && properties.id == id){
        		layers[i].dragging.enable();
        		layers[i].on("dragend", function(e){
        			var latlng = e.target.getLatLng();
        			$("[name=lat]").val(latlng.lat);
        			$("[name=lon]").val(latlng.lng);
        		});
        	}

        };
    });
}

$( document ).ready(function() {
	phenoclim.session = {}
	if($("#map").length > 0){
		phenoclim.session.map = new phenoclim.map(phenoclim.options);
	}
});