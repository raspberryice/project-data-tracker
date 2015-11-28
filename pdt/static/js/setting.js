$(document).ready(function(){
   $('#add').click(function() {
    return !$('#developerlist option:selected')
.remove().appendTo('#selected_developers');
   });
   $('#remove').click(function() {
    return !$('#selected_developers option:selected')
.remove().appendTo('#developerlist');
   });
   $('#submitdeveloperlist').click(function() {
     $('#selected_developers').find('option').each(function() {
        $(this).attr('selected', 'selected');
       });
     $("#developerform").submit();
   });

function selectall()  {
$('#selected_developers').find('option').each(function() {
   $(this).attr('selected', 'selected');
  });
}
});
