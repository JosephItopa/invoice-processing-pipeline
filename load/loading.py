import os
import pandas as pd
from extraction.extract import upload_files 


def file_upload():
    """upload processed images, and extracted image contents(in csv)"""
    # gcs folders: raw_img, processed_img, processed_csv
    path = "./data/tmp_processed_csv/"
    files = [os.path.join(path, file) for file in os.listdir(path)]
    df = pd.concat((pd.read_csv(f) for f in files if f.endswith('csv')), ignore_index=True).reset_index()
    df.to_csv("./data/tmp_csv/file_{}.csv".format(pd.Timestamp.now().strftime("%Y-%m-%d %H%M%S")), index=False)

    upload_files("invoice-text-extraction", "./data/tmp_processed_img", "processed_img/")

    upload_files("invoice-text-extraction", "./data/tmp_processed_csv", "processed_csv/")

    upload_files("invoice-text-extraction", "./data/tmp_csv", "one_joined_csv/")
        
    #delete_files("invoice-text-extraction", "raw_img")
    print("finished processing...")