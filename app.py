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
 
#  '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>Description</th>\n      <th>Value</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>Equatorial Diameter</td>\n      <td>6,792 km</td>\n    </tr>\n    <tr>\n      <th>1</th>\n      <td>Polar Diameter</td>\n      <td>6,752 km</td>\n    </tr>\n    <tr>\n      <th>2</th>\n      <td>Mass</td>\n      <td>6.42   10  Earth)</td>\n    </tr>\n    <tr>\n      <th>3</th>\n      <td>Moons</td>\n      <td>2 (Phobos  Deimos)</td>\n    </tr>\n    <tr>\n      <th>4</th>\n      <td>Orbit Distance</td>\n      <td>227,943,824 km (1.52 AU)</td>\n    </tr>\n    <tr>\n      <th>5</th>\n      <td>Orbit Period</td>\n      <td>687 days (1.9 years)</td>\n    </tr>\n    <tr>\n      <th>6</th>\n      <td>Surface Temperature</td>\n      <td>-153 to 20  C</td>\n    </tr>\n    <tr>\n      <th>7</th>\n      <td>First Record</td>\n      <td>2nd millennium BC</td>\n    </tr>\n    <tr>\n      <th>8</th>\n      <td>Recorded By</td>\n      <td>Egyptian astronomers</td>\n    </tr>\n  </tbody>\n</table>',  

# to initialize the values
mars_data =  {'news_title': 'BLABLA', 
              'news_p': "BIBLI",
               'jpl_url': 'fake_url', 
                'facts_tbl': '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>Value</th>\n    </tr>\n    <tr>\n      <th>Description</th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>Equatorial Diameter</th>\n      <td>6,792 km</td>\n    </tr>\n    <tr>\n      <th>Polar Diameter</th>\n      <td>6,752 km</td>\n    </tr>\n    <tr>\n      <th>Mass</th>\n      <td>6.42 x 10^23 kg (10.7% Earth)</td>\n    </tr>\n    <tr>\n      <th>Moons</th>\n      <td>2 (Phobos &amp; Deimos)</td>\n    </tr>\n    <tr>\n      <th>Orbit Distance</th>\n      <td>227,943,824 km (1.52 AU)</td>\n    </tr>\n    <tr>\n      <th>Orbit Period</th>\n      <td>687 days (1.9 years)</td>\n    </tr>\n    <tr>\n      <th>Surface Temperature</th>\n      <td>-153 to 20 °C</td>\n    </tr>\n    <tr>\n      <th>First Record</th>\n      <td>2nd millennium BC</td>\n    </tr>\n    <tr>\n      <th>Recorded By</th>\n      <td>Egyptian astronomers</td>\n    </tr>\n  </tbody>\n</table>',
               'weather': 'weather', 
            'hemi_pct' : {'title1': 'Cerberus Hemisphere Enhanced',
                          'img_url1': 'https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg',
                          'title2': 'Schiaparelli Hemisphere Enhanced',
                          'img_url2': 'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg',
                          'title3': 'Syrtis Major Hemisphere Enhanced',
                          'img_url3': 'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg',
                          'title4': 'Valles Marineris Hemisphere Enhanced',
                          'img_url4': 'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg'}
               }    


# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Insert our first "mock element" into the db
mongo.db.collection.update({}, mars_data, upsert=True)


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", data=mars_data, 
                           hemisphere=mars_data['hemi_pct'],
                           facts_tbl = mars_data['facts_tbl'])


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
    

