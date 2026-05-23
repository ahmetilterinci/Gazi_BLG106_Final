"""
CyberLearn AI — Auth Blueprint
Kullanıcı kimlik doğrulama route'ları (/auth prefix'i ile) bu blueprint'te yer alır.
"""

from flask import Blueprint

auth = Blueprint("auth", __name__, url_prefix="/auth")

from app.auth import routes  # noqa: F401  # pylint: disable=wrong-import-position
