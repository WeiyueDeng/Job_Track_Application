from hashlib import new
from pydoc import doc
from tkinter import N
from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
import datetime
from datetime import date

app = Flask(__name__)

import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate("./advanced-web-362604-firebase-adminsdk-h1k4s-31cd581f8b.json")
default_app = initialize_app(cred)
db = firestore.client()
users_ref = db.collection(u'users')
plan_ref = db.collection(u'plan')
jobs_ref = db.collection(u'jobs')

if not plan_ref.document(u'Target_Num').get().exists:
    target_num = {
        u'target_num': None
    }
    plan_ref.document(u'Target_Num').set(target_num)
if not plan_ref.document(u'Deadline').get().exists:
    deadline = {
        u'deadline': None
    }
    plan_ref.document(u'Deadline').set(deadline)
if not plan_ref.document(u'Estimated_Daily_Task').get().exists:
    target_daily_task = {
        u'estimated_daily_task': None
    }
    plan_ref.document(u'Estimated_Daily_Task').set(target_daily_task)
if not plan_ref.document(u'Start_Date').get().exists:
    start_date = {
        u'start_date': None
    }
    plan_ref.document(u'Start_Date').set(start_date)
target_num_ref = plan_ref.document(u'Target_Num')
deadline_ref = plan_ref.document(u'Deadline')
estimated_daily_task_ref = plan_ref.document(u'Estimated_Daily_Task')
start_date_ref = plan_ref.document(u'Start_Date')


if not users_ref.document(u'users_states').get().exists:
    users_states = {
        u'current_Id': 1
    }
    users_ref.document(u'users_states').set(users_states)

# ROUTES
@app.route('/')
def home():
    global target_num_ref
    global deadline_ref
    global jobs_ref
    global start_date_ref

    cur_target_num = target_num_ref.get().to_dict()["target_num"]
    cur_deadline = deadline_ref.get().to_dict()["deadline"]
    print("cur_deadline homepage: ", type(cur_deadline), cur_deadline)
    date_deadline = datetime.datetime(cur_deadline.year, cur_deadline.month, cur_deadline.day)
    print("date_deadline homepage: ", type(date_deadline), date_deadline)
    view_deadline = date_deadline.strftime("%Y-%m-%d")
    print("view_deadline homepage: ", type(view_deadline), view_deadline)

    cur_start_date = start_date_ref.get().to_dict()["start_date"]
    print("cur_start_datehomepage: ", type(cur_start_date), cur_start_date)
    view_start_date = datetime.datetime(cur_start_date.year, cur_start_date.month, cur_start_date.day).strftime("%Y-%m-%d")

    plan_data = {
        "target_num": cur_target_num,
        "deadline": view_deadline,
        "start_date": view_start_date
    }

    today = datetime.datetime.today()
    print("Today's date homepage: ", type(today),today)
    applied_job_data={}
    
    cur_job_num = 0
    # daily_applied_job_num = len(list(jobs_ref.where(u"applied_date", u"==", today).stream()))
    daily_applied_job_num = 0
    if cur_start_date:
        date_start_date = datetime.datetime(cur_start_date.year,cur_start_date.month, cur_start_date.day)
        # cur_job_num = len(list(jobs_ref.where(u"applied_date", u">=", cur_start_date).stream()))
        all_jobs = jobs_ref.stream()
        for job in all_jobs:
            applied_date = job.to_dict()["applied_date"]
            date_applied_date =  datetime.datetime(applied_date.year,applied_date.month, applied_date.day)
            if date_applied_date >= date_start_date:
                cur_job_num+=1
            if date_applied_date.date() == today.date():
                daily_applied_job_num+=1

    print("cur jobs homepage: ", cur_job_num)
    applied_job_data["total_applied_job"]=cur_job_num

    days_left_data = {}
    if today < date_deadline:
        days_left_data["days_left"] = (date_deadline.date()-today.date()).days
    else:
        days_left_data["days_left"] = 0
    print("days left:", type(days_left_data["days_left"]), days_left_data["days_left"])

    daily_task_data ={}
    if days_left_data["days_left"] != 0:
        daily_task_data["target_daily_activity"] = estimated_daily_task_ref.get().to_dict()["estimated_daily_task"]
    else:
        daily_task_data["target_daily_activity"] = cur_target_num - cur_job_num
    print("target daily task: ", daily_task_data["target_daily_activity"])

    
    daily_task_data["daily_applied_job_num"] = daily_applied_job_num
    print("completed daily task: ", daily_task_data["daily_applied_job_num"])
    return render_template('home.html', plan = plan_data, applied_job_num = applied_job_data, days_left_data = days_left_data, daily_task_data = daily_task_data)

@app.route('/set_plan', methods=['GET', 'POST'])
def set_plan():
    global target_num_ref
    global deadline_ref
    global start_date_ref

    if request.method == 'GET':
        return render_template('set_plan.html')
    else:
        json_data = request.get_json()
        updated_target_num = json_data["target_num"]
        updated_deadline = json_data["deadline"]
        target_num_ref.update({u"target_num": int (updated_target_num)})

        converted_deadline = updated_deadline.split("-")
        date_deadline = datetime.datetime(int(converted_deadline[0]), int(converted_deadline[1]), int(converted_deadline[2]))
        print("deadline:", type(date_deadline), date_deadline)
        deadline_ref.update({u"deadline": date_deadline})
        today = datetime.datetime.today()
        print("Today's date:", type(today), today)
        start_date_ref.update({u"start_date": today})

        all_jobs = jobs_ref.stream()
        cur_job_num = 0
        for job in all_jobs:
            applied_date = job.to_dict()["applied_date"]
            date_applied_date =  datetime.datetime(applied_date.year,applied_date.month, applied_date.day)
            if date_applied_date.date() < today.date():
                cur_job_num+=1
        

        if today < date_deadline:
            days_left = (date_deadline.date()-today.date()).days
            print("days_left_set_plan:", days_left)
            jobs_left = int(updated_target_num)
            print("jobs_left_set_plan:", jobs_left)
            estimated_daily = jobs_left//(days_left+1)
            if jobs_left%(days_left+1) !=0:
                estimated_daily += 1
            estimated_daily_task_ref.update({u'estimated_daily_task': estimated_daily})
        else:
            jobs_left = updated_target_num - cur_job_num
            estimated_daily_task_ref.update({u'estimated_daily_task': jobs_left})
        response = {
            "response_status": "success"
        }
        return jsonify(response = response)
        

@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    global jobs_ref
    if request.method == 'GET':
        return render_template('add_job.html')
    else:
        new_job_json = request.get_json()
        position  = new_job_json["position"]
        company = new_job_json["company"]
        url = new_job_json["url"]
        status = new_job_json["status"]
        location = new_job_json["location"]
        applied_date = new_job_json["applied_date"].split("-")
        converted_applied_date = datetime.datetime(int (applied_date[0]), int (applied_date[1]), int (applied_date[2]))
        note = new_job_json["note"]

        # save new job in DB
        new_job_ref = jobs_ref.document()
        new_job_ref.set({
            "position": position,
            "company": company,
            "url": url,
            "status": status,
            "location": location,
            "applied_date": converted_applied_date,
            "note": note
        })
        response = {
            "response_status": "success"
        }
        return jsonify(response = response)

@app.route('/view_applied_jobs')
def view_jobs():
    global jobs_ref

    all_jobs = []
    jobs = jobs_ref.stream()
    for job in jobs:
        job_info = job.to_dict()
        job_info["doc_id"] = job.id
        print("doc_id: ", job.id)
        applied_date = job_info["applied_date"]
        date_applied_date = datetime.datetime(applied_date.year, applied_date.month, applied_date.day)
        view_applied_date = date_applied_date.strftime("%Y-%m-%d")
        job_info["applied_date"] = view_applied_date
        all_jobs.append(job_info)
    return render_template('view_applied_jobs.html', all_jobs = all_jobs)

@app.route('/view_applied_jobs/<id>')
def edit_jobs(id=None):
    global jobs_ref
    job_data = jobs_ref.document(id).get().to_dict()
    applied_date = job_data["applied_date"]
    date_applied_date = datetime.datetime(applied_date.year, applied_date.month, applied_date.day)
    view_applied_date = date_applied_date.strftime("%Y-%m-%d")
    job_data["applied_date"] = view_applied_date

    return render_template('view_a_job_item.html', job_data = job_data, job_id = id)    

@app.route('/update_jobs', methods = ['POST'])
def update_jobs():
    global jobs_ref
    update_job_data = request.get_json()
    print("update_jobs", update_job_data)
    update_doc_id = update_job_data["doc_id"]
    update_job_info = update_job_data["update_job_data"]

    applied_date = update_job_info["applied_date"].split("-")
    date_applied_date = datetime.datetime(int (applied_date[0]), int (applied_date[1]),int (applied_date[2]))
    update_job_info["applied_date"] = date_applied_date
    jobs_ref.document(update_doc_id).update(update_job_info)
    response = {
            "response_status": "success"
    }
    return jsonify(response = response)

@app.route('/delete_jobs', methods = ['POST'])
def delete_jobs():
    global jobs_ref
    deleted_job_data = request.get_json()
    deleted_doc_id = deleted_job_data["doc_id"]
    jobs_ref.document(deleted_doc_id).delete()
    response = {
            "response_status": "success"
    }
    return jsonify(response = response)

@app.route('/create', methods=['GET', 'POST'] )
def create():

    if request.method == 'GET':
        return render_template('create.html')   
    else:
        json_data = request.get_json()

        first_name = json_data["first_name"]
        last_name = json_data["last_name"]

        current_users_states = users_ref.document(u'users_states').get()
        current_id = current_users_states.to_dict()["current_Id"]
        new_doc_name = "user" + str(current_id)
        new_doc_data = {
            'id': current_id,
            'first_name' : first_name,
            'last_name': last_name
        }
        #add data
        users_ref.document(new_doc_name).set(new_doc_data)
        #update user states
        users_ref.document(u'users_states').set({"current_Id": current_id+1})
        response = {
            "response_status": "success"
        }
        return jsonify(response = response)

@app.route('/read')
def read():
    #all current users' doc
    global users_ref
    
    current_users_states = users_ref.document("users_states").get()
    current_id= current_users_states.to_dict()["current_Id"]

    all_users = []
    for i in range(1, current_id):
        target_doc_name = "user" + str(i)
        if users_ref.document(target_doc_name).get().exists:
            target_doc = users_ref.document(target_doc_name).get().to_dict()
            all_users.append(target_doc)

    return render_template('read.html', data = all_users)

@app.route('/update', methods= ["GET","POST"])
def update():
    #all current users' doc
    global users_ref
    if request.method == "GET":
        current_users_states = users_ref.document("users_states").get()
        current_id= current_users_states.to_dict()["current_Id"]

        all_users = []
        for i in range(1, current_id):
            target_doc_name = "user" + str(i)
            if users_ref.document(target_doc_name).get().exists:
                target_doc = users_ref.document(target_doc_name).get().to_dict()
                all_users.append(target_doc)

        return render_template('update.html', data = all_users) 
    else:
        json_data = request.get_json()
        user_id = json_data["id"]
        updated_first_name = json_data["first_name"]
        updated_last_name = json_data["last_name"]
        doc_name = "user" + str(user_id)
        print("doc_name", doc_name)
        new_data = {
            "id": user_id,
            "first_name": updated_first_name,
            "last_name" : updated_last_name
        }
        print("new_data", new_data)
        users_ref.document(doc_name).set(new_data)

        #get current db info
        current_users_states = users_ref.document("users_states").get()
        current_id= current_users_states.to_dict()["current_Id"]
        
        all_users = []
        for i in range(1, current_id):
            target_doc_name = "user" + str(i)
            if users_ref.document(target_doc_name).get().exists:
                target_doc = users_ref.document(target_doc_name).get().to_dict()
                all_users.append(target_doc)
        print("all users", all_users)
        return jsonify(data = all_users) 

@app.route('/delete',  methods=['GET', 'POST'])
def delete():
    #all current users' doc
    global users_ref
    if request.method == "GET":
        current_users_states = users_ref.document("users_states").get()
        current_id= current_users_states.to_dict()["current_Id"]

        all_users = []
        for i in range(1, current_id):
            target_doc_name = "user" + str(i)
            if users_ref.document(target_doc_name).get().exists:
                target_doc = users_ref.document(target_doc_name).get().to_dict()
                all_users.append(target_doc)
        return render_template('delete.html', data = all_users)
    else:
        json_data = request.get_json()
        user_id = json_data["id"]
        doc_name = "user" +str(user_id)
        #delete the doc
        users_ref.document(doc_name).delete()
        #get the current db info
        current_users_states = users_ref.document("users_states").get()
        current_id= current_users_states.to_dict()["current_Id"]

        all_users = []
        for i in range(1, current_id):
            target_doc_name = "user" + str(i)
            if users_ref.document(target_doc_name).get().exists:
                target_doc = users_ref.document(target_doc_name).get().to_dict()
                all_users.append(target_doc)
        return jsonify(data = all_users)


@app.route('/hello/<name>')
def hello_name(name=None):
    return render_template('hello_name.html', name=name) 


@app.route('/people')
def people():
    return render_template('people.html', data=data)  


# AJAX FUNCTIONS

# ajax for people.js
@app.route('/add_name', methods=['GET', 'POST'])
def add_name():
    global data 
    global current_id 

    json_data = request.get_json()   
    name = json_data["name"] 
    
    # add new entry to array with 
    # a new id and the name the user sent in JSON
    current_id += 1
    new_id = current_id 
    new_name_entry = {
        "name": name,
        "id":  current_id
    }
    data.append(new_name_entry)

    #send back the WHOLE array of data, so the client can redisplay it
    return jsonify(data = data)
 


if __name__ == '__main__':
   app.run(debug = True)




