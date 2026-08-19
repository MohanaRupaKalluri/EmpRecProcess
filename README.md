# Employment Recruitment System (EmpRecProcess)

A full-stack online employment recruitment platform with role-based workflows for **admins**, **recruiters**, and **job seekers**. Built with **Python**, **Flask**, and **MongoDB Atlas**.

## Features

- **Admin panel** — manage skills, companies, recruiters, and job postings
- **Recruiter workflow** — post jobs, review applicants, and schedule interviews
- **Job seeker workflow** — create profiles, apply to jobs, and track applications
- **Role-based access** — separate login flows and dashboards for each role
- **MongoDB-backed persistence** — stores users, jobs, applications, and interviews
- **Template-driven UI** — server-rendered HTML with Jinja2/Flask templates

## Architecture

```
Browser (HTML templates)
    │
    └── Flask server
        ├── MongoDB Atlas (users, jobs, applications, interviews)
        └── Session-based authentication
```

## Tech Stack

- **Python** — backend logic
- **Flask** — web framework and routing
- **MongoDB Atlas** — NoSQL database (configured via environment variables)
- **PyMongo** — MongoDB driver for Python
- **Jinja2 / HTML templates** — server-rendered front-end

## Run Locally

```bash
# clone the repo
git clone https://github.com/MohanaRupaKalluri/EmpRecProcess.git
cd EmpRecProcess

# create a virtual environment
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# set environment variables
export MONGODB_URI="your-mongodb-atlas-connection-string"
export FLASK_SECRET_KEY="your-secret-key"

# start the app
python main.py
```

Open `http://localhost:5000` in your browser.

## Security Note

Move the MongoDB connection string and Flask secret key to environment variables before deploying. Never commit credentials to version control.

## Project Structure

```
EmpRecProcess/
├── main.py              # Flask application with all routes
├── requirements.txt     # Python dependencies
├── EmpRecProcess/       # Application modules and templates
├── static/              # CSS, JS, images
├── templates/           # HTML templates
└── README.md            # Project documentation
```

## Portfolio

See this project in my data/AI portfolio: **[meetmohana.lovable.app](https://meetmohana.lovable.app/)**

## License

This project is open for learning and portfolio use.
