"""
CyberLearn AI — Uygulama Giriş Noktası

Çalıştırmak için:
    python run.py
veya:
    flask run
"""

from app import create_app

app = create_app("development")

if __name__ == "__main__":
    app.run(debug=True)
