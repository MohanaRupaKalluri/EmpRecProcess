# Employment Recruitment System (EmpRecProcess)

A full-stack online employment recruitment platform with role-based workflows for **admins**, **recruiters**, and **job seekers**. Built with **Python**, **Flask**, and **MongoDB Atlas**.

## Live Demo

The repo is deployment-ready (`Dockerfile`, `render.yaml`, `Procfile`, gunicorn, env-based config). Easiest path — **Render Blueprint (one click, free tier):**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/MohanaRupaKalluri/EmpRecProcess)

1. Click the button and sign in with GitHub (existing Render accounts work).
2. Render reads `render.yaml` — builder, port, and health check are already set.
3. Paste your `MONGO_URI` when prompted (`SECRET_KEY` is auto-generated).
4. Click **Apply** — the app builds and goes live at `https://emprecprocess.onrender.com`.

**Alternatives (also free):**
- **Hugging Face Spaces** — new Space, SDK **Docker**, push this repo, add `MONGO_URI` / `SECRET_KEY` under Settings, Variables and secrets (serves on port **7860**).
- **Koyeb** — [deploy link](https://app.koyeb.com/deploy?type=git&repository=github.com/MohanaRupaKalluri/EmpRecProcess&branch=master&builder=dockerfile&name=emprecprocess), builder **Dockerfile**, port **7860**.

> After deploying, add `0.0.0.0/0` (or the host's egress IPs) under **MongoDB Atlas, Network Access**, otherwise database calls time out.
> Render's free instance sleeps after inactivity and wakes on the first request (~30s cold start).

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
    └── Flask server (gunicorn)
        ├── MongoDB Atlas (users, jobs, applications, interviews)
        └── Session-based authentication
```

## Tech Stack

- **Python** — backend logic
- **Flask + gunicorn** — web framework and production WSGI server
- **MongoDB Atlas** — NoSQL database (configured via environment variables)
- **PyMongo** — MongoDB driver for Python
- **Docker** — reproducible deploys on Koyeb / Hugging Face Spaces / Fly.io / Railway
- **Jinja2 / HTML templates** — server-rendered front-end

## Configuration

| Variable | Required | Description |
|---|---|---|
| `MONGO_URI` | yes | MongoDB Atlas connection string |
| `SECRET_KEY` | no | Flask session secret (random one generated if unset) |
| `PORT` | no | Port to bind (defaults to `7860`) |

## Run Locally

```bash
git clone https://github.com/MohanaRupaKalluri/EmpRecProcess.git
cd EmpRecProcess

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

export MONGO_URI="your-mongodb-atlas-connection-string"
export SECRET_KEY="your-secret-key"
export PORT=5000

python main.py
```

Open `http://localhost:5000`.

With Docker:

```bash
docker build -t emprecprocess .
docker run -p 7860:7860 -e MONGO_URI="..." -e SECRET_KEY="..." emprecprocess
```

## Security Note

The MongoDB connection string and Flask secret key are read from environment variables and are no longer hardcoded. If the previously committed Atlas credentials were ever live, rotate that database user's password in MongoDB Atlas.

## Project Structure

```
EmpRecProcess/
├── main.py              # Flask application with all routes
├── Dockerfile           # Container image for Koyeb / HF Spaces
├── Procfile             # Start command for Render / Railway / Heroku-style hosts
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
