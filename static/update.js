function displayAllUsers(data){
    $("#user-info-content").empty()
    $.each(data, function(index, value){
        var user_id = value["id"];
        //console.log("id", user_id)
        var first_name = value["first_name"]
        //console.log("first_name", first_name)
        var last_name = value["last_name"]
        //console.log("last_name", last_name)
        var user_item = $("<div class = 'row user_item_div row-margin' data-userId = '"+user_id+"'>")
        user_item.html("<div class = 'col-10'><div class='user_id_div'>User "+user_id+"</div><div class='update_first_name'>First Name: <input class= 'update_first_name_input' data-id = '"+user_id+"' value ='"+first_name+"'></div><div class='update_last_name'>Last Name: <input class='update_last_name_input' data-id = '"+user_id+"' value= '"+last_name+"'></div><div class = 'update-response' data-id = '"+user_id+"'></div></div><div class='col-2 update-btn-div'><button class = 'update-btn' data-buttonid='"+user_id+"'>Update</button></div>")
        $("#user-info-content").append(user_item);
    });
}

function updateUsers(id){
    console.log("id", id)
    var updated_first_name = $(".update_first_name_input[data-id = '"+id+"']").val()
    console.log("update_first_name", updated_first_name)
    var updated_last_name =  $(".update_last_name_input[data-id = '"+id+"']").val()
    if(updated_first_name && updated_last_name && updated_first_name.trim().length!=0 && updated_last_name.trim().length != 0){
        //send new data to server and update
        update_user_data = {
            "id" :id,
            "first_name": updated_first_name,
            "last_name": updated_last_name
        }
        console.log("new_data", update_user_data)
        $.ajax({
            type: "POST",
            url: "update",                
            dataType : "json",
            contentType: "application/json; charset=utf-8",
            data : JSON.stringify(update_user_data),
            success: function(result){
                let all_data = result["data"]
                data = all_data
                console.log("update_data", data)
                displayAllUsers(data)
                $(".update-response[data-id = '"+id+"']").html("<span>Update successfully!</span>")
            },
            error: function(request, status, error){
                console.log("Error");
                console.log(request)
                console.log(status)
                console.log(error)
            }
        });
    }else{
        //alert
        $(".update-response[data-id = '"+id+"']").html("<span class = 'update-fail'>Neither first name and last name can be empty!</span>")
        console.log("fail-update", id)
        $(".update_first_name_input[data-id = '"+id+"']").focus()
    }
}

$(document).ready(function(){
    displayAllUsers(data);
    $(".update-btn").click(function(){
        $(".update-response[data-id = '"+id+"']").empty()
        var id = $(this).data("buttonid");
        console.log("id", id)
        updateUsers(id);
    });
});