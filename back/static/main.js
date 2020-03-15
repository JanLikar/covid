"use strict";


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
          map.flyTo(L.latLng(data.lat, data.lon));
        },
        error: function( xhr, err ) {
          alert(err);
        }
    });
    return false;
});
