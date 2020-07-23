# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 12:35:23 2020
python 3.7

@author: amarti32
"""

import psycopg2 as pg2


def ConnectToDB(db_name, USER, PASSWORD):
    """
    Parameters
    ----------
    db_name : string, raw console input
        Name of the database
        
    USER : string, raw console input
        Username for postgresql
        
    PASSWORD : string, raw console input
        Password for postgresql
    ----------
    """
    
    try:
        #open connection to database
        global connection
        connection = pg2.connect(database = db_name, user = USER, password = PASSWORD)
        cursor = connection.cursor()
        
        #print the connection properties
        print(connection.get_dsn_parameters(),"\n")
        
        #print postgres version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")
        cursor.close()
        
        # #initiate extensions
        # cursor.execute("CREATE EXTENSION pg_trgm;")
        # print("Trigram Fuzzy Matching extension activated successfully")
        # cursor.execute("CREATE EXTENSION postgis;")
        # print("PostGIS extensions activated successfully")
        
    except (Exception, pg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        

def QueryBuilder():
    try:
        #Query the database for available tables
        Available_Tables_Query = ''' SELECT table_name 
                                    FROM information_schema.tables 
                                    WHERE table_schema='public' AND table_type='BASE TABLE';'''
                                    
        cursor2 = connection.cursor()
        cursor2.execute(Available_Tables_Query)
        table_list = cursor2.fetchall()
        
        print("The available tables in the database are the following : ")
        for row in table_list:
            print(row)
        
        cursor2.close()
        
        #Prompt the user for one of the valid tables listed
        table_name = input("Which of the tables do you want to query : ")
        
        
        #Prompt user for the search column
        search_column = input("Are you searching for the Country, Department, Municipality or Place Name? : ")
        if search_column.lower().replace(" ","") == 'country':
            QUERY_SEARCH_COL = 'name_0'
        elif search_column.lower().replace(" ","") == 'department':
            QUERY_SEARCH_COL = 'name_1'
        elif search_column.lower().replace(" ","") == 'municipality':
            QUERY_SEARCH_COL = 'name_2'
        elif search_column.lower().replace(" ","") == 'placename':
            QUERY_SEARCH_COL = 'nga_full_n'
        else:
            print("That was not a valid choice, please choose from the valid options\n")
            search_column = input("Are you searching for the Country, Department, Municipality or Place Name? :")
          
        
        #Prompt user for the search word
        search_word = input("Enter the word you want to search for in the table : ")
        
        
        #if searching for the country return all country entries
        if QUERY_SEARCH_COL == 'name_0':
            TABLE_QUERY = '''SELECT name_0, name_1, name_2, nga_full_n, point_x, point_y
                         FROM {0}
                         ORDER BY SIMILARITY({1}, '{2}') > .7 DESC
                         LIMIT 15;'''.format(table_name, QUERY_SEARCH_COL, search_word)
                         
            cursor3 = connection.cursor()
            cursor3.execute(TABLE_QUERY)
            ITEMS_RETURNED = cursor3.fetchall()
    
            print("The results for the country query are: ")
            print('Country  |  Department   |  Municipality  |  Place Name  |  Point X  |  Point Y  |\n')
    
            for row in ITEMS_RETURNED:
                print('{0}  |  {1}  |  {2}  |  {3}  |  {4:.6f}  |  {5:.6f}\n'.format(row[0], row[1], row[2], row[3], row[4], row[5]))

            cursor3.close()
            
        #if searching for the department return all department results    
        elif QUERY_SEARCH_COL == 'name_1':
            TABLE_QUERY = '''SELECT name_0, name_1, name_2, nga_full_n, point_x, point_y
                         FROM {0}
                         ORDER BY SIMILARITY({1}, '{2}') > .7 DESC
                         LIMIT 15;'''.format(table_name, QUERY_SEARCH_COL, search_word)
                         
            cursor3 = connection.cursor()
            cursor3.execute(TABLE_QUERY)
            ITEMS_RETURNED = cursor3.fetchall()
    
            print("The results for the department query are: ")
            print('Country  |  Department   |  Municipality  |  Place Name  |  Point X  |  Point Y  |\n')
    
            for row in ITEMS_RETURNED:
                print('{0}  |  {1}  |  {2}  |  {3}  |  {4:.6f}  |  {5:.6f}\n'.format(row[0], row[1], row[2], row[3], row[4], row[5]))

            cursor3.close()
              
        #if searching for the municipality return all municipality results    
        elif QUERY_SEARCH_COL == 'name_2':
            TABLE_QUERY = '''SELECT name_0, name_1, name_2, nga_full_n, point_x, point_y
                         FROM {0}
                         ORDER BY SIMILARITY({1}, '{2}') > .7 DESC
                         LIMIT 15;'''.format(table_name, QUERY_SEARCH_COL, search_word)
                         
            cursor3 = connection.cursor()
            cursor3.execute(TABLE_QUERY)
            ITEMS_RETURNED = cursor3.fetchall()
    
            print("The results for the municipality query are: ")
            print('Country  |  Department   |  Municipality  |  Place Name  |  Point X  |  Point Y  |\n')
    
            for row in ITEMS_RETURNED:
                print('{0}  |  {1}  |  {2}  |  {3}  |  {4:.6f}  |  {5:.6f}\n'.format(row[0], row[1], row[2], row[3], row[4], row[5]))

            cursor3.close()
        
        
        #if searching for the place name return the first 15 best results    
        elif QUERY_SEARCH_COL == 'nga_full_n':
            
            "TODO : ENABLE LIST INPUT OF COLUMN NAMES"
            "TODO : INSERT THOSE COLUMN NAMES INTO THE QUERY SOMEHOW"
            "TODO : FORMAT THE OUTPUT WITH THE INPUT COLUMN NAMES"
            
            TABLE_QUERY = '''SELECT name_0, name_1, name_2, nga_full_n, point_x, point_y
                         FROM {0}
                         ORDER BY SIMILARITY({1}, '{2}') > .7 DESC
                         LIMIT 15;'''.format(table_name, QUERY_SEARCH_COL, search_word)
                         
            cursor3 = connection.cursor()
            cursor3.execute(TABLE_QUERY)
            ITEMS_RETURNED = cursor3.fetchall()
        
        
            """
            TODO : CHANGE FORMATTING, USE {:< 10} TO LEFT ALIGN THE COLUMNS
            """
            
            print("The first 15 results for the place name query are: ")
            print('Country  |  Department   |  Municipality  |  Place Name  |  Point X  |  Point Y  |\n')
    
            for row in ITEMS_RETURNED:
                print('{0}  |  {1}  |  {2}  |  {3}  |  {4:.6f}  |  {5:.6f}\n'.format(row[0], row[1], row[2], row[3], row[4], row[5]))
    
            cursor3.close()

  
    except (Exception, pg2.Error) as error:
        print(error)
        
    



if __name__ == "__main__":
    
    db = input("Enter Database Name: ")
    username = input("Enter user name: ")
    password = input("Enter user password: ")
    
    #initaiate connection
    print("Initiating connection to database...\n")
    ConnectToDB(db_name=db, USER = username, PASSWORD = password)
    
    #begin building the search query
    print("Beginning Query Builder...\n")
    QueryBuilder()
    RERUN = input("Do you want to perform another query (y/n) : ")
    while RERUN.lower().replace(" ","") == 'y':
        QueryBuilder()
        RERUN = input("Do you want to perform another query (y/n) : ")
        
    else:
        print("Exiting Program")
        connection.close()
        print("Database connection successfully closed")
           
            
        
    




        
    


