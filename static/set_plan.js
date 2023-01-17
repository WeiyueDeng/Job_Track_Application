function setPlan(){
    $("#set_plan_alert_div").empty();

    var target_num = $("#target_num_input").val();
    var deadline = $("#deadline_input").val();
    console.log("target_num:" , target_num);
    console.log("deadline:" , deadline);
    
    if(target_num && deadline){
        console.log("setting plan");
        plan_data = {
            "target_num":target_num,
            "deadline": deadline
        }
        $.ajax({
            type: "POST",
            url: "set_plan",                
            dataType : "json",
            contentType: "application/json; charset=utf-8",
            data : JSON.stringify(plan_data),
            success: function(result){
                document.location.href="/"
            },
            error: function(request, status, error){
                console.log("Error");
                console.log(request)
                console.log(status)
                console.log(error)
            }
        });

    }else{
        console.log("altering");
        $("#set_plan_alert_div").html("<div class='alert alert-danger' role='alert'> You cannot leave any input blank</div>");
        if(!target_num){
            $("#target_num_input").focus();
        }else{
            $("#deadline_input").focus();
        }
        
    }
}

$(document).ready(function(){
    $("#submit_plan_btn").click(function(){
        setPlan();
    });
});