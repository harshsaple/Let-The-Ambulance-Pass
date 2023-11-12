var map = document.getElementById('map');
var pathCoordinates = []; // Array to store the coordinates of the path
var startMarker, endMarker; // Variables to store the start and end markers

function initMap(lat = 37.7749, lng = -122.4194) {
    var centerCoordinates = { lat: lat, lng: lng };

    map = new google.maps.Map(document.getElementById('map'), {
        center: centerCoordinates,
        zoom: 13,
        mapTypeControl: false,
        streetViewControl: false
    });

    var panControl = new google.maps.PanControlOptions();
    var zoomControl = new google.maps.ZoomControlOptions();

    map.setOptions({
        panControl: true,
        zoomControl: true,
        panControlOptions: panControl,
        zoomControlOptions: zoomControl
    });
}


function sendPlaceNames() {
    // Add your logic for finding and displaying the route

    console.log("Initiating Emergency Rerouting...");
    // window.location.reload();
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
            // findRoute(data)
            formattedData = convertArrayFormat(data)
            console.log(formattedData)
            var pathPolyline = new google.maps.Polyline({
                path: formattedData,
                geodesic: true,
                strokeColor: '#FF0000',
                strokeOpacity: 1.0,
                strokeWeight: 5
            });

            pathPolyline.setMap(map);

            // Fit the map bounds to the polyline
            var bounds = new google.maps.LatLngBounds();
            for (var i = 0; i < formattedData.length; i++) {
                bounds.extend(new google.maps.LatLng(formattedData[i].lat, formattedData[i].lng));
            }
            map.fitBounds(bounds);

            // Add markers for the start and end points
            startMarker = new google.maps.Marker({
                position: formattedData[0],
                map: map,
                title: 'Start Point'
            });

            endMarker = new google.maps.Marker({
                position: formattedData[formattedData.length - 1],
                map: map,
                title: 'End Point',
                icon: {
                    url: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png', // Green pointer icon
                    scaledSize: new google.maps.Size(40, 40) // Adjust the size as needed
                }
            });

            // Add pop-ups to the markers with user input content
            addInfoWindow(startMarker, start_place, formattedData[0]);
            addInfoWindow(endMarker, end_place, formattedData[formattedData.length - 1]);

            // Randomly select a point on the path
            var randomIndex = Math.floor(Math.random() * (formattedData.length - 2)) + 1; // Exclude start and end points
            var randomLocation = formattedData[randomIndex];
            console.log(randomLocation)
            // Add a car marker at the random location    
            var carMarker = new google.maps.Marker({
                position: randomLocation,
                map: map,
                title: 'Random Car Location',
                icon: {
                    url: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                    scaledSize: new google.maps.Size(40, 40)
                }
            });

            // Add an info window (popup) to the car marker
            addInfoWindow(carMarker, 'Random Car', 'Car on the path of the ambulance');

            console.log("Initiating Emergency Rerouting...");
            // 37.772903679007456, -122.43040929805751 reroute
            // 
            alert('Emergency Rerouting initiated!');
            var destPoint = new google.maps.LatLng(37.772903679007456, -122.43040929805751); // Replace with your destination coordinates
            var directionsService = new google.maps.DirectionsService();

            // Request for the directions from the car marker to the destination
            var request = {
                origin: carMarker.getPosition(),
                destination: destPoint,
                travelMode: google.maps.TravelMode.DRIVING
            };

            // Use the DirectionsService to calculate the route
            directionsService.route(request, function (response, status) {
                if (status === google.maps.DirectionsStatus.OK) {
                    // Display the route on the map
                    var directionsDisplay = new google.maps.DirectionsRenderer();
                    directionsDisplay.setMap(map);
                    directionsDisplay.setDirections(response);
                } else {
                    // Handle the error appropriately
                    console.error('Error getting directions:', status);
                }
            });

            //Alert for rerouting
            //alert('Emergency Rerouting initiated!');


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


function findRoute(coordinatePoints) {
    // Simulate getting coordinate points from the backend
    //   var coordinatePoints = getCoordinatePoints();

    // Draw a polyline using the coordinate points
    formattedData = convertArrayFormat(coordinatePoints)
    console.log(formattedData)
    var pathPolyline = new google.maps.Polyline({
        path: formattedData,
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

    // Randomly select a point on the path
    var randomIndex = Math.floor(Math.random() * (coordinatePoints.length - 2)) + 1; // Exclude start and end points
    var randomLocation = coordinatePoints[randomIndex];

    // Add a car marker at the random location    
    var carMarker = new google.maps.Marker({
        position: randomLocation,
        map: map,
        title: 'Random Car Location',
        icon: {
            url: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
            scaledSize: new google.maps.Size(40, 40)
        }
    });

    // Add an info window (popup) to the car marker
    addInfoWindow(carMarker, 'Random Car', 'Car on the path of the ambulance');

    console.log("Initiating Emergency Rerouting...");
}

// Function to simulate getting coordinate points from the backend
function getCoordinatePoints() {
    return [
        { lat: 37.770558905016905, lng: -122.44254506450635 }, // Example coordinate points
        { lat: 37.770502567294436, lng: -122.44294881818402 },
        { lat: 37.77050256729126, lng: -122.44294881820679 },
        { lat: 37.770481109619141, lng: -122.44303464889526 }, // Example coordinate points
        { lat: 37.770459651947021, lng: -122.44335651397705 },
        { lat: 37.770416736602783, lng: -122.44367837905884 },
        { lat: 37.769472599029541, lng: -122.44346380233765 }, // Example coordinate points
        { lat: 37.769408226013184, lng: -122.44344234466553 },
        { lat: 37.768936157226563, lng: -122.44333505630493 },
        { lat: 37.768292427062988, lng: -122.44361400604248 }, // Example coordinate points
        { lat: 37.7679705619812, lng: -122.44372129440308 },
        { lat: 37.7675199508667, lng: -122.44387149810791 },
        { lat: 37.767090797424316, lng: -122.44376420974731 }, // Example coordinate points
        { lat: 37.766940593719482, lng: -122.44369983673096 },
        { lat: 37.766575813293457, lng: -122.44339942932129 },
        { lat: 37.766554355621338, lng: -122.44335651397705 }, // Example coordinate points
        { lat: 37.766468524932861, lng: -122.44320631027222 },
        { lat: 37.766382694244385, lng: -122.44312047958374 }
    ];
}

// Function to add info window to a marker
function addInfoWindow(marker, title, content) {
    var infowindow = new google.maps.InfoWindow({
        content: '<div><strong>' + title + '</strong><br>' + '</div>'
    });

    marker.addListener('click', function () {
        infowindow.open(map, marker);
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