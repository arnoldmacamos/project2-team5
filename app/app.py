from flask import Flask, render_template, redirect
from sqlalchemy import create_engine
import pandas as pd
import pymongo
import scrape_ukelection


#ETL of all needed data
def execute_etl():

    print("START UK Brexit/Election Data Gathering")
    
    #(1) Clear Existing Data
    clear_data()
    
    #(2) import constituency data
    import_constituency()
    
    #(3) import party data
    import_parties()
    
    #(4) import brexit result data
    import_brexit_results()
    
    #(5) import election result data
    import_election_results()
    
    print("Data Gathering is COMPLETED")
  

#Clear all reccords in the database
def clear_data():
    connection_string = "postgres:root123@localhost:5432/ukelection_db"
    engine = create_engine(f'postgresql://{connection_string}')
    conn = engine.connect()
    
    conn.execute("delete from election_results")
    conn.execute("delete from brexit_results")
    conn.execute("delete from constituencies")
    conn.execute("delete from parties")

    conn.close()    

#Import UK Constituencies    
def import_constituency():
    print("Import constituencies")
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

#Import UK Parties    
def import_parties():
    print("Import parties")
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
    
#Import 2019 UK Election results
def import_election_results():
    print("Import 2019 UK Election results")
    
    include_webscraping = input("-->Would you like to get the fresh data through web scraping? \n-->(Enter 'Y' to do web scraping): ")
    
    if (include_webscraping.upper() == "Y"):
        lst_ukelection_data = scrape_ukelection.scrape_info()    
        df_ukelection_data = pd.DataFrame(lst_ukelection_data)
        df_ukelection_data.to_csv("datafiles/ukelection_results.csv", index = False)
    
    ukelection_file = "datafiles/ukelection_results.csv";
    df_ukelection = pd.read_csv(ukelection_file)
    
    connection_string = "postgres:root123@localhost:5432/ukelection_db"
    engine = create_engine(f'postgresql://{connection_string}')
    conn = engine.connect()

    df_constituencies = pd.read_sql_query("select * from constituencies", con=conn, index_col = "ons_code")
    
    df_parties = pd.read_sql_query("select * from parties", con=conn, index_col = "party_code")
    
    df_ukelection = df_ukelection.join(df_constituencies, on="ons_code").join(df_parties, on="party_code")
    
    df_ukelection.index = [x for x in range(1, len(df_ukelection.values)+1)]
    
    df_ukelection.index.name = "id"
    
    # Create a filtered dataframe from specific columns
    df_ukelection_cols = ["const_id", "party_id", "votes_share", "year"]
    df_transf_ukelection= df_ukelection[df_ukelection_cols].copy()
    
    df_transf_ukelection.to_sql(name='election_results', con=engine, if_exists='append', index=True)
    
    conn.close()

 
#Import 2016 Brexit results  
def import_brexit_results():
    print("Import 2016 Brexit results")
    brexit_file = "datafiles/eu_2016_results.csv"
    df_brexit = pd.read_csv(brexit_file)
    
    connection_string = "postgres:root123@localhost:5432/ukelection_db"
    engine = create_engine(f'postgresql://{connection_string}')
    conn = engine.connect()

    df_constituencies = pd.read_sql_query("select * from constituencies", con=conn, index_col = "ons_code")
    
    df_brexit = df_brexit.join(df_constituencies, on="ONS ID")
    df_brexit["year"] = 2016
    
    df_brexit.index = [x for x in range(1, len(df_brexit.values)+1)]
    df_brexit.index.name = "id"
    
    # Create a filtered dataframe from specific columns
    df_brexit_cols = ["const_id", "Percent Pro-Brexit", "Percent Anti-Brexit", "year"]
    df_transf_brexit= df_brexit[df_brexit_cols].copy()

    # Rename the column headers
    df_transf_brexit = df_transf_brexit.rename(columns={"Percent Pro-Brexit": "probrexit_share",
                                                            "Percent Anti-Brexit": "antibrexit_share"})
                                                            
    df_transf_brexit.to_sql(name='brexit_results', con=engine, if_exists='append', index=True)
    
    conn.close()

execute_etl()