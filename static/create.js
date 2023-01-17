function addName(){
    let first_name = $("#first-name").val();
    console.log("first_name:", first_name);
    let last_name = $("#last-name").val();
    console.log("last_name:", last_name);
    if(first_name && last_name && first_name.trim().length!=0 && last_name.trim().length != 0){
        //send first name and last name to server and add in database
        let data_to_add = {"first_name": first_name, "last_name": last_name};
        $.ajax({
            type: "POST",
            url: "create",                
            dataType : "json",
            contentType: "application/json; charset=utf-8",
            data : JSON.stringify(data_to_add),
            success: function(result){
                // response = result["response"]
                // console.log("create-response", response);
                // response_status = response["response_status"]
                // if(response_status == "success"){
                    $("#create-response").html("<span>Create data successfully!</sapn>");
                    $("input").val("");
                    $("#first-name").focus();
                // }
            },
            error: function(request, status, error){
                console.log("Error");
                console.log(request)
                console.log(status)
                console.log(error)
            }
        });
    }else{
        $("#create-response").html("<span class = 'create-fail'>Neither first name and last name can be empty!</sapn>");
        $("#first-name").focus();
    }
}

$(document).ready(function(){
    $(".submit-btn").click(function(){
        //$("#create-response").empty();
        addName();
    });

    $("#last-name").keyup(function(e){
        if(e.whihc == 13){
            //$("#create-response").empty();
            addName();
        }
    });

    $("#first-name").keyup(function(e){
        if(e.whihc == 13){
            //$("#create-response").empty();
            addName();
        }
    });
});