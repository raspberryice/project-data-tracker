var ongoingList = document.getElementById("ongoingList").getElementsByTagName('ul')[0]
var removedList = document.getElementById("removedList").getElementsByTagName('ul')[0]

function markAsRemoved(e){
    var targetBtn = e.target;
    var listItem = targetBtn.parentNode;
    ongoingList.removeChild(listItem);
    listItem.removeChild(targetBtn);
    removedList.appendChild(listItem);

}
