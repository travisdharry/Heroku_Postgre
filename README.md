# Heroku_Postgre
Connecting a Flask app served by Heroku with a Heroku PostgreSQL database.

## Setup files
- Procfile tells Heroku how to run the app
- runtime.txt tells Heroku what kind of language the app will be written in
- requirements.txt tells Heroku what libraries/versions your app will need

## Code to initialize db:
#import the relevant sql library 
from sqlalchemy import create_engine
#link to your database
engine = create_engine(<YOUR DATABASE URL>, echo = False)
#attach the data frame (df) to the database with a name of the 
#table; the name can be whatever you like
df.to_sql("df", con = engine, if_exists='append')
#run a quick test 
print(engine.execute(“SELECT * FROM df”).fetchone())