"""Production entrypoint.

Loads the Flask app from main.py and overrides the database connection and
session secret with environment variables, so no credentials are needed in
source code. Used by Docker / Koyeb / Hugging Face Spaces / Render:

    gunicorn wsgi:app
"""

import os

from pymongo import MongoClient

import main

MONGO_URI = os.environ.get("MONGO_URI")
if MONGO_URI:
    client = MongoClient(MONGO_URI)
    db = client[os.environ.get("MONGO_DB", "EmpRecCluster")]
    main.client = client
    main.EmpRecCluster = db
    main.admin_collection = db["admin"]
    main.companies_collection = db["companies"]
    main.recruiter_collection = db["recruiter"]
    main.seeker_collection = db["seeker"]
    main.skill_collection = db["skill_collection"]
    main.job_post_collection = db["job_post"]
    main.job_application_collection = db["job_application"]
    main.interview_collection = db["interview"]

SECRET_KEY = os.environ.get("SECRET_KEY")
if SECRET_KEY:
    main.app.secret_key = SECRET_KEY

app = main.app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))
