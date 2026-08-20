"""Database bootstrap.

Two modes, chosen automatically:

1. If MONGO_URI is set in the environment, connect to that real MongoDB.
2. Otherwise fall back to an embedded, in-process MongoDB-compatible store
   (mongomock) that is seeded with demo data on startup.

Mode 2 means the app runs anywhere -- laptop, Docker, Hugging Face Spaces --
with zero configuration and no external database, which is what the public
demo deployment uses. No credentials live in source code.
"""

import hashlib
import os
from datetime import datetime, timedelta


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_database():
    """Return (client, db, is_demo)."""
    mongo_uri = os.environ.get("MONGO_URI")
    if mongo_uri:
        from pymongo import MongoClient

        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        return client, client[os.environ.get("MONGO_DB", "EmpRecCluster")], False

    import mongomock

    client = mongomock.MongoClient()
    db = client["EmpRecCluster"]
    seed_demo_data(db)
    return client, db, True


def seed_demo_data(db):
    """Populate the embedded store with a realistic demo dataset."""
    if db["companies"].count_documents({}) > 0:
        return

    skills = [
        "Python", "SQL", "Apache Spark", "Airflow", "AWS", "Azure",
        "React", "Java", "Kubernetes", "Machine Learning",
    ]
    skill_ids = [
        db["skill_collection"].insert_one({"skill_name": s}).inserted_id
        for s in skills
    ]

    companies = [
        {
            "first_name": "Northwind", "last_name": "Analytics",
            "email": "hr@northwind.example", "phone": "9000000001",
            "address": "500 Market St", "zipcode": "94105",
            "city": "San Francisco", "state": "CA",
            "password": "demo123", "password2": _hash("demo123"),
            "about": "Cloud data platform company hiring data and ML engineers.",
            "status": "Verified",
        },
        {
            "first_name": "Blue Harbor", "last_name": "Retail",
            "email": "careers@blueharbor.example", "phone": "9000000002",
            "address": "12 Commerce Ave", "zipcode": "60601",
            "city": "Chicago", "state": "IL",
            "password": "demo123", "password2": _hash("demo123"),
            "about": "National retailer modernising its supply chain analytics.",
            "status": "Verified",
        },
    ]
    company_ids = [db["companies"].insert_one(c).inserted_id for c in companies]

    recruiters = [
        {
            "first_name": "Priya", "last_name": "Nair",
            "email": "recruiter@demo.com", "phone": "9000000010",
            "address": "88 Hiring Lane", "zipcode": "94105",
            "city": "San Francisco", "state": "CA", "experience": "6",
            "password": "demo123", "password2": _hash("demo123"),
            "status": "Verified",
        },
    ]
    for r in recruiters:
        db["recruiter"].insert_one(r)

    seekers = [
        {
            "first_name": "Arjun", "last_name": "Rao",
            "email": "seeker@demo.com", "phone": "9000000020",
            "address": "4 Candidate Rd", "zipcode": "73301",
            "city": "Austin", "state": "TX",
            "expert_technology": "Data Engineering",
            "password": "demo123", "password2": _hash("demo123"),
            "cover_letter": "Data engineer with 4 years building batch and streaming pipelines.",
            "work_experience": "4 years",
            "skills": [str(skill_ids[0]), str(skill_ids[1]), str(skill_ids[2])],
            "qualifications": [
                {"degree": "M.S. Computer Science", "institute": "UT Austin", "year_of_graduation": "2023"},
            ],
            "resumes": [],
        },
        {
            "first_name": "Meera", "last_name": "Shah",
            "email": "seeker2@demo.com", "phone": "9000000021",
            "address": "19 Applicant Way", "zipcode": "10001",
            "city": "New York", "state": "NY",
            "expert_technology": "Full Stack Development",
            "password": "demo123", "password2": _hash("demo123"),
            "cover_letter": "Full stack engineer focused on React and cloud APIs.",
            "work_experience": "3 years",
            "skills": [str(skill_ids[6]), str(skill_ids[7])],
            "qualifications": [
                {"degree": "B.Tech Information Technology", "institute": "NYU", "year_of_graduation": "2022"},
            ],
            "resumes": [],
        },
    ]
    for s in seekers:
        db["seeker"].insert_one(s)

    today = datetime.now()
    job_posts = [
        {
            "company_id": company_ids[0], "job_title": "Data Engineer",
            "job_description": "Build and maintain Spark and Airflow pipelines feeding the analytics warehouse.",
            "job_type": "Full Time", "no_of_openings": "3",
            "skill_required": "Python, SQL, Spark, Airflow",
            "location": "San Francisco, CA (Hybrid)",
            "post_date": today - timedelta(days=6),
            "last_date": today + timedelta(days=24),
            "status": "Selected",
        },
        {
            "company_id": company_ids[0], "job_title": "Machine Learning Engineer",
            "job_description": "Ship models to production with MLflow, Docker and Kubernetes.",
            "job_type": "Full Time", "no_of_openings": "2",
            "skill_required": "Python, Machine Learning, Kubernetes",
            "location": "Remote (US)",
            "post_date": today - timedelta(days=3),
            "last_date": today + timedelta(days=27),
            "status": "Selected",
        },
        {
            "company_id": company_ids[1], "job_title": "Analytics Engineer",
            "job_description": "Own dbt models and the retail reporting layer on the cloud warehouse.",
            "job_type": "Contract", "no_of_openings": "1",
            "skill_required": "SQL, dbt, Snowflake",
            "location": "Chicago, IL",
            "post_date": today - timedelta(days=10),
            "last_date": today + timedelta(days=20),
            "status": "Not Selected",
        },
    ]
    for j in job_posts:
        db["job_post"].insert_one(j)
