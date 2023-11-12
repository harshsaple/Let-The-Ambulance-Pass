


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

function sendPlaceNames() {
  // Add your logic for finding and displaying the route
  console.log("Initiating Emergency Rerouting...");
  var start_place = document.getElementById("placeInput1").value;
  var end_place = document.getElementById("placeInput2").value;
  console.log(start_place)
  var data = {
    'start_place': start_place,
    'end_place': end_place
  };
  console.log(data)
  // Make a POST request to the backend endpoint
  fetch('/place-names', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
      // Add any other headers you may need
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(data => {
      // Handle the response from the server
      console.log('Server response:', data);
      // const requestData = {
      //   start_coord: { lat: data['start_lat'], lng: data['end_long'] },
      //   end_coord: { lat: data['end_lat'], lng: data['end_long'] }
      // };

      // // Make an AJAX request to the Flask API
      // console.log(requestData)
    })
    .catch(error => {
      console.error('Error:', error);
    });
  fetch('/place-names', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
      // Add any other headers you may need
    },

  })
    .then(response => response.json())
    .then(data => {
      // Handle the response from the server
      console.log('Server response:', data);

      plotPolyLine(data)
    })
    .catch(error => {
      console.error('Error:', error);
    });

}

function convertArrayFormat(inputArray) {
  return inputArray.map(coordinates => {
    return {
      lat: coordinates[1],
      lng: coordinates[0]
    };
  });
}

function plotPolyLine(coordinatePoints) {
  console.log(coordinatePoints)
  var formattedArray = convertArrayFormat(coordinatePoints)

  console.log(formattedArray)

  // for (var i = 0; i < coordinatePoints.length; i++) {
  //   var lat = coordinatePoints[i][1];
  //   var lng = coordinatePoints[i][0];

  //   var formattedCoordinate = {
  //     lat: lat,
  //     lng: lng
  //   };

  //   formattedArray.push(formattedCoordinate);
  // }


  var pathPolyline = new google.maps.Polyline({
    path: formattedArray,
    geodesic: true,
    strokeColor: '#FF0000',
    strokeOpacity: 1.0,
    strokeWeight: 5
  });

  pathPolyline.setMap(map);

  // Fit the map bounds to the polyline
  var bounds = new google.maps.LatLngBounds();
  for (var i = 0; i < coordinatePoints.length; i++) {
    bounds.extend(new google.maps.LatLng(coordinatePoints[i].lat, coordinatePoints[i].lng));
  }
  map.fitBounds(bounds);

  // Add markers for the start and end points
  startMarker = new google.maps.Marker({
    position: coordinatePoints[0],
    map: map,
    title: 'Start Point'
  });

  endMarker = new google.maps.Marker({
    position: coordinatePoints[coordinatePoints.length - 1],
    map: map,
    title: 'End Point',
    icon: {
      url: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png', // Green pointer icon
      scaledSize: new google.maps.Size(40, 40) // Adjust the size as needed
    }
  });

  // Add pop-ups to the markers with user input content
  addInfoWindow(startMarker, 'Current Location', currentLocation);
  addInfoWindow(endMarker, 'Hospitals Nearby', hospitalsNearby);
}

function searchPlaces(inputId, dropdownId) {
  var input = document.getElementById(inputId).value;

  if (input.length < 3) {
    $('#' + dropdownId).hide();
    return;
  }

  $.ajax({
    url: '/search_places',
    type: 'GET',
    data: { 'query': input },
    success: function (response) {
      var dropdown = $('#' + dropdownId);
      dropdown.empty();
      dropdown.show();

      response.forEach(function (place) {
        dropdown.append($('<option></option>').attr('value', place.place_id).text(place.name + ', ' + place.formatted_address));
      });
    },
    error: function (error) {
      console.log(error);
    }
  });
}

function selectPlace(dropdownId, inputId) {
  var selectedPlace = $('#' + dropdownId).val();
  var selectedText = $('#' + dropdownId + ' option:selected').text();
  $('#' + inputId).val(selectedText);
  $('#' + dropdownId).hide();
  if (selectedPlace) {
    console.log('Place selected:', selectedPlace);

  }
}


