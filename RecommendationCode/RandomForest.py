from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

dataset_path = "../data/dataset_TIST2015/"


def Read_Data(filename,limit):
    chunksize = 10 ** 6
    count = 0
    data_df = pd.DataFrame()
    for chunk in pd.read_csv(dataset_path+filename,
                       chunksize= chunksize):
        if(count == limit):
            break
        else:
            data_df = pd.concat([data_df,chunk], ignore_index=True)
            print("Chunk ",filename," ",count," : Processed")
            count += 1
    return data_df

def User_Venue_Values():

    pass


data_df = Read_Data("FinalMergedDF.csv",1)
cols = data_df.columns
data_df = data_df[:1000]
data_df.columns = cols
print(data_df[["User ID","Venue ID"]].head(2))
finaldf_grouped = data_df.groupby(["User ID","Venue ID"])
size = finaldf_grouped.size()
print(size[size > 1])
print(finaldf_grouped.get_group((9448,'3fd66200f964a52014eb1ee3')))
#print(finaldf_grouped.groups.keys())


# data_df.drop_duplicates(["User ID","Venue ID"])
# data_df_pivot = data_df.reset_index().pivot_table(index="User ID",columns="Venue ID",values="Venue category name")
# print(data_df_pivot.head(2))

