var c=0;
var t;
function starttimer()
{
    document.getElementById('timerdisplay').value = c;
    c = c + 1;
    t = setTimeout("starttimer()",1000);
}
