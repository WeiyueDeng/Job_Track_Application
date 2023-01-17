function displayJobs(all_jobs){
    $(".content").empty();
    if(all_jobs.length == 0){
        $(".content").text("You haven't added any applied jobs yet!");
    }else{
        $.each(all_jobs, function(index, value){
            var job_id = value["doc_id"];
            var position  = value["position"];
            var company = value["company"];
            var url = value["url"];
            var status = value["status"];
            var location = value["location"];
            var applied_date = value["applied_date"];
            var note = value["note"];
    
            var job_div = $("<div class = 'row job_item_div' data-jobId = '"+job_id+"'>");
            var job_item_container = $("<div class ='col section-bg'>");
            var status_div = $("<div class = 'row status_div' data-jobId = '"+job_id+"'>");
            var status_converted = status.replace("_", " ");
            status_div.html("<div class = 'col-3'> <span class = '"+status+"'>"+status_converted+"</div><div class = 'col-7'></div><div class = 'col-2 delete_btn_div'><button class='delete_btn' data-buttonid = '"+job_id+"'> X </button></div>");
            var position_and_update_btn_div = $("<div class = 'row position_and_update_btn_div' data-jobId = '"+job_id+"'>");
            position_and_update_btn_div.html("<div class = 'col-7 position_content'><a class = 'position_link' href = '"+url+"' target='_blank'>"+position+"</a></div><div class = 'col-4 update_btn_div'><button class='update_btn' data-buttonid = '"+job_id+"'>Update</button></div>");
            var company_and_applied_date_div = $("<div class = 'row company_and_applied_date_div' data-jobId = '"+job_id+"'>");
            company_and_applied_date_div.html("<div class = 'col-7 company_content'>"+company+"</div><div class = 'col-4'></div>");
            var location_and_note_div = $("<div class = 'row location_and_note_div' data-jobId = '"+job_id+"'>");
            location_and_note_div.html("<div class = 'col-7 location_content'>"+location+"</div><div class = 'col-4 applied_date_content'> Applied on "+applied_date+"</div>");
    
            job_item_container.append(status_div);
            job_item_container.append(position_and_update_btn_div);
            job_item_container.append(company_and_applied_date_div);
            job_item_container.append(location_and_note_div);
            job_div.append(job_item_container);
            $(".content_jobs").append(job_div);
        });
    }
    
}

function update(btn){
    var btn_id = btn.data("buttonid");
    console.log("click btn: ", btn_id);
    url = "/view_applied_jobs/" + btn_id;
    document.location.href = url;
}

function delete_job(btn){
    var btn_id = btn.data("buttonid");
    console.log("click btn: ", btn_id);
    deleted_job_data ={
        "doc_id": btn_id
    }
    $.ajax({
        type: "POST",
        url: "delete_jobs",                
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(deleted_job_data),
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
}

$(document).ready(function(){
    displayJobs(all_jobs);
    $(".update_btn").click(function(){
        update($(this));
    });
    $(".delete_btn").click(function(){
        delete_job($(this));
    });
    $("#add_btn_in_view").click(function(){
        document.location.href = "/add_job"
    });
});