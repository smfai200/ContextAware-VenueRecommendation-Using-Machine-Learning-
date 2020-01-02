from sklearn.preprocessing import StandardScaler 
from sklearn.cluster import MiniBatchKMeans,DBSCAN
from sklearn.preprocessing import normalize
import pandas as pd
import numpy as np
from DBSCAN import MyDBSCAN

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

def LocationCluster(finaldf_local):
    
    def DBSCAN_Cluster(data):
        #datanew = data.as_matrix(columns=["Latitude","Longitude"])
        print("Clustering the Data")
        labels = []
        meters = 100 
        eps = meters / 10000
        # clustered_lat_long = DBSCAN(eps = 0.01, min_samples = 100)
        # clustered_lat_long.fit(data)
        # labels = clustered_lat_long.labels_

        for i in data.mb_cluster.unique():
            subset = data.loc[data.mb_cluster == i]
            clustered_lat_long = DBSCAN(eps = eps, min_samples = 100)
            datanew = subset.as_matrix(columns=["Latitude","Longitude"])
            clustered_lat_long.fit(datanew)
            subset['dbscan_cluster'] = clustered_lat_long.labels_
            data.loc[data.mb_cluster == i, 'dbscan_cluster'] = subset['dbscan_cluster']
            
        print("Cluster Labels: ", labels)
        return labels
    
    def Normalize(scaled_data):
        print("Normalizing Data according to Gaussian Distribution")
        normalized_data = normalize(scaled_data)
        x_normalized_data = pd.DataFrame(normalized_data,columns=["Latitude","Longitude","mb_cluster"])
        return x_normalized_data
        
    def Scale(data):
        print("Scaling Data to 0-1 Range")
        scaler = StandardScaler() 
        scaled_df = scaler.fit_transform(data) 
        return scaled_df
        
    LocationCluster = finaldf_local[["Latitude","Longitude","mb_cluster"]]
    LocationCluster.dropna(inplace=True)
    
    scaled_df = Scale(LocationCluster)
    my_labels = MyDBSCAN(scaled_df, eps=0.3, MinPts=10)
    
    # normalized_df = Normalize(scaled_df)

    # cluster_labels = DBSCAN_Cluster(data=normalized_df)
    # finaldf_local['DBScan_Labels'] = cluster_labels
    # finaldf_local['Cluster'] = finaldf_local.mb_cluster + (finaldf_local.dbscan_cluster.replace(-1.0, np.nan) / 100)
    # print('Number of unique clusters generated: {}'.format(len(finaldf_local.Cluster.unique())))
    
    return my_labels

data_df = Read_Data("FinalMergedMB.csv",1)
print("Shape of Data: ",data_df.shape)
data_df.corr()

# data_df_mb = LocationCluster(data_df)
# print(data_df_mb)
# data_df_mb.to_csv(dataset_path+"FinalMergedDBScan.csv")



