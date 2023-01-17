function displayAllUsers(data){
    $("#user-info-content").empty()
    $.each(data, function(index, value){
        var user_id = value["id"];
        console.log("id", user_id)
        var first_name = value["first_name"]
        console.log("first_name", first_name)
        var last_name = value["last_name"]
        console.log("last_name", last_name)
        var user_item = $("<div class = 'row user_item_div row-margin' data-userId = '"+user_id+"'>")
        user_item.html("<div class = 'col-11'><div class='user_id_div'>User "+user_id+"</div><div class='read_first_name'>First Name: "+first_name+"</div><div class='read_last_name'>Last Name: "+last_name+"</div></div><div class='col-1 delete-btn-div'><button class = 'delete-btn' data-buttonId='"+user_id+"'>X</button></div>")
        $("#user-info-content").append(user_item);
    });
}

function deleteUsers(id){
    //$(".user_item_div[data_userId = '"+id+"']").remove();
    var user_deleted = {
        "id" : id
    }
    console.log(id)
    $.ajax({
        type: "POST",
        url: "delete",                
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(user_deleted),
        success: function(result){
            let all_data = result["data"]
            data = all_data
            displayAllUsers(data)
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    });
}

$(document).ready(function(){
    displayAllUsers(data);
    $(".delete-btn").click(function(){
        var id = $(this).data("buttonid");
        deleteUsers(id);
    });
});