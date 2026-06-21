"""Freeze the Flask app into a static site for Netlify deployment."""
from flask_frozen import Freezer
from app import app

freezer = Freezer(app)

if __name__ == "__main__":
    freezer.freeze()
