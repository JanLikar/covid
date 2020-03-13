"use strict";


function setCookie(name, value, days) {
    var date = new Date();
    date.setTime(date.getTime() + (days*24*60*60*1000));

    document.cookie = name + "=" + value + "; expires="  + date.toUTCString() + "; path=/";
}
