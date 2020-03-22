"use strict";


function createMap(mapId) {
    var map = L.map(mapId);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    }).addTo(map);

    map.setView([0,0], 2);

    return map;
};


function loadMarkers(map, markers, only_owned=false) {
    var min_date_element = $('#map-filter-start');
    var max_date_element = $('#map-filter-end');

    var data = {};

    if (max_date_element && min_date_element) {
        data['max_date'] = max_date_element.val();
        data['min_date'] = min_date_element.val();
    };

    if (only_owned) {
        data['only_owned'] = 1
    };

    Object.values(markers).forEach(function (l) {map.removeLayer(l)});
    markers = {};

    $.getJSON("/list-markers", data, function( data ) {
        $.each( data, function( key, val ) {
            markers[val.id] = add_map_marker(map, val)
        });
    });
};


$("#use-my-location").click(function() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      function (position){
        window.localStorage.setItem('lat', position.coords.latitude)
        window.localStorage.setItem('lon', position.coords.longitude)
        map.panTo(new L.LatLng(position.coords.latitude, position.coords.longitude));
      },
      function(e) {console.log(e)}
    );
  };
});


$(document).on('click', '.remove-marker', function (e) {
  $.ajax({
    url: '/remove-marker/' + $(this).data('marker-id'),
    type: 'POST',
    success: function( data ) {
      marker_id = parseInt(e.target.getAttribute("data-marker-id"));
      map.removeLayer(markers[marker_id]);
      delete markers[marker_id];
    },
    error: function( xhr, err ) {
      alert(err);
    }
  });
});


function setLanguage(value) {
    setCookie("_LOCALE_", value, 14);
    location.reload();
};


function setCookie(name, value, days) {
    var date = new Date();
    date.setTime(date.getTime() + (days*24*60*60*1000));

    document.cookie = name + "=" + value + "; expires="  + date.toUTCString() + "; path=/";
}


var form_selector = '#search-address-form';
$(document).on('submit', form_selector, function(e) {
    $.ajax({
        url: $(this).attr('action'),
        type: $(this).attr('method'),
        data: $(this).serialize(),
        dataType: 'json',
        success: function( data ) {
          map.flyTo(L.latLng(data.lat, data.lon), 16);
        },
        error: function( xhr, err ) {
          alert(err);
        }
    });
    return false;
});


function add_map_marker(map, val) {
  var color = 'red';

  if(val.cur_status == 1){
    // suspicious
    color = '#ff7b00';
  } else if(val.cur_status == 0){
    // healthy
    color = '#b8b5b2';
  } else if(val.cur_status == 3){
    // disinfected
    color = '#b8b5b2';
  }

  var bgcolor = '#f03'

  var circle = L.circle([val.lat, val.lon], {
    color: color,
    fillColor: bgcolor,
    fillOpacity: 0.5,
    radius: 10
  }).addTo(map);

  circle.bindPopup(function (layer) {
    $.ajax({
        url: '/marker-popup/' + val.id,
        type: 'GET',
        success: function (data) {
            layer.unbindPopup();
            layer.bindPopup(data);
            layer.openPopup();
        },
        error: function(xhr, err) {
            alert(err);
        }
    });
  });
  return circle;
};
