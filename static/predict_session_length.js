/**
 * Created by martinl on 23/12/2016.
 */
function predictSessLength() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://localhost:5000/make_prediction", true);
    xhttp.send();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(JSON.parse(xhttp.responseText).user_leaving_in);
            console.log(document.cookie);
            var time = JSON.parse(xhttp.responseText).user_leaving_in * 1000;
            finalCountDown(time);
            /*
            console.log(JSON.parse(xhttp.responseText).prediction);
            alert('blha')
            */

        }
    };

}

function finalCountDown(time) {
    setTimeout(function(){ alert("Hello"); }, time);
}
