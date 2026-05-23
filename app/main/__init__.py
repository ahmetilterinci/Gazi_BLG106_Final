"""
CyberLearn AI — Main Blueprint
Ana sayfalar ve genel route'lar bu blueprint altında toplanır.
"""

from flask import Blueprint

main = Blueprint("main", __name__)

from app.main import routes  # noqa: F401  # pylint: disable=wrong-import-position
