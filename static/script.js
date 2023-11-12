function initMap() {
  var centerCoordinates = { lat: 37.7749, lng: -122.4194 };

  var map = new google.maps.Map(document.getElementById('map'), {
    center: centerCoordinates,
    zoom: 13,
    mapTypeControl: false,
    streetViewControl: false
  });

  var panControl = new google.maps.PanControlOptions();
  var zoomControl = new google.maps.ZoomControlOptions();

  map.setOptions({
    panControl: true,
    panControlOptions: panControl,
    zoomControl: true,
    zoomControlOptions: zoomControl
  });
}

function findRoute() {
  // Add your logic for finding and displaying the route
  console.log("Initiating Emergency Rerouting...");
}
