import scrape_mars
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# # Create an instance of Flask
# app = Flask(__name__)


# # Use PyMongo to establish Mongo connection
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# # Route to render index.html template using data from Mongo
# @app.route("/")
# def home():

#     # Find one record of data from the mongo database
#     destination_data = mongo.db.collection.find_one()


#     # Return template and data
#     return render_template("templates/index.html")

# if __name__ == "__main__":
#     app.run(debug=True)




# print(scrape_mars.scrape_news())
# print(scrape_mars.scrape_jpl_images())
# print(scrape_mars.scrape_weather())
# print(scrape_mars.scrape_mars_facts())
# print(scrape_mars.scrape_hemispheres())

dico = scrape_mars.scrape_mars()

print(dico)

