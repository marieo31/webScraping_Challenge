import scrape_mars
from flask import Flask, render_template, redirect
# from flask_pymongo import PyMongo

# Create an instance of Flask
app = Flask(__name__)


# Route to render index.html template using data from Mongo
@app.route("/")
def home():


    # Return template and data
    return render_template("templates/index.html", vacation=destination_data)

if __name__ == "__main__":
    app.run(debug=True)




# print(scrape_mars.scrape_news())
# print(scrape_mars.scrape_jpl_images())
# print(scrape_mars.scrape_weather())
# print(scrape_mars.scrape_mars_facts())
# print(scrape_mars.scrape_hemispheres())

