$(function() {

    Morris.Area({
        element: 'latestActivity',
        data: [{
            period: '2015-10-13',
            sloc: 2.66,
            defect: 5,
        }, {
            period: '2015-10-14',
            sloc: 2.77,
            defect: 10,
        }, {
            period: '2015-10-15',
            sloc: 5,
            defect: 15,
        }, {
            period: '2015-10-16',
            sloc: 4,
            defect: 25,
        }, {
            period: '2015-10-17',
            sloc: 6,
            defect: 9,
        }, {
            period: '2015-10-18',
            sloc: 5,
            defect: 2,
        }, {
            period: '2015-10-19',
            sloc: 4,
            defect: 20,
        }, {
            period: '2015-10-20',
            sloc: 15,
            defect: 59,
        }, {
            period: '2015-10-21',
            sloc: 10,
            defect: 12,
        }, {
            period: '2015-10-22',
            sloc: 8,
            defect: 30,
        }],
        xkey: 'period',
        ykeys: ['sloc', 'defect'],
        labels: ['Delivered Hundred SLOC', 'Removed Defects'],
        pointSize: 2,
        hideHover: 'auto',
        resize: true,
    });
});
