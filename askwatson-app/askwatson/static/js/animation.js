 // This example adds an animated symbol to a polyline.
 var marker=new google.maps.Marker({
  position: new google.maps.LatLng(35.621444, 139.748835),
});
 var map;
 var line;
 var lineCoordinates ={};
 var elevator;
 var infowindow = new google.maps.InfoWindow();
 var sdata = {};
 var elevations = [];//new Array(d.length);
 var d;

  var lineCoordinates = [];
  var locations = [];

  var markers = [];

 function get_data (log_id) {

  $.ajax({
   url: "/logview/" + log_id,
   dataType: 'json',
   async: false,
   cache: false,
   timeout: 30000,
   success: function(json) {
     sdata = json;
   }
 });
}


function initialize() {

  d = sdata.data;

  var mapOptions = {
    // samurai
    center: new google.maps.LatLng(Number(d[parseInt(d.length/2)].latitude), Number(d[parseInt(d.length/2)].longitude)), 
    zoom: 16,
    mapTypeId: google.maps.MapTypeId.TERRAIN
  };


  map = new google.maps.Map(document.getElementById('googleMap'), mapOptions);
  
   // Create an ElevationService
   elevator = new google.maps.ElevationService();
  // Add a listener for the click event and call getElevation on that location
  // google.maps.event.addListener(map, 'click', getElevation);
  run();

  console.log(elevations);
  
  //Clusterer
  var mcOptions = {gridSize: 50, maxZoom: 15};
  var markerCluster = new MarkerClusterer(map, markers);


  for (var cord in lineCoordinates){
        //console.log(lineCoordinates[cord]);
        $( "<div class='bar' id=" + cord+" style='border-top-width: 10px; height: 40px;width: 2px;'></div>" ).appendTo( ".graph" );
    }
      $( ".bar" ).mouseover(function() {
        var id = $(this).attr("id");
        console.log(id + " in");
        var pos = new google.maps.LatLng(lineCoordinates[id].lat(), lineCoordinates[id].lng());
        marker=new google.maps.Marker({
          position:pos,
        });
        marker.setMap(map);
        $("#para").text("Elevation: " + $(this).height() + " metr");
      });
      $( ".bar" ).mouseout(function() {
        var id = $(this).attr("id");
        console.log(id + " out");
        marker.setMap(null);
      });

      // Define the symbol, using one of the predefined paths ('CIRCLE')
      // supplied by the Google Maps JavaScript API.
      var lineSymbol = {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 5,
        strokeColor: '#393'
      };

      // Create the polyline and add the symbol to it via the 'icons' property.
      line = new google.maps.Polyline({
        path: lineCoordinates,
        strokeColor:"#FD5959",
        strokeOpacity:0.8,
        strokeWeight:1.5,

        icons: [{
          icon: lineSymbol,
          offset: '100%'
        }],
        map: map
      });

      animateCircle();
      //elevate();
    }

// Use the DOM setInterval() function to change the offset of the symbol
// at fixed intervals.
function animateCircle() {
  var count = 0;
  window.setInterval(function() {
    count = (count + 1) % 100;

    var icons = line.get('icons');
    icons[0].offset = (count / 2) + '%';
    line.set('icons', icons);
  }, 40);
}

function populate(){
    for (var i = 0; i < d.length; i++) {
      if (Number(d[i].latitude)>0){
        var pos = new google.maps.LatLng(Number(d[i].latitude), Number(d[i].longitude));
        lineCoordinates.push(pos);
        marker=new google.maps.Marker({
          position:pos
          // icon: {
          //   path: google.maps.SymbolPath.CIRCLE,
          //   scale: 10
          // },
        });

        // var markerOptions = {
        //   strokeColor: '#FF0000',
        //   strokeOpacity: 0.8,
        //   strokeWeight: 2,
        //   fillColor: '#FF0000',
        //   fillOpacity: 0.35,
        //   map: map,
        //   center: pos,
        //   radius: 10
        // };
        // // Add the circle for this city to the map.
        // cityCircle = new google.maps.Circle(markerOptions);


        markers.push(marker);
        //marker.setMap(map);
      }
    }
    // alert("populate");
  }

function elevate () {
    //Add elevation
  // alert("elevate");
  var positionalRequest = { 'locations': lineCoordinates };

  elevator.getElevationForLocations(positionalRequest, function (results, status) {
    if (status == google.maps.ElevationStatus.OK) {
      // alert(results);
      for (var res in results){
        if (results[res]) {
            // console.log(results[res].elevation);
            // setTimeout(elevations.push(results[res].elevation), 10);
            // console.log("#"+res + ": " + results[res].elevation + "px");
            var height = parseInt(results[res].elevation*10);
            $("#"+res).attr("style", "border-top-width: " + height +"px;width: 4px; height: "+ (60-height)+"px;");
            // elevations[res] = results[res].elevation;
          }
        }
      }
    });
}

    function run(){
      var d = jQuery.Deferred(), 
      p=d.promise();
      //You can chain jQuery promises using .then
      p.then(populate).then(elevate);
      d.resolve();
    }

function getElevation(event) {

  var locations = [];

  // Retrieve the clicked location and push it on the array
  var clickedLocation = event.latLng;
  locations.push(clickedLocation);

  // Create a LocationElevationRequest object using the array's one value
  var positionalRequest = {
    'locations': locations
  }

  // Initiate the location request
  elevator.getElevationForLocations(positionalRequest, function(results, status) {
    if (status == google.maps.ElevationStatus.OK) {

      // Retrieve the first result
      if (results[0]) {

        // Open an info window indicating the elevation at the clicked position
        infowindow.setContent('The elevation at this point <br>is ' + results[0].elevation + ' meters.');
        infowindow.setPosition(clickedLocation);
        infowindow.open(map);
      } else {
        alert('No results found');
      }
    } else {
      alert('Elevation service failed due to: ' + status);
    }
  });
}
