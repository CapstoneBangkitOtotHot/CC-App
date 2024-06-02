"""
Bangkit Capstone C241-PS005 Cloud Computing Team

API for creating bridge between ML (Machine Learning) and MD (Mobile Development) team"
"""

# fmt: off
__version__ = "0.2.0"
__description__ = "API for creating bridge between ML (Machine Learning) and MD (Mobile Development) team"
__author__ = "C241-PS005"
__author_email__ = "C241-PS005@bangkit.academy"
__license__ = "MIT"
# fmt: on

# Initialize firebase app
from . import firebase  # noqa: F401
from .app import app

app.title = "CC-App"
app.description = __description__
app.version = __version__
