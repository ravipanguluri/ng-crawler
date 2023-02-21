import os
import pandas as pd
import numpy as np
import csv


def load_data(data_path):
    return (os.listdir(data_path))

def main():
    all_objects = []

    data_path = "./data"
    csvs = load_data(data_path)
    for i in csvs:
        df = pd.read_csv(data_path + "/" + i)
        df.drop(index = range(0 ,6), inplace = True)
        df['cname'] = df.Vendor
        df['website'] = df.URL
        df['industry'] = df['Sub Category']

        keep_cols = ['cname', 'website', 'industry']
        df.drop(columns = ([i for i in list(df.columns) if i not in keep_cols]), axis = 1, inplace = True)

        company_objects = df.to_dict(orient = 'records')
        print(company_objects[:10])
        all_objects.extend(company_objects)


    return all_objects




# def main():
#     file = open("./data/testing.csv")
#     csvreader = csv.reader(file)
#     header  = []
#     header = next(csvreader)
#     print(header)
#     file.close()    
main()
