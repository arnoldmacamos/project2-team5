from flask import Flask, render_template, redirect
import pandas as pd
import pymongo
import scrape_ukelection

# Create an instance of Flask
#app = Flask(__name__)

# Use PyMongo to establish Mongo connection
#mongo = pymongo(app, uri="mongodb://localhost:27017/weather_app")





# Route to render index.html template using data from Mongo
#@app.route("/")
#def home():

    # Find one record of data from the mongo database
#    destination_data = mongo.db.collection.find_one()

    # Return template and data
#    return render_template("index.html", vacation=destination_data)


#To execute etl of all needed data 
def execute_etl():
    
    #(1) import constituency data
    
    #(2) import party data
    
    #(4) import brexit result data
    
    #(5) import election result data
    
    

    # Run the scrape function
    import_election_result()
    

    # Update the Mongo database using update and upsert=True
    #mongo.db.collection.update({}, costa_data, upsert=True)

    # Redirect back to home page
    #return redirect("/")

def import_election_result():
    lst_ukelection_data = scrape_ukelection.scrape_info()
    df_ukelection_data = pd.DataFrame(lst_ukelection_data)
    df_ukelection_data.to_csv("datafiles/ukelection_results.csv", index = False)


#if __name__ == "__main__":
#app.run(debug=True)
execute_etl()