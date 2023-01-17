function checkOriginalStatus(job_data){
    var status = job_data["status"];
    $("input[name = 'status'][value = '"+status+"']").attr("checked", true);
}

function updateJobs(id){
    $("#add_job_alert_div").empty();

    var position = $("#position_input").val();
    console.log("position new job: ", position);

    var company = $("#company_input").val();
    console.log("company new job: ", company);

    var url = $("#URL_input").val();
    console.log("url new job: ", url);

    var status = $("input[name = 'status']:checked").val();
    console.log("status new job: ", status);

    var location = $("#location_input").val();
    console.log("location new job: ", location);
    
    var applied_date = $("#applied_date_input").val();
    console.log("applied_date new job: ", applied_date);
    
    var note = $("#note_input").val();
    console.log("note new job: ", note);

    if(position && company && url && status && location && applied_date && position.trim().length != 0 && company.trim().length != 0 && url.trim().length != 0 && location.trim().length != 0){
        console.log("adding jobs");
        update_job_data ={
            "position": position,
            "company": company,
            "url": url,
            "status": status,
            "location": location,
            "applied_date": applied_date,
            "note": note
        }
        update_info = {
            "doc_id": id,
            "update_job_data": update_job_data
        }
        $.ajax({
            type: "POST",
            url: "/update_jobs",                
            dataType : "json",
            contentType: "application/json; charset=utf-8",
            data : JSON.stringify(update_info),
            success: function(result){
                document.location.href="/view_applied_jobs"
            },
            error: function(request, status, error){
                console.log("Error");
                console.log(request)
                console.log(status)
                console.log(error)
            }
        });
    }else{
        console.log("alerting -- add jobs")
        $("#add_job_alert_div").html("<div class='alert alert-danger' role='alert'>You cannot leave any input blank</div>");
        $("#position_input").focus();
    }
}


$(document).ready(function(){
    checkOriginalStatus(job_data);
    $("#save_job_btn").click(function(){
        updateJobs(id);
    });
});