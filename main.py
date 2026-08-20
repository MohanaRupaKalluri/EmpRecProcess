import hashlib
import os
from datetime import datetime, timedelta

from flask import Flask, redirect, render_template, session, request
import pymongo
import secrets
from bson import ObjectId

from flask import Flask
from pymongo import MongoClient

from db import get_database

app = Flask(__name__)

# Flask session secret: from the environment, else a random per-process key.
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(16)

# Database: a real MongoDB when MONGO_URI is set, otherwise an embedded
# demo store seeded on startup (see db.py). No credentials in source code.
client, EmpRecCluster, DEMO_MODE = get_database()
admin_collection = EmpRecCluster["admin"]
companies_collection = EmpRecCluster["companies"]
recruiter_collection = EmpRecCluster["recruiter"]
seeker_collection = EmpRecCluster["seeker"]
skill_collection = EmpRecCluster["skill_collection"]
job_post_collection = EmpRecCluster["job_post"]
job_application_collection = EmpRecCluster["job_application"]
interview_collection = EmpRecCluster["interview"]

APP_ROOT = os.path.dirname(os.path.abspath(__file__))




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin_login")
def admin_login():
    message = request.args.get("message")
    if message == None:
        message = ""
    return render_template("admin_login.html", message=message)


@app.route("/admin_login_action",methods=['post'])
def aLogin1():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == 'admin' and password == 'admin':
        session['role'] = 'admin'
        return render_template("admin_home.html", username=username)
    else:
        return redirect("/admin_login?message=Invalid login details")




@app.route("/admin_home")
def admin_home():
    return render_template("/admin_home.html")



@app.route("/add_skill")
def add_skill():
    skills = skill_collection.find()
    message = request.args.get("message")
    if message == None:
        message = ""
    return render_template("add_skill.html",skills=skills,message=message)


@app.route("/add_skill_action",methods=['post'])
def add_skill_action():
    skill_name = request.form.get("skill_name")
    query = {"$or":[{"skill_name":skill_name}]}
    count = skill_collection.count_documents(query)
    if count > 0:
        return redirect("/add_skill?message=Duplicate Email Address")
    else:
        skill_collection.insert_one({"skill_name": skill_name})
        return redirect("/add_skill?message=Skill Added Successfully")


@app.route("/edit_skill")
def edit_skill():
    skill_id = request.args.get("skill_id")
    print(skill_id)
    return render_template("edit_skill.html",skill_id=skill_id)


@app.route("/edit_skill_action")
def edit_skill_action():
    skill_id = request.args.get("skill_id")
    skill_name = request.args.get("skill_name")
    query = {"_id": ObjectId(skill_id)}
    query2 = {"$set":{"skill_name":skill_name}}
    skill_collection.update_one(query, query2)
    print(query2)
    return redirect("/add_skill")


@app.route("/company_login")
def company_login():
    message = request.args.get("message")
    if message == None:
        message = ""
    return render_template("company_login.html", message=message)


@app.route("/company_login_action", methods=['post'])
def company_login_action():
    email = request.form.get("email")
    password = request.form.get("password")
    query = {"email": email, "password": password}
    total_count = companies_collection.count_documents(query)
    if total_count > 0:
        company = companies_collection.find_one(query)
        if company['status'] == 'Not Verified':
            return redirect("/company_login?message=Your Account Not Verified")
        else:
            session['company_id'] = str(company['_id'])
            session['role'] = 'company'
            return redirect("/company_home")
    else:
        return redirect("/company_login?message=Invalid Login Details")


@app.route("/company_home")
def company_home():
    return render_template("/company_home.html")

@app.route("/company_registration")
def company_registration():
    message = request.args.get("message")
    if message == None:
        message = ""
    return render_template("company_registration.html", message=message)

@app.route("/company_registration_action", methods=['post'])
def company_registration_action():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    zipcode = request.form.get("zipcode")
    city = request.form.get("city")
    state = request.form.get("state")
    address = request.form.get("address")
    password = request.form.get("password")
    password2 = request.form.get("password2")
    if password != password2:
        return redirect("/company_registration?message=confirm password and password must be same")
    password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    about = request.form.get("about")
    status = "Not Verified"
    query = {"email": email}
    count = companies_collection.count_documents(query)
    if count > 0:
        return redirect("/company_registration?message=Duplicate Email Address")
    query = {"phone": phone}
    count = companies_collection.count_documents(query)
    if count > 0:
        return redirect("/company_registration?message=Duplicate Phone Number")
    query = {"first_name": first_name, "last_name":last_name, "address":address,"zipcode":zipcode,"city":city,"state":state, "email": email, "phone": phone, "password": password,"password2": password_hash, "about":about,"status": status}
    companies_collection.insert_one(query)
    return redirect("/company_registration?message=Company Registered Successfully")


@app.route("/view_companies")
def view_companies():
    query = {}
    companies= companies_collection.find(query)
    companies = list(companies)
    print(list(companies))
    return render_template("view_companies.html", companies=companies)




@app.route("/recruiter_login")
def recruiter_login():
    message = request.args.get("message")
    if message == None:
        message = ""
    return render_template("recruiter_login.html", message=message)


@app.route("/recruiter_login_action", methods=['post'])
def recruiter_login_action():
    email = request.form.get("email")
    password = request.form.get("password")
    query = {"email": email, "password": password}
    total_count = recruiter_collection.count_documents(query)
    if total_count > 0:
        recruiter = recruiter_collection.find_one(query)
        session['recruiter_id'] = str(recruiter['_id'])
        session['role'] = 'recruiter'
        return redirect("/recruiter_home")
    else:
        return render_template("msg.html", msg="Invalid login Details")



@app.route("/recruiter_home")
def recruiter_home():
    return render_template("/recruiter_home.html")


@app.route("/recruiter_registration")
def recruiter_registration():
    message = request.args.get("message")
    if message == None:
        message = ""
    return render_template("recruiter_registration.html", message=message)

@app.route("/recruiter_registration_action", methods=['post'])
def recruiter_registration_action():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    zipcode = request.form.get("zipcode")
    city = request.form.get("city")
    state = request.form.get("state")
    address = request.form.get("address")
    password = request.form.get("password")
    password2 = request.form.get("password2")
    if password != password2:
        return redirect("/company_registration?message=confirm password and password must be same")
    password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    experience = request.form.get("experience")
    status = "Not Verified"
    query = {"email": email}
    count = recruiter_collection.count_documents(query)
    if count > 0:
        return redirect("/recruiter_registration?message=Duplicate Email Address")

    query = {"phone": phone}
    count = recruiter_collection.count_documents(query)
    if count > 0:
        return redirect("/recruiter_registration?message=Duplicate Phone Number")

    query = {"first_name":first_name,"last_name":last_name,"zipcode":zipcode,"city":city,"address":address,"experience":experience,"password2":password_hash,"state":state, "email":email, "phone":phone, "password":password, "status":status}
    recruiter_collection.insert_one(query)
    return redirect("/recruiter_registration?message=Recruiter Registered Successfully")


@app.route("/seeker_login")
def seeker_login():
    message = request.args.get("message")
    if message == None:
        message = ""
    return render_template("seeker_login.html", message=message)

@app.route("/seeker_login_action", methods=['post'])
def seeker_login_action():
    email = request.form.get("email")
    password = request.form.get("password")
    query = {"email": email, "password": password}
    total_count = seeker_collection.count_documents(query)
    if total_count > 0:
        seeker = seeker_collection.find_one(query)
        session['seeker_id'] = str(seeker['_id'])
        session['role'] = 'seeker'
        return redirect("/seeker_home")
    else:
        return redirect("/seeker_login?message=Invalid Login Details")


@app.route("/seeker_home")
def seeker_home():
    return render_template("/seeker_home.html")


@app.route("/seeker_registration")
def seeker_registration():
    skill_id = request.form.get("skill_id")
    skills = skill_collection.find({})
    message = request.args.get("message")
    if message == None:
        message = ""
    return render_template("/seeker_registration.html", message=message,skills=skills,skill_id=skill_id)


@app.route("/seeker_registration_action", methods=['post'])
def seeker_registration_action():
    skill_id = request.form.getlist("skill_id")
    skill_ids = []
    for id in skill_id:
        skill_ids.append({"skill_id":ObjectId(id)})
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    zipcode = request.form.get("zipcode")
    city = request.form.get("city")
    state = request.form.get("state")
    address = request.form.get("address")
    expert_technology = request.form.get("expert_technology")
    resumes = request.files.getlist("resume")
    resumes2 = []
    if resumes:
        for resume in resumes:
            path = APP_ROOT + "/static/Resumes/" + resume.filename
            resume.save(path)
            resumes2.append(resume.filename)
    else:
        return render_template("msg2.html", msg="Please upload a resume.")
    password = request.form.get("password")
    password2 = request.form.get("password2")
    if password != password2:
        return redirect("/company_registration?message=confirm password and password must be same")
    password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    cover_letter = request.form.get("cover_letter")
    work_experience = request.form.get("work_experience")
    qualifications = []
    number_of_qualifications = request.form.get("number_of_qualifications")
    print(number_of_qualifications)
    for i in range(1, int(number_of_qualifications)+1):
        degree = request.form.get("degree" + str(i))
        institute = request.form.get("institute" + str(i))
        year_of_graduation = request.form.get("year_of_graduation" + str(i))
        qualification = {"degree": degree, "institute": institute,"year_of_graduation":year_of_graduation}
        qualifications.append(qualification)
    if seeker_collection.count_documents({"email": email}) > 0:
        return redirect("/seeker_registration?message=Duplicate Email Address")
    if seeker_collection.count_documents({"phone": phone}) > 0:
        return redirect("/seeker_registration?message=Duplicate Phone Number")
    query = {"first_name":first_name, "last_name":last_name, "email":email,"city":city,"expert_technology":expert_technology,"zipcode":zipcode,"state":state,"address":address, "phone":phone, "password":password,"password2":password_hash,"cover_letter":cover_letter, "work_experience":work_experience,"skills": skill_ids,"qualifications":qualifications,"resumes":resumes2}
    seeker_collection.insert_one(query)
    return redirect("/seeker_registration?message=Seeker Registered Successfully")


@app.route("/edit_seeker_profile")
def edit_seeker_profile():
        seeker_id = request.args.get("seeker_id")
        seeker = seeker_collection.find_one({"_id": ObjectId(seeker_id)})
        skills = skill_collection.find({})
        return render_template("edit_seeker_profile.html", seeker=seeker, skills=skills)


@app.route("/edit_seeker_profile_action", methods=['post'])
def edit_seeker_profile_action():
    seeker_id = request.form.get("seeker_id")
    skill_ids = [
        {"skill_id": ObjectId(skill_id)}
        for skill_id in request.form.getlist("skill_id")
    ]
    updated_data = {
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
        "email": request.form.get("email"),
        "phone": request.form.get("phone"),
        "zipcode": request.form.get("zipcode"),
        "city": request.form.get("city"),
        "state": request.form.get("state"),
        "address": request.form.get("address"),
        "work_experience": request.form.get("work_experience"),
        "expert_technology": request.form.get("expert_technology"),
        "cover_letter": request.form.get("cover_letter"),
        "skills": skill_ids,
    }

    # Handle Resume Upload
    resume = request.files.get("resume")
    if resume:
        resume_path = APP_ROOT + "/static/Resumes/" + resume.filename
        resume.save(resume_path)
        updated_data["resume"] = resume.filename

    seeker_collection.update_one({"_id": ObjectId(seeker_id)}, {"$set": updated_data})
    return redirect(f"/profile?seeker_id={seeker_id}&message=Profile Updated Successfully")

@app.route("/add_qualification")
def add_qualification():
    seeker_id = request.args.get("seeker_id")
    return render_template("add_qualification.html",seeker_id=seeker_id)

@app.route("/add_qualification_action", methods=['POST'])
def add_qualification_action():
    seeker_id = request.form.get("seeker_id")
    degree = request.form.get("degree")
    institute = request.form.get("institute")
    year_of_graduation = request.form.get("year_of_graduation")

    new_qualification = {
        "degree": degree,
        "institute": institute,
        "year_of_graduation": year_of_graduation
    }

    query = {"$push": {"qualifications": new_qualification}}
    seeker_collection.update_one({"_id": ObjectId(seeker_id)}, query)
    return redirect("/profile")


@app.route("/profile")
def profile():

    if session['role'] == 'company':
        seeker_id = request.args.get("seeker_id")
        query = {"_id": ObjectId(seeker_id)}
        seekers = seeker_collection.find({"_id": ObjectId(seeker_id)})
    elif session['role'] == 'seeker':
        seeker_id = session['seeker_id']
        query = {"_id": ObjectId(seeker_id)}
        seekers = seeker_collection.find(query)
    return render_template("/profile.html",seekers=seekers,get_skill_by_skill_id=get_skill_by_skill_id)

def get_skill_by_skill_id(skill_id):
    query = {"_id": skill_id}
    skill = skill_collection.find_one(query)
    return skill

@app.route("/job_post")
def job_post():
    recruiter_id = request.form.get("recruiter_id")
    recruiters = recruiter_collection.find({})
    return render_template("/job_post.html",recruiters=recruiters,recruiter_id=recruiter_id)


@app.route("/job_post_action", methods=['POST'])
def job_post_action():
    company_id = session['company_id']
    job_title = request.form.get("job_title")
    job_description = request.form.get("job_description")
    job_type = request.form.get("job_type")
    no_of_openings = request.form.get("no_of_openings")
    skill_required = request.form.get("skill_required")
    location = request.form.get("location")
    post_date = request.form.get("post_date")
    post_date = datetime.strptime(post_date, "%Y-%m-%d")
    last_date = request.form.get("last_date")
    last_date = datetime.strptime(last_date, "%Y-%m-%d")
    status = 'Not Selected'
    query = {"no_of_openings":no_of_openings,"company_id": ObjectId(company_id), "job_title": job_title, "job_description": job_description,"job_type": job_type, "skill_required": skill_required, "location": location, "post_date": post_date,"last_date": last_date,"status":status}
    job_post_collection.insert_one(query)
    return render_template("msg2.html", msg="Job Post added successfully")

@app.route("/activate_company")
def activate_company():
    company_id = request.args.get("company_id")
    query = {"_id":ObjectId(company_id)}
    query2 = {"$set":{"status":"Verified"}}
    companies_collection.update_one(query, query2)
    return redirect("/view_companies")


@app.route("/deactivated_company")
def deactivated_company():
    company_id = request.args.get("company_id")
    query = {"_id":ObjectId(company_id)}
    query2 = {"$set":{"status":"Not Verified"}}
    companies_collection.update_one(query, query2)
    return redirect("/view_companies")

@app.route("/view_job_post")
def view_job_post():
    query = {}
    if session['role']=='company':
        query = {"company_id":ObjectId(session['company_id'])}
    elif session['role']=='recruiter':
        query = {"status": "Not Selected"}
    elif session['role']=='seeker':
        query = {"status": "Selected"}
    search_query = request.args.get('search', '').strip()
    if search_query:
        query["$or"] = [
            {"job_title": {"$regex": search_query, "$options": "i"}},
            {"job_type": {"$regex": search_query, "$options": "i"}},
            {"skill_required": {"$regex": search_query, "$options": "i"}}
        ]
    job_posts = job_post_collection.find(query)
    date = datetime.now()
    return render_template("view_job_post.html",job_posts=job_posts,date=date,get_is_job_applied=get_is_job_applied,job_post_count=job_post_count)

def job_post_count(job_post_id):
    count = job_application_collection.count_documents({"job_post_id": ObjectId(job_post_id), "seeker_id": ObjectId(session['seeker_id'])})
    return count
def get_is_job_applied(job_post_id):
    count = job_application_collection.count_documents({"job_post_id":ObjectId(job_post_id),"seeker_id":ObjectId(session['seeker_id'])})
    return count

@app.route("/view_my_job")
def view_my_job():
    recruiter_id = session['recruiter_id']
    job_posts = job_post_collection.find({"recruiter_id":ObjectId(recruiter_id)})
    return render_template("view_my_job.html",job_posts=job_posts)


@app.route("/select_to_recruit")
def select_to_recruit():
    recruiter_id = session['recruiter_id']
    job_post_id = request.args.get("job_post_id")
    query1 = {"_id": ObjectId(job_post_id)}
    query2 = {"$set": {"status": "Selected", "recruiter_id": ObjectId(recruiter_id)}}
    job_post_collection.update_one(query1, query2)
    return render_template("msg2.html", msg="Select successfully To Recruit")


def get_recruiter_by_recruiter_id(recruiter_id):
    recruiter = recruiter_collection.find_one({'_id':ObjectId(recruiter_id)})
    return recruiter


@app.route("/apply_job", methods=['POST'])
def apply_job():
    job_post_id = request.form.get("job_post_id")
    seeker_id = session['seeker_id']
    resume = request.files.get("resume")
    if resume:
        path = APP_ROOT + "/static/Resumes/" + resume.filename
        resume.save(path)
    else:
        return render_template("msg2.html", msg="Please upload a resume.")
    query = job_application_collection.find_one({"job_post_id": ObjectId(job_post_id),"seeker_id": ObjectId(seeker_id)})
    if query:
        return render_template("msg2.html", msg="You have already applied for this job.")
    status = "Applied"
    date = datetime.now().strftime("%m-%d-%Y %I:%M %p")
    query1 = {"job_post_id": ObjectId(job_post_id),"seeker_id": ObjectId(seeker_id),"status": status,"date": date,"resume": resume.filename}
    job_application_collection.insert_one(query1)
    job_candidates = {"seeker_id":ObjectId(seeker_id),"status":status,"applied_date":date}
    job_post_collection.update_one({"_id":job_post_id},{"$push":{"job_candidates":job_candidates}})
    return render_template("msg2.html", msg="Job Applied Successfully")


@app.route("/view_applications")
def view_applications():
    query = {}
    if session['role'] == 'seeker':
        job_post_id = request.args.get("job_post_id")
        if job_post_id == None:
            query = {"seeker_id": ObjectId(session['seeker_id'])}
        else:
            query = {"job_post_id": ObjectId(job_post_id)}
    elif session['role'] == 'recruiter':
        job_post_id = request.args.get("job_post_id")

        if job_post_id == None:
            job_posts = job_post_collection.find({"recruiter_id": ObjectId(session['recruiter_id'])})
            job_posts_ids = []
            for job_post in job_posts:
                print(job_post)
                job_posts_ids.append({"job_post_id": ObjectId(job_post['_id'])})
            query = {"$or":job_posts_ids }
        else:
            query = {"job_post_id": ObjectId(job_post_id)}
    job_applications = job_application_collection.find(query)
    # print(job_applications)
    return render_template("/view_applications.html",job_applications=job_applications,get_seeker_by_seeker_id=get_seeker_by_seeker_id,get_job_post_by_job_post_id=get_job_post_by_job_post_id, get_recruiter_by_recruiter_id=get_recruiter_by_recruiter_id,get_company_by_company_id=get_company_by_company_id)


def get_seeker_by_seeker_id(seeker_id):
    seeker = seeker_collection.find_one({'_id':ObjectId(seeker_id)})
    return seeker

def get_job_post_by_job_post_id(job_post_id):
    job_post = job_post_collection.find_one({'_id':ObjectId(job_post_id)})
    return job_post

def get_company_by_company_id(company_id):
    company = companies_collection.find_one({'_id':ObjectId(company_id)})
    return company


@app.route("/drop_application")
def drop_application():
    job_application_id = ObjectId(request.args.get("job_application_id"))
    query = {"_id":ObjectId(job_application_id)}
    query2 ={"$set":{"status":"Dropped"}}
    job_application_collection.update_one(query,query2)
    return redirect("/view_applications")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/schedule_interview")
def schedule_interview():
    job_application_id = request.args.get("job_application_id")
    job_applications = job_application_collection.find_one({})
    return render_template("/schedule_interview.html",job_application_id=job_application_id,job_applications=job_applications)


@app.route("/schedule_interview_action", methods=['POST'])
def schedule_interview_action():
    job_application_id = request.form.get("job_application_id")
    interview_date_time = request.form.get("Interview_date_time")
    feedback = request.form.get("feedback")
    interview_date_time1 = datetime.strptime(interview_date_time, "%Y-%m-%dT%H:%M")
    interview_date_time2 = interview_date_time1.strftime("%m-%d-%Y %I:%M %p")
    date = datetime.now().strftime("%m-%d-%Y %I:%M %p")
    number_of_interview_rounds = request.form.get("number_of_interview_rounds")
    end_date = interview_date_time1 + timedelta(days=4)
    interview_types = []
    for i in range(1, int(number_of_interview_rounds) + 1):
        round_name = request.form.get("round_name" + str(i))
        print(round_name)
        interview_types.append(round_name)
    interview_collection.insert_one({
        "job_application_id": ObjectId(job_application_id),
        "Interview_types": interview_types,
        "Interview_date_time": interview_date_time2,
        "date": date,
        "end_date":end_date,
        "status": "Interview Scheduled",
        "feedback": feedback
    })
    query = {"_id": ObjectId(job_application_id)}
    update = {"$set": {"status": "Selected For Interview"}}
    job_application_collection.update_one(query, update)
    return render_template("msg2.html", msg="Interview scheduled successfully")


@app.route("/view_interview_schedule")
def view_interview_schedule():
    job_application_id = request.args.get("job_application_id")
    interviews = interview_collection.find({"job_application_id":ObjectId(job_application_id)})
    return render_template("/view_interview_schedule.html",interviews=interviews,job_application_id=job_application_id,is_interview_expired=is_interview_expired)

def is_interview_expired(end_date,interview_id):
    cur_date = datetime.now()
    diff = end_date - cur_date
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if days <1:
        count = interview_collection.count_documents({"_id":ObjectId(interview_id),"status":'Interview Scheduled'})
        if count>0:
            interview_collection.update_one({'_id':ObjectId(interview_id)},{"$set":{"status":'Rejected'}})
    return 0

@app.route("/update_request_status")
def update_request_status():
    status = request.args.get("status")
    job_application_id = request.args.get("job_application_id")
    query1 = {"_id": ObjectId(job_application_id)}
    query2 = {"$set": {"status": status}}
    job_application_collection.update_one(query1, query2)
    return redirect("/view_applications")

@app.route("/accept_interview")
def accept_interview():
    job_application_id = request.args.get("job_application_id")
    interview_id = request.args.get("interview_id")
    query1 = {"_id": ObjectId(interview_id)}
    query2 = {"$set": {"status": 'Accepted'}}
    interview_collection.update_one(query1, query2)
    return redirect("/view_interview_schedule?job_application_id="+str(job_application_id))


@app.route("/reject_interview")
def reject_interview():
    job_application_id = request.args.get("job_application_id")
    interview_id = request.args.get("interview_id")
    query1 = {"_id": ObjectId(interview_id)}
    query2 = {"$set": {"status": 'Rejected'}}
    interview_collection.update_one(query1, query2)
    return redirect("/view_interview_schedule?job_application_id="+str(job_application_id))


@app.route("/start_interview")
def start_interview():
    job_application_id = request.args.get("job_application_id")
    interview_id = request.args.get("interview_id")
    query1 = {"_id": ObjectId(interview_id)}
    query2 = {"$set": {"status": 'Interview Started'}}
    interview_collection.update_one(query1, query2)
    return redirect("/view_interview_schedule?job_application_id="+str(job_application_id))

@app.route("/selected")
def selected():
    interview_id = request.args.get("interview_id")
    # job_application_id = request.args.get("job_application_id")
    query1 = {"_id": ObjectId(interview_id)}
    query2 = {"$set": {"status": 'Mark As Selected'}}
    interview_collection.update_one(query1, query2)
    interview = interview_collection.find_one({"_id":ObjectId(interview_id),"status": 'Mark As Selected'})
    job_application_id = interview['job_application_id']
    job_application = job_application_collection.find_one({"_id": ObjectId(job_application_id)})
    seeker_id = job_application['seeker_id']
    job_post_id = job_application['job_post_id']
    candidate_details = {
        "seeker_id": ObjectId(seeker_id),
        "status": "Mark As Selected",
        "date": datetime.now().strftime("%Y-%m-%d %I:%M %p")
    }
    query3 = {"_id": ObjectId(job_post_id)}
    query4 = {"$push": {"job_candidates": candidate_details}}
    job_post_collection.update_one(query3, query4)
    return redirect("/view_interview_schedule?job_application_id="+str(job_application_id))


@app.route("/rejected")
def rejected():
    job_application_id = request.args.get("job_application_id")
    interview_id = request.args.get("interview_id")
    query1 = {"_id": ObjectId(interview_id)}
    query2 = {"$set": {"status": 'Rejected For Job'}}
    interview_collection.update_one(query1, query2)
    return redirect("/view_interview_schedule?job_application_id="+str(job_application_id))


@app.route("/view_job_candidates")
def view_job_candidates():
    job_post_id = request.args.get("job_post_id")
    job_posts = job_post_collection.find({"_id":ObjectId(job_post_id)})
    return render_template("view_job_candidates.html",job_posts=job_posts,get_seeker_by_seeker_id=get_seeker_by_seeker_id)


@app.route("/selected_for_job")
def selected_for_job():
    job_post_id = request.args.get("job_post_id")
    seeker_id =  request.args.get("seeker_id")
    query1 = {"_id": ObjectId(job_post_id), "job_candidates.seeker_id": ObjectId(seeker_id)}
    query2 = {"$set": {"job_candidates.$.status": "Selected For job"}}
    job_post_collection.update_one(query1, query2)
    job_application = job_application_collection.find_one({"job_post_id":ObjectId(job_post_id),"seeker_id":ObjectId(seeker_id)})
    query3 = {"$set":{"status":'Selected For job'}}
    job_application_collection.update_one({"_id":ObjectId(job_application['_id'])},query3)
    interview_collection.update_one({"job_application_id":ObjectId(job_application['_id'])},{"$set":{"status":'Selected For job'}})
    return redirect("/view_job_candidates?job_post_id="+str(job_post_id))


@app.route("/Reject_for_job")
def Reject_for_job():
    job_post_id = request.args.get("job_post_id")
    seeker_id =  request.args.get("seeker_id")
    query1 = {"_id": ObjectId(job_post_id), "job_candidates.seeker_id": ObjectId(seeker_id)}
    query2 = {"$set": {"job_candidates.$.status": "Rejected For job"}}
    job_post_collection.update_one(query1, query2)
    job_application = job_application_collection.find_one({"job_post_id":ObjectId(job_post_id),"seeker_id":ObjectId(seeker_id)})
    query3 = {"$set":{"status":'Rejected For job'}}
    job_application_collection.update_one({"_id":ObjectId(job_application['_id'])},query3)
    interview_collection.update_one({"job_application_id":ObjectId(job_application['_id'])},{"$set":{"status":'Rejected For job'}})
    return redirect("/view_job_candidates?job_post_id="+str(job_post_id))







#app.run(debug=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

