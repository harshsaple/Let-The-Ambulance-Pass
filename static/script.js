


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
  var end_place = document.getElementById("placeInput2").value();

  var data = {
    startPlace: start_place,
    endPlace: end_place
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
    })
    .catch(error => {
      console.error('Error:', error);
    });

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
        dropdown.append($('<option></option>').attr('value', place.place_id).text(place.name));
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


