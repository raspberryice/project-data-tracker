var myVar = setInterval(myTimer, 1000);
var totseconds = 0;
function myTimer() {
    totseconds = totseconds + 1;
    var hour = Math.floor(totseconds / 3600),
        minute = Math.floor(totseconds % 3600 / 60),
        sec = Math.floor(totseconds % 60);
    if (hour < 10) hour = '0' + hour;
    if (minute < 10) minute = '0' + minute;
    if (sec < 10) sec = '0' + sec;
    document.getElementById("timerdisplay").innerHTML = hour + ":" + minute + ":" + sec;
}
var paused = false;
function pausetimer() {
    if (paused) {
        paused = false;
        document.getElementById("pausebutton").innerHTML = "Pause";
        document.getElementById("pausebutton").setAttribute("class", "btn btn-md btn-info");
        myVar = setInterval(myTimer, 1000);
    } else {
        clearInterval(myVar);
        document.getElementById("pausebutton").innerHTML = "Resume";
        document.getElementById("pausebutton").setAttribute("class", "btn btn-md btn-success");
        paused = true;
    }
}
function stoptimer() {
    clearInterval(myVar);
    document.getElementById("stopbutton").innerHTML = "Submit";
    document.getElementById("stopbutton").setAttribute("class", "btn btn-md btn-success")
    document.getElementById("pausebutton").remove();
    document.getElementById("time").setAttribute("value", document.getElementById("timerdisplay").innerHTML);
}
