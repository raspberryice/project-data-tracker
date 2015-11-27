$('.devSessionBtn').on('click',function(e){
    var li = $(this).parent();
    li.addClass('current');
    var time = li.children('.time').text();
    var sloc = parseInt(li.children('.sloc').text());
    console.log (sloc);
    var id = li.children('.id').text();
    $('#devTime').val(time);
    $('#devSLOC').val(sloc);
    $('#devId').val(id);
    $('#submitDev').modal('show');
});
$('.mngSessionBtn').on('click',function(e){
    var li = $(this).parent();
    li.addClass('current');
    var time = li.children('.time').text();
    var id = li.children('.id').text();
    $('#mngTime').val(time);
    $('#mngId').val(id);
    $('#submitMng').modal('show');
});

$('.remSessionBtn').on('click',function(e){
    var li = $(this).parent();
    li.addClass('current');
    var time = li.children('.time').text();
    var defect_no = li.children('.defectno').text();
    var id = li.children('.id').text();
    $('#remTime').val(time);
    $('#defectNo').val(defect_no);
    $('#remId').val(id);
    $('#submitRem').modal('show');
});

$('.viewDefectBtn').on('click',function(){
    var li = $(this).parent();
    li.addClass('current');
    var report = {
    'name':li.children('.name').text(),
    'date':li.children('.date').text(),
    'iterationInjected':li.children ('.inject').text(),
    'iterationRemoved':li.children('.remove').text(),
    'type':li.children('.type').text(),
    'desc':li.children('.desc').text(),
    };
    console.log(report);
    //hidden id field
    var defect_id = li.children('.id').text();
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
}

$('#updateDev').on('submit',function(e){
    e.preventDefault();
    $('#submitDev').modal('hide');
    $.ajax({
    url: "developer/update_dev",
    type :"POST",
    data :{
     'time': $('#devTime').val(),
     'sloc':$('#devSLOC').val(),
     'id': $('#devId').val(),
    },
    success: function(json){
        console.log("success");
    },
    error :function(xhr,errmsg,err){
        console.log(xhr.status + ': '+xhr.responseText);
    },
    });
    //update in html
    var li =$('#devSessionList').children('.current');
    li.children('.time').text($('#devTime').val());
    li.children('.sloc').text($('#devSLOC').val());


});

$('#updateRem').on('submit',function(e){
    e.preventDefault();
    $('#submitRem').modal('hide');
    $.ajax({
    url: "developer/update_rem",
    type :"POST",
    data :{
    'time':$('#remTime').val(),
    'id':$('#remId').val(),
    },
    success: function(json){
        console.log("success");
    },
    error :function(xhr,errmsg,err){
        console.log(xhr.status + ': '+xhr.responseText);
    },
    });

    var li =$('#remSessionList').children('.current');
    li.children('.time').text($('#remTime').val());
    li.children('.sloc').text($('#defectNo').val());

});

$('#updateMng').on('submit',function(e){
    e.preventDefault();
    $('#submitMng').modal('hide');
    $.ajax({
    url: "developer/update_mng",
    type :"POST",
    data :{
     'time':$('#mngTime').val(time),
     'id':  $('#mngId').val(id),
    },
    success: function(json){
        console.log("success");
    },
    error :function(xhr,errmsg,err){
        console.log(xhr.status + ': '+xhr.responseText);
    },
    });
    var li =$('#mngSessionList').children('.current');
    li.children('.time').text($('#remTime').val());
    li.children('.sloc').text($('#defectNo').val());


});

$('#editDefectForm').on('submit',function(e){
    e.preventDefault();
    $('#editReport').modal('hide');
    var id = $('')
    var report = {
          id:$('#defectId').val(),
          name: $('#viewDefectName').val(),
          date: $("#viewDefectDate").val(),
          iterationInjected: $('#viewIterationInjected').val(),
          iterationRemoved: $('#viewIterationRemoved').val(),
          type: $('#viewDefectType').val(),
          desc: $('#viewDefectDesc').val(),
        };
    update_defect(report);

});

function update_defect(report){
    $.ajax({
    url: "developer/update_defect/",
    type :"POST",
    data :report,
    success: function(json){
        console.log("success");
    },
    error :function(xhr,errmsg,err){
        console.log(xhr.status + ': '+xhr.responseText);
    },
    });

};
