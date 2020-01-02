import os
import numpy as np
import pandas as pd
from sklearn import preprocessing

dataset_path = "../data/dataset_TIST2015/"

def Read_Data(filename,limit):
    chunksize = 10 ** 6
    count = 0
    data_df = pd.DataFrame()
    for chunk in pd.read_csv(dataset_path+filename, 
                       sep="\t", 
                       header=None,
                       chunksize= chunksize):
        if(count == limit):
            break
        else:
            data_df = pd.concat([data_df,chunk], ignore_index=True)
            print("Chunk ",filename," ",count," : Processed")
            count += 1
    return data_df


def Clean_data_Checkin(data_df_local):
    def Clean_date():
        data_df_local['UTC time new'] = pd.to_datetime(data_df_local['UTC time'],format="%a %b %d %H:%M:%S %z %Y")
        year_formater = lambda x: x.year
        month_formater = lambda x: x.month
        day_formater = lambda x: x.day

        data_df_local['Year'] = data_df_local['UTC time new'].apply(year_formater)
        data_df_local['Month'] = data_df_local['UTC time new'].apply(month_formater)
        data_df_local['Day'] = data_df_local['UTC time new'].apply(day_formater)
    
    data_df_local.columns = ["User ID","Venue ID","UTC time","Timezone"]
    Clean_date()
    data_df_local['Timezone'] = data_df_local['Timezone']/60
    data_df_local = data_df_local.drop(['UTC time','UTC time new'],axis=1)
    return data_df_local
    
def Clean_data_POI(data_df_POI_local):
    data_df_POI_local.columns = ["Venue ID","Latitude","Longitude","Venue category name","Country code"]
    return data_df_POI_local

def MergeDatasets():
    finaldf = pd.merge(data_df_POI,data_df,on="Venue ID")
    #finaldf_grouped = finaldf.groupby(["User ID","Venue ID"])
    # print(finaldf.first())
    return finaldf

def ValueCount(data_df):
    _count = lambda x:len(x)
    data_df["Count"] = data_df["Venue category name"].apply(_count)
    value_array = data_df['Count'].values
    value_array = value_array.reshape(-1,1)
    print("Length: ", len(value_array))
    min_max_scaler = preprocessing.MinMaxScaler()
    scaled_array = min_max_scaler.fit_transform(value_array)
    data_df["Count_Scaled"] = scaled_array
    return data_df

data_df = Read_Data("dataset_TIST2015_Checkins.txt",8)
print("Shape of the DataFrame: ", data_df.shape)

data_df_POI = Read_Data("dataset_TIST2015_POIs.txt", 10)
print("Shape of the DataFrame: ", data_df_POI.shape)

#Backups of DataFrame
data_df_backup = data_df
data_df_POI_backup = data_df_POI

#Clean Data and Format Dates
data_df = Clean_data_Checkin(data_df)
data_df_POI = Clean_data_POI(data_df_POI)


print(data_df.head(5))
print(data_df_POI.head(5))

finaldf = MergeDatasets()
finaldf = ValueCount(finaldf)

finaldf.to_csv(dataset_path+"FinalMergedDF_CountVector.csv")
