/**
 * Created by martinl on 05/01/2017.
 */

function onLoadEvent() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://localhost:5000/on_load_event", true);
    xhttp.send();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(JSON.parse(xhttp.responseText).user_leaving_in);
        }
    };

}

function onUnLoadEvent() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://localhost:5000/on_unload_event", false);
    xhttp.send();
}
