import os
import re
import time
import json
import shutil
import requests
import pandas as pd

def transformation_pipeline():
    """extract image contents and store as csv on tmp folder"""
    #
    num = 0
    input_path = './data/tmp_preprocessed_img/'
    target = './data/tmp_processed_img/'

    file_id = str(int(time.time()))

    def extract_text(image):
        receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt' # Receipt OCR API endpoint
        imageFile = image # Modify it to use your own file
        r = requests.post(receiptOcrEndpoint, data = { \
                                                    'api_key': 'TEST',        # Use 'TEST' for testing purpose \
                                                    'recognizer': 'auto',       # can be 'US', 'CA', 'JP', 'SG' or 'auto' \
                                                    'ref_no': 'ocr_python_123', # optional caller provided ref code \
                                                    }, \
        files = {"file": open(imageFile, "rb")}) # bill1.jpg
        return r

    def get_address_phone(ocr_text):
        test=""
        rgx_phone = re.compile(r"(?:\+\d{2})?\d{3,4}\D?\d{3}\D?\d{3}")
        phone_no = [x.replace(" ","") for x in ocr_text if re.findall(rgx_phone, x)]
        states = ["Abia", "Adamawa", "Akwa Ibom","Anambra","Bauchi","Bayelsa","Benue","Borno","Cross River","Delta","Ebonyi","Edo",
                    "Ekiti","Enugu","Gombe","Imo","Jigawa","Kaduna","Kano","Katsina","Kebbi","Kogi","Kwara","Lagos", "Mainland", "Island", "Lekki",
                    "Nasarawa","Niger","Ogun","Ondo","Osun","Oyo","Plateau","Rivers","Sokoto","Taraba","Yobe","Zamfara"]
            #ocr_text
        for i in states:
            for x in ocr_text:
                if x.find(i) > 0:
                    test = x
                    break

        return test.lstrip(), phone_no[0]

    for filename in os.listdir(input_path):
        if any([filename.endswith(x) for x in [".png","jpg"]]):
            print(os.path.join(input_path, filename))
            res = json.loads(extract_text(os.path.join(input_path, filename)).text)
            df = pd.json_normalize(res["receipts"][0]["items"])
            #ocr_text = res["receipts"][0]["ocr_text"].split("\n")#" ".join(res["receipts"][0]["ocr_text"].split("\n")[0:10])
            address, phone_no = get_address_phone(res["receipts"][0]["ocr_text"].split("\n"))
            df["date"], df["merchant_name"], df["merchant_address"], df["address"], df["merchant_phone"] = \
                res["receipts"][0]["date"], res["receipts"][0]["merchant_name"], res["receipts"][0]["merchant_address"], address, phone_no
            df = df[["date","merchant_name","description","amount","qty", "unitPrice","merchant_address", "address","merchant_phone"]]
            df = df[df["amount"] > 0.0]
            df["no"] = df.index
            df.to_csv(f"./data/tmp_processed_csv/file_{file_id}_{num}.csv", index=False) #
            shutil.move(os.path.join(input_path, filename), target)
            #os.remove()
            num += 1
            time.sleep(1)
