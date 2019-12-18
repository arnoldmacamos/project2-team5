from flask import Flask, render_template, redirect
import pandas as pd
from sqlalchemy import create_engine
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

    #(1) Clear Existing Data
    clear_data()
    
    #(2) import constituency data
    import_constituency()
    
    #(3) import party data
    import_parties()
    
    #(4) import brexit result data
    
    #(5) import election result data
    
    

    # Run the scrape function
    #import_election_result()
    

    # Update the Mongo database using update and upsert=True
    #mongo.db.collection.update({}, costa_data, upsert=True)

    # Redirect back to home page
    #return redirect("/")

def clear_data():
    connection_string = "postgres:root123@localhost:5432/ukelection_db"
    engine = create_engine(f'postgresql://{connection_string}')
    conn = engine.connect()
    conn.execute("delete from constituencies")
    conn.execute("delete from parties")

    conn.close()    
    
def import_constituency():
    constituency_file = "datafiles/constituency_ids.csv"
    df_constituency = pd.read_csv(constituency_file)
    
    # Create a filtered dataframe from specific columns
    constituency_cols = ["CONST ID","ONS ID", "Constituency"]
    df_transf_constituency= df_constituency[constituency_cols].copy()

    # Rename the column headers
    df_transf_constituency = df_transf_constituency.rename(columns={"CONST ID": "const_id",
                                                            "ONS ID": "ons_code",
                                                              "Constituency": "constituency_name"})

    # Clean the data by dropping duplicates and setting the index
    df_transf_constituency.drop_duplicates("const_id", inplace=True)
    df_transf_constituency.set_index("const_id", inplace=True)
    
    connection_string = "postgres:root123@localhost:5432/ukelection_db"
    engine = create_engine(f'postgresql://{connection_string}')
    
    df_transf_constituency.to_sql(name='constituencies', con=engine, if_exists='append', index=True)
    
def import_parties():
    party_file = "datafiles/parties_pro_or_anti.csv"
    df_party = pd.read_csv(party_file)
    
    # Create a filtered dataframe from specific columns
    party_cols = ["party_id", "party_code", "party_name", "pro_brexit"]
    df_transf_party= df_party[party_cols].copy()

    # Clean the data by dropping duplicates and setting the index
    df_transf_party.drop_duplicates("party_id", inplace=True)
    df_transf_party.set_index("party_id", inplace=True)
    
    connection_string = "postgres:root123@localhost:5432/ukelection_db"
    engine = create_engine(f'postgresql://{connection_string}')
    
    df_transf_party.to_sql(name='parties', con=engine, if_exists='append', index=True)
    

def import_election_result():
    lst_ukelection_data = scrape_ukelection.scrape_info()
    df_ukelection_data = pd.DataFrame(lst_ukelection_data)
    df_ukelection_data.to_csv("datafiles/ukelection_results.csv", index = False)


#if __name__ == "__main__":
#app.run(debug=True)
execute_etl()