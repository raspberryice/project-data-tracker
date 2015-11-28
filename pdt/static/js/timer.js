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

var removedList = $("#removedList").children('ul');
var ongoingList = $("#ongoingList").children('ul');
function stoptimer() {
    pausetimer();
    document.getElementById("time").setAttribute("value", document.getElementById("timerdisplay").innerHTML);
    //for defect session
    $('#defectNo').attr("value",removedList.find('li').length);
    if (ongoingList.find('li').length ){
        $('#submitMessage').text("You have "+ ongoingList.find('li').length +" defects not yet removed!");
     }
     else {
         $('#submitMessage').text('');
     }
}
$('#submitmodal').on('hidden.bs.modal',function(){
        paused = false;
        document.getElementById("pausebutton").innerHTML = "Pause";
        document.getElementById("pausebutton").setAttribute("class", "btn btn-md btn-info");
        myVar = setInterval(myTimer, 1000);

});
