from sklearn.preprocessing import StandardScaler 
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import normalize
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

def MiniBatch(finaldf_local):
    def MiniBatchLaunch(data):
        mb = MiniBatchKMeans(n_clusters=100, init='k-means++', n_init=10, batch_size=1000)
        mb.fit(data)
        labels = mb.labels_ 
        return labels

    def Normalize(scaled_data):
        print("Normalizing Data according to Gaussian Distribution")
        normalized_data = normalize(scaled_data)
        x_normalized_data = pd.DataFrame(normalized_data)
        print(x_normalized_data.head(2))
        return x_normalized_data
        
    def Scale(data):
        print("Scaling Data to 0-1 Range")
        scaler = StandardScaler() 
        scaled_df = scaler.fit_transform(data) 
        print(scaled_df)
        return scaled_df

    print("Running MiniBatch")
    LocationCluster = finaldf_local[["Latitude","Longitude"]]
    LocationCluster.fillna(0,inplace=True)
    
    scaled_df = Scale(LocationCluster)
    normalized_df = Normalize(scaled_df)

    MiniBatch_labels = MiniBatchLaunch(data=normalized_df)
    print(MiniBatch_labels)
    LocationCluster['mb_cluster'] = MiniBatch_labels
    return LocationCluster


data_df = Read_Data("FinalMergedDF.csv",3)
data_df_mb = MiniBatch(data_df)
data_df_mb.to_csv(dataset_path+"FinalMergedMB.csv")



