"""
Bangkit Capstone C241-PS005 Cloud Computing Team

API for creating bridge between ML (Machine Learning) and MD (Mobile Development) team"
"""

# fmt: off
__version__ = "0.0.1"
__description__ = "API for creating bridge between ML (Machine Learning) and MD (Mobile Development) team"
__author__ = "C241-PS005"
__author_email__ = "C241-PS005@bangkit.academy"
__license__ = "MIT"
# fmt: on

import flask
from .auth.urls import urls_patterns as auth_urls


def redirect_docs():
    return flask.redirect("/docs")


def main():
    app = flask.Flask("cc_api")

    # Auth urls
    for kwargs_url in auth_urls:
        app.add_url_rule(**kwargs_url)

    # Redirect to docs
    app.add_url_rule("/", redirect_docs)

    app.run(port=5000)
