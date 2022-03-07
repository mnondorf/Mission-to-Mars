from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define the route for the HTML page 
@app.route("/")            

# The following function is what links our visual representation of our work, our web app, to the code that powers it.
def index(): 
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars) 

# The next function will set up our scraping route.This route will be the "button" of the web application, 
# the one that will scrape updated data when we tell it to from the homepage of our web app
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)
if __name__ == "__main__":
   app.run()
