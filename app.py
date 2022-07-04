# Import dependencies
# Flask converts Python outputs to a format browsers can read
from flask import Flask, render_template, request
# Psycopg2 allows Python to interface with PostgreSQL databases
import psycopg2
import pandas as pd
import os

# Create a new Flask instance
app = Flask(__name__)

# Find environment variables
DATABASE_URL = os.environ.get("DATABASE_URL", None)

# Create Flask route
@app.route('/')
def index():
    con = psycopg2.connect(DATABASE_URL)
    cur = con.cursor()
    # query 
    query = "SELECT * FROM player_df"

    # return results as a dataframe
    results = pd.read_sql(query, con)

    return render_template("index.html", tables=[results.to_html(classes='data')], titles=df.columns.values)