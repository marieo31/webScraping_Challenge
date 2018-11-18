# -*- coding: utf-8 -*-
import scrape_mars
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

import pandas as pd
import numpy as np
import json

# let
# mars_data = scrape_mars.scrape_mars()

# Let fake some data to see how it goes without scraping each time

# create a fake dataframe f
                 

# df = pd.DataFrame({ 'A' : 1.,
#                     'B' : pd.Timestamp('20130102'),
#                     'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
#                     'D' : np.array([3] * 4,dtype='int32'),
#                     'E' : pd.Categorical(["test","train","test","train"]),
#                     'F' : 'foo' })
# 
# print(df)
 
#  
# mars_data =  {'news_title': 'Opportunity Hunkers Down During Dust Storm', 
#               'news_p': "It's the beginning of the end for the planet-encircling dust storm on Mars. But it could still be weeks, or even months, before skies are clear enough for NASA's Opportunity rover to recharge its batteries and phone home.",
#                'jpl_url': 'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA17462_ip.jpg', 
# #                 'facts_tbl': 
#                'weather': 'Sol 2230 (2018-11-14), high -5C/23F, low -72C/-97F, pressure at 8.59 hPa, daylight 06:22-18:39', 
#                'hemi_pct': [{'title': 'Cerberus Hemisphere Enhanced', 
#                              'img_url': 'https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg'}, 
#                              {'title': 'Schiaparelli Hemisphere Enhanced', 
#                               'img_url': 'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg'},
#                               {'title': 'Syrtis Major Hemisphere Enhanced', 
#                                'img_url': 'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg'}, 
#                               {'title': 'Valles Marineris Hemisphere Enhanced', 
#                                'img_url': 'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg'}]
#                }    

# Create an instance of Flask
app = Flask(__name__)


# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# mongo.db.collection.update({}, mars_data, upsert=True)

# mars_data = scrape_mars.scrape_mars()

# Update the Mongo database
# mongo.db.collection.update({}, mars_data, upsert=True)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()


    # Return template and data
    return render_template("index.html", data=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function 
    mars_data = scrape_mars.scrape_mars()
    
    # Update the Mongo database
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
    
# print(scrape_mars.scrape_news())
# print(scrape_mars.scrape_jpl_images())
# print(scrape_mars.scrape_weather())
# print(scrape_mars.scrape_mars_facts())
# print(scrape_mars.scrape_hemispheres())

# dico = scrape_mars.scrape_mars()

# print(dico)

