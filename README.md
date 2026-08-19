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

## Live Demo / Deployment

The previous Render demo is offline (free Render web services are suspended after inactivity).
To bring the demo back, deploy the Flask app to any of these free hosts:

| Host | Notes |
|---|---|
| **Render** (recreate service) | Free web service; sleeps after 15 min idle. Build: `pip install -r requirements.txt`, Start: `gunicorn main:app` |
| **Hugging Face Spaces (Docker)** | Free, always-on, allows outbound MongoDB Atlas connections |
| **Koyeb** | Free instance, no cold-start sleep, Git-based deploy |
| **Fly.io** | Free allowance, `fly launch` on the repo |
| **Railway** | Simple Git deploy, trial credits |

Required environment variables on any host:

```
MONGODB_URI=<your MongoDB Atlas connection string>
FLASK_SECRET_KEY=<random secret>
```

Also add `0.0.0.0/0` (or the host's IPs) to MongoDB Atlas Network Access, and make sure the app binds to the platform port:

```python
import os
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
```

## Portfolio

See this project in my data/AI portfolio: **[mohana-kalluri.lovable.app](https://mohana-kalluri.lovable.app/)**

## License

This project is open for learning and portfolio use.
