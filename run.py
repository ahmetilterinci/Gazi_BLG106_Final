"""
CyberLearn AI — Uygulama Giriş Noktası

Çalıştırmak için:
    python run.py
veya:
    flask run
"""

import os

from app import create_app, db

app = create_app(os.environ.get("FLASK_CONFIG", "development"))


if __name__ == "__main__":
    app.run(debug=True)
