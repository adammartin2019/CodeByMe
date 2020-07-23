import pandas as pd
import xlrd
from pandas import ExcelWriter
from pandas import ExcelFile



"""
Need to read in the relevant excel files; the master codex file and then the 
excel file you are trying to clean and structure. Filepath1 should point to the
master codex and filepath2 should point to the excel file to be cleaned

"""

def MissingDeathCodeCheck(CodexFilepath, DatasetFilepath):
    """
    CodexFilepath : string : filepath to master codex
    DatasetFilepath : string : filepath to dataset to be checked
    
    Useful for quickly checking which death codes are missing from a given dataset
    file by checking the column names against the master codex death code column row entries.
    
    Need to first organize the dataset file to make sure header and column names are 
    in the right place
    
    """
    list1 = []
    list2 = []
    
    dfCodex = pd.read_excel(CodexFilepath)
    dfData = pd.read_excel(DatasetFilepath)
    
    for i in dfCodex["Causa de Defuncion Codes"]:
        list1.append(i)
    
    for i in dfData.columns.values:
        list2.append(i)
    
    for i,j in zip(list1,list2):
        if j not in list1:
            print(j)
    
    





def ExcelDFCleaner(filepath1, filepath2,num_depts,num_munic,num_deaths,country_code,to_filepath,data_year ):
    """
    **make sure to follow filepath \\ conventions**
    
    filepath1 : string : path to file
    filepath2 : string : path to file
    num_depts : int : number of departments in DeptCodes column
    num_munic : int : number of municipalities in MunicipCodes column
    num_deaths : int : number of death codes used in CauseOfDeath column
    country_code : string : two letter initials for country studied; "GM" for guatemala for example
    to_filepath : string : filepath destination for the exported excel file
    data_year : string : year of the data for the exporting filepath
    
    """
    
    
    "Create dataframes from the input filepaths"
    df1 = pd.read_excel(filepath1)
    df2 = pd.read_excel(filepath2)
    
    
    "Create dictionaries to store the unique identifier columns for later comparison"
    t1 = list()
    t2 = list()
    
    for i in df1.index[0:num_depts]:
    
        t1.append(df1["Dept Codes"][i])
        t2.append(df1["Departamento de registro"][i])
        
    DeptDict = dict(zip(t1,t2))
    
    
    t3 = list()
    t4 = list()  
        
    for i in df1.index[0:num_munic]:
        t3.append(df1["Municipio Registro Codes"][i])
        t4.append(df1["Municipio de registro"][i])
    
    MunicDict = dict(zip(t3,t4))
    
    
    t5 = list()
    t6 = list()
    
    for i in df1.index[0:num_deaths]:
        t5.append(df1["Causa de Defuncion Codes"][i])
        t6.append(df1["CauseDescrip"][i])
        
    DeathDict = dict(zip(t5,t6))

    print("Data dictionaries completed")
    

    """
    First loop checks each line in the municipalities codes column and creates
    a standard naming convention by adding the country code in front and adding 
    a 0 if the read in codes begin with a zero which is not an accepted format for 
    ints in python.
    
    The next loop creates a new column Munic_Name and then checks each code against
    the Municipalities dictionary codex and enters the name of the municipality based
    on the code.
    
    Next, get the list of column names from the original data and filter for 
    the death cause codes by checking for names where the length is less than or equal
    to 4. Create a new df3 empty list to store column names and append the relevant
    names ending by creating dataframe3. 
    
    Lastly loop through the column names in df2 and check against the df3 column
    names. If they are in df3 set df3 equal to df2 column, otherwise retrieve the 
    description of the death cause from the death dict and set the name in df3.
    
    Then export to new excel and save. 
    
    
    """
    
    df2["Munic_Code"] = df2["Munic_Code"].astype(str)
    
    for i in range(len(df2["Munic_Code"])):
        if len(df2.at[i,"Munic_Code"]) <= 3:
            df2.at[i,"Munic_Code"] = country_code+"0"+str(df2.at[i,"Munic_Code"])
        else:
            df2.at[i,"Munic_Code"] = country_code+str(df2.at[i,"Munic_Code"])
    
    print("Country municipality codes cleaned")
    
    
    df2["Munic_Name"] = pd.Series()
    for i in range(len(df2["Munic_Code"])):
        df2["Munic_Name"][i] = MunicDict[df2["Munic_Code"][i]]
        
    print("Country municipality names added")
    
    
    df2Cols = list(df2.columns.values)
    df2ColsFiltered = list(filter(lambda x: len(x)<=4, df2Cols))
    df3Cols = []
    df3Cols.append("Munic_Name")
    df3Cols.append("Munic_Code")
    for i in df2ColsFiltered:
        colName = DeathDict[i]
        df3Cols.append(colName)
    df3Cols.append("Grand Total")
    df3 = pd.DataFrame(columns = df3Cols)
    
    print("Dataframe 3 created, ready to be filled with data")
    
    
    for i in df2.columns.values:
        if i in df3.columns.values:
            df3[i] = df2[i]
        else:
            namecode = DeathDict[i]
            df3[namecode] = df2[i]
    
    df3.fillna(value=0,inplace=True)
    print("Dataframe 3 completed and nullvalues replaced with 0" )
    
    
    df3.to_excel(str(to_filepath) + "\\" + str(data_year) + "DeathData_Cleaned.xlsx")
    
    print("Dataframe 3 successfully exported to excel file")
    print("Terminating program")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    