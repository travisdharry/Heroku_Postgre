# Import dependencies
# Flask converts Python outputs to a format browsers can read
from flask import Flask, render_template, request
# Psycopg2 allows Python to interface with PostgreSQL databases
# import psycopg2

# Create a new Flask instance
app = Flask(__name__)

# Create Flask route
@app.route('/')
def index():
    return render_template("index.html")