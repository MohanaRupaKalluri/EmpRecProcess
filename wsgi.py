"""Production entrypoint: gunicorn wsgi:app

The database is selected in db.py -- a real MongoDB when MONGO_URI is set,
otherwise an embedded demo store, so the app runs anywhere with zero config.
"""

import os

from main import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))
