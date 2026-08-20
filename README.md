# Employment Recruitment System (EmpRecProcess)

A full-stack online employment recruitment platform with role-based workflows for **admins**, **recruiters**, and **job seekers**. Built with **Python**, **Flask**, and **MongoDB Atlas**.

## Live Demo

**No database setup required.** The app ships with an embedded demo database
(`db.py`) seeded on startup with sample companies, recruiters, job seekers,
skills and job posts. Set no environment variables and it just runs.

### Deploy free on Hugging Face Spaces (always-on, no card)

1. Create a Space: https://huggingface.co/new-space -> name `emprecprocess`, SDK **Docker** (blank), Public.
2. Push this repo to the Space:
   ```bash
   git clone https://github.com/MohanaRupaKalluri/EmpRecProcess.git
   cd EmpRecProcess
   git remote add space https://huggingface.co/spaces/<your-username>/emprecprocess
   git push space HEAD:main
   ```
3. Add this front matter at the top of the Space's `README.md`:
   ```yaml
   ---
   title: Employment Recruitment System
   sdk: docker
   app_port: 7860
   ---
   ```
4. It builds and goes live at `https://<your-username>-emprecprocess.hf.space`.

### Demo logins

| Role | Email | Password |
| --- | --- | --- |
| Company | `hr@northwind.example` | `demo123` |
| Recruiter | `recruiter@demo.com` | `demo123` |
| Job seeker | `seeker@demo.com` | `demo123` |

### Run locally

```bash
pip install -r requirements.txt
python wsgi.py     # http://localhost:7860
```

### Using a real MongoDB instead

Set `MONGO_URI` (optionally `MONGO_DB`, `SECRET_KEY`) and the app connects to
that cluster instead of the embedded demo database. No credentials are stored
in source code.

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
