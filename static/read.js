function displayAllUsers(data){
    $.each(data, function(index, value){
        var user_id = value["id"];
        console.log("id", user_id)
        var first_name = value["first_name"]
        console.log("first_name", first_name)
        var last_name = value["last_name"]
        console.log("last_name", last_name)
        var user_item = $("<div class = 'col user_item_div' data-userId = '"+user_id+"'>")
        user_item.html("<div class='user_id_div'>User "+user_id+"</div><div class='read_first_name'>First Name: "+first_name+"</div><div class='read_last_name'>Last Name: "+last_name+"</div>")
        $("#user-info-content").append(user_item);
    });
}

$(document).ready(function(){
    displayAllUsers(data);
});