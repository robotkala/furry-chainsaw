window.onload = initialize_sess_api();

function initialize_sess_api() {
    
    window.hosturl = 'http://localhost:5000';
    if (getCookie('_ga') == undefined) {

        var ga_id = prompt("Please enter a cookie:", 'GA1.2.37.1479217586');
        if (ga_id != null) {
            createCookie('_ga', ga_id, 1);
        }
    }

    var ga_cookie = getCookie('_ga');

    var user_nr_from_cookie = parseInt(ga_cookie.split('.')[2]);

    if (user_nr_from_cookie % 37 === 0) {
        onLoadEvent();
        exitIntentListener();
        window.addEventListener("beforeunload", onUnLoadEvent);
    }
}

function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

function createCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + '=' + value + expires + "; path=/";
}

function onLoadEvent() {
    var xhttp = new XMLHttpRequest();
    url = window.hosturl + "/on_load_event";
    console.log(url);
    xhttp.open("GET", url, true);
    xhttp.send();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {

            window.user_leaving_in = JSON.parse(xhttp.responseText).user_leaving_in;
            window.tabcounter = JSON.parse(xhttp.responseText).counter;
            window.visited = JSON.parse(xhttp.responseText).visited;
            window.exp_time = JSON.parse(xhttp.responseText).exp_time;

            setTimeout(userLeaving, window.user_leaving_in * 1000);

            if (window.visited == 1) {
                setTimeout(setVisitedTimer, window.exp_time * 1000);
            }
        }
    };
}

function userLeaving() {
    alert("You should leave now!");
}

function onUnLoadEvent() {
    var xhttp = new XMLHttpRequest();
    url = window.hosturl + "/on_unload_event/" + window.tabcounter;
    xhttp.open("GET", url, false);
    xhttp.send();
}

function setVisitedTimer() {
    window.visited = 0;
    exitIntentListener();
}

function exitIntentListener() {
    $(document).mouseleave(function (e) {
        if (e.clientY < 0 && window.visited == 0) {
            exitIntentEvent();
            alert("You left the window :)");
            window.visited = 1;
            setTimeout(setVisitedTimer, window.exp_time * 1000);
        }
    });
}

function exitIntentEvent() {
    var xhttp = new XMLHttpRequest();
    url = window.hosturl + "/exit_intent_event/" + window.tabcounter;
    xhttp.open("GET", url, true);
    xhttp.send();
}
