from load.loading import file_upload
from transformation.transform import transformation_pipeline
from extraction.extract import folder_creation, pull_img_from_gdrive_to_tmp, img_preprocess_

def pipeline():
    print("creating temporary folders..")
    folder_creation()
    print("pulling image data from gdrive to temporary folder..")
    pull_img_from_gdrive_to_tmp()
    print("preprocessing images..")
    img_preprocess_()
    # ------------------
    print("extraction of text and transformation..")
    transformation_pipeline()
    # --------------------
    print("uploading of CSV files to Google cloud storage..")
    file_upload()


if __name__ == '__main__':
    pipeline()