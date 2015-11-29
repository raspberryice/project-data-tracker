$(function() {

    Morris.Area({
        element: 'latestActivity',
        data: convertDict(data),
        xkey: 'period',
        ykeys: ['sloc', 'defect'],
        labels: ['Delivered SLOC', 'Removed Defects'],
        pointSize: 2,
        hideHover: 'auto',
        resize: true,
    });
});

var data = JSON.parse($('#graphData').text());

function convertDict(data){
    var ret = [];
    for(var i =0;i<data.length;i++){
        ret.push({
            period: data[i][0],
            sloc: data[i][1],
            defect : data[i][2],
        });
    }
    return ret;
}
