$('.devSessionBtn').on('click',function(e){
    var li = $(this).parent();
    var time = li.children('.time').text();
    var sloc = li.children('.sloc').text();
    var id = li.children('.id').text();
    $('#devTime').val(time);
    $('#devSLOC').val(sloc);
    $('#devId').val(id);
    $('#submitDev').modal('show');
});
$('.mngSessionBtn').on('click',function(e){
    var li = $(this).parent();
    var time = li.children('.time').text();
    var id = li.children('.id').text();
    $('#mngTime').val(time);
    $('mngId').val(id);
    $('#submitMng').modal('.show');
});

$('.remSessionBtn').on('click',function(e){
    var li = $(this).parent();
    var time = li.children('.time').text();
    var defect_no = li.children('.defectno').text();
    var id = li.children('.id').text();
    $('#remTime').val(time);
    $('#defectNo').val(defect_no);
    $('#remId').val(id);
    $('#submitMng').modal('show');
});

$('.viewDefectBtn').on('click',function(){
    var li = $(this).parent();
    var report = {
    'name':li.children('.name'),
    'date':li.children('.date'),
    'iterationInjected':li.children ('.inject'),
    'iterationRemoved':li.children('.remove'),
    'type':li.children('.type'),
    'desc':li.children('.desc'),
    };
    //hidden id field
    var defect_id = li.children('.id');
    $('#defectId').val(defect_id);
    render_report(report);
    $('#editReport').modal('show');
});

function render_report(report){

    $('#viewDefectName').val(report['name']);
    $('#viewDefectDate').val(report['date']);
    var iterationInjected = report['iterationInjected'];
    $('#viewIterationInjected').children().each(function(){
        if ($(this).text() == iterationInjected)
        {   $(this).attr('selected','selected');}
    });
     $('#viewIterationRemoved').children().each(function(){
        if ($(this).text() == report['iterationRemoved'])
        {   $(this).attr('selected','selected');}
    });

    var selectedType = report['type'];
    var option = $('#viewDefectType').children();
    option.each(function(){
     if ($(this).attr('value')==selectedType)
       { $(this).attr('selected','selected');}
    });

    $('#viewDefectDesc').text(report['desc']);
     console.log('done rendering report for'+defect);
}