$('#createDefectForm').on('submit',function(event){
    event.preventDefault();
     $('#defectReport').modal('hide');
    create_local_defect();
});

function create_defect(report){
    console.log($('#defectName').val());
    $.ajax({

    url: "adddefect/",//this may be change
    type :"POST",
    data :report,
    success: function(json){
        //console.log(json);//this sends a new request to beginDefectSession?
        console.log("success");
    },
    error :function(xhr,errmsg,err){
    //add error msg to DOM
        console.log(xhr.status + ': '+xhr.responseText);
    },
    })

};

sessionStorage.defect_no = 0;
function create_local_defect(){
    sessionStorage.defect_no = parseInt(sessionStorage.defect_no) +1;
    var defect = "defect_"+ sessionStorage.defect_no;
    var report = {
          name: $('#defectName').val(),
          iterationInjected: $('#iterationInjected').val(),
          sid: $('sid').val(),
          type: $('#defectType').val(),
          desc: $('#defectDesc').val(),
        };
     sessionStorage.setItem (defect,JSON.stringify(report));
     console.log('defect no ' + sessionStorage.defect_no+ ' has been stored locally.');
      var new_item = '<li class="list-group-item clearfix" id="'
        +defect
        +'"><span class="name">'
        + $('#defectName').val()
        +'</span>'
        +'<span class="pull-right">'
        +'<button class="btn btn-default edit-btn" >Edit</button>'
        +'<button class="btn btn-success remove-btn"  style="margin-left: 10px;">Removed</button></li>'
        +'</span>';
        $('#ongoingList').children('ul').append(new_item);
}
$('#createDefectBtn').on('click',function(e){
    clear_report();
    $('#defectReport').modal('show');
});


function clear_report(){
    $('#defectName').val('');
    $('#defectDate').val('');
    $('#iterationInjected').children().each(function(){
    $(this).removeAttr('selected');
    });
    $('#defectType').children().each(function(){
    $(this).removeAttr('selected');
    });
    $('#defectDesc').val('');
}


function render_report(report){

    $('#viewDefectName').val(report['name']);
    $('#viewDefectDate').val(report['date']);
    var iterationInjected = report['iterationInjected'];
    $('#viewIterationInjected').children().each(function(){
        if ($(this).text() == iterationInjected)
        {   $(this).attr('selected','selected');}
    });
    var selectedType = report['type'];
    var option = $('#viewDefectType').children();
    option.each(function(){
     if ($(this).attr('value')==selectedType)
       { $(this).attr('selected','selected');}
    });
    $('#viewDefectDesc').val(report['desc']);

}
$('#editDefectForm').on('submit',function(event){
    event.preventDefault();
     $('#editReport').modal('hide');
    update_local_defect();
    sessionStorage.removeItem("current_defect");
});

function update_local_defect(){
     var defect = sessionStorage.current_defect;
     var report = { name: $('#viewDefectName').val(),
          date: $("#viewDefectDate").val(),
          iterationInjected: $('#viewIterationInjected').val(),
          iterationRemoved: $('#viewIterationRemoved').val(),
          type: $('#viewDefectType').val(),
          desc: $('#viewDefectDesc').val(),
          status: 'True',
        };
     sessionStorage.setItem (defect,JSON.stringify(report));
     //update name
     var id = '#'+ defect;
     $(id).find('.name').text($('#viewDefectName').val());
     console.log(report);
     console.log('defect no ' + sessionStorage.defect_no+ ' has been updated locally.');

}

var ongoingList = $("#ongoingList").children('ul');
var removedList = $("#removedList").children('ul');
$('#ongoingList').on('click','.edit-btn',function(){
    var defect_id = $(this).parent().parent().attr('id');
    console.log(defect_id);
     var report = JSON.parse(sessionStorage.getItem(defect_id));
    render_report(report);
    $('#editReport').modal('show');
    sessionStorage.current_defect= defect_id;
})

$("#ongoingList").on('click','.remove-btn',function(){
    var li = $(this).parent().parent();
    var defect_id = li.attr('id');
    var report = JSON.parse(sessionStorage.getItem(defect_id))
    create_defect(report);
    //creating db object
    li.detach();
    removedList.append(li);
    li.find('.edit-btn').text("View");
    $(this).remove();
});

$('#removedList').on('click','.edit-btn',function(){
    var defect_id = $(this).parent().parent().attr('id');
    console.log(defect_id);
    var report = JSON.parse(sessionStorage.getItem(defect_id));
    render_report(report);
    $('#viewDefectName').attr('readonly','readonly');
    $('#viewDefectDate').attr('readonly','readonly');
    $('#viewDefectType').attr('disabled','disabled');
    $('#viewIterationInjected').attr('disabled','disabled');
    $('#viewDefectDesc').attr('readonly','readonly');
    $('#save-btn').remove();
    $('#editReport').modal('show');
})