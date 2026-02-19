import os
import time
import cv2
import numpy as np
from gcloud.gdrive_api import download_gdrive_files
from gcloud.gcp_functions import gdrive_folder_id

folder_id = gdrive_folder_id

def folder_creation():
    """creates all needed temporary folders"""
    print("initiating tasks...")

    directory1 = "./data/tmp_raw"
    directory2 = './data/tmp_preprocessed_img/'
    directory3 = './data/tmp_processed_img/'
    directory4 = './data/tmp_processed_csv/'
    directory5 = './data/tmp_csv/'
        
    if not os.path.exists(directory1):
        os.makedirs(directory1)
        
    if not os.path.exists(directory2):
        os.makedirs(directory2)

    if not os.path.exists(directory3):
        os.makedirs(directory3)

    if not os.path.exists(directory4):
        os.makedirs(directory4)

    if not os.path.exists(directory5):
        os.makedirs(directory5)


def pull_img_from_gdrive_to_tmp():
    """downloads raw files from google drive"""
    try:
        download_gdrive_files("./data/tmp_raw/", "_invoices", folder_id)
    except Exception as e:
        print(e)

def img_preprocess_():
    """preprocess all images"""
    num = 0
    input_path = './data/tmp_raw/'
    output_path = './data/tmp_preprocessed_img/'
    img_id = str(int(time.time()))

    def image_processor(image):
        img = cv2.imread(image)
        blurred = cv2.blur(img, (3,3))
        canny = cv2.Canny(blurred, 50, 200)

        # find the non-zero min-max coords of canny
        pts = np.argwhere(canny>0)
        y1, x1 = pts.min(axis=0)
        y2, x2 = pts.max(axis=0)

        # crop the region
        cropped = img[y1:y2, x1:x2]
            
        # Apply dilation and erosion to remove some noise
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(cropped, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)
        return img

    for filename in os.listdir(input_path):
        if any([filename.endswith(x) for x in [".png", "jpg"]]):
            try:
                img = image_processor(os.path.join(input_path, filename))
                cv2.imwrite(os.path.join(output_path, '{0}_img{1}.jpg'.format(img_id,num)), img)
                cv2.waitKey(2)
                print("thumbnail created")
                os.remove(os.path.join(input_path, filename))
                print("removed raw image")
                num += 1
            except Exception as error:
                print(f"skipping {filename}", " ", error)
                continue
