########### Python Form Recognizer Async Receipt #############

import json
import time
from requests import get, post
import os

def makeJSON():
    # Endpoint URL
    endpoint = r"https://navneetsn18.cognitiveservices.azure.com/"
    apim_key = "0c860d0a19344acd96b783c83f578ce1"
    post_url = endpoint + "/formrecognizer/v2.0/prebuilt/receipt/analyze"
    source = r"./data/image.pdf"

    headers = {
        # Request headers
        'Content-Type': 'application/pdf, image/jpeg, image/png, image/tiff',
        'Ocp-Apim-Subscription-Key': apim_key,
    }

    params = {
        "includeTextDetails": True
    }

    with open(source, "rb") as f:
        data_bytes = f.read()

    try:
        resp = post(url = post_url, data = data_bytes, headers = headers, params = params)
        if resp.status_code != 202:
            print("POST analyze failed:\n%s" % resp.text)
            quit()
        print("POST analyze succeeded:\n%s" % resp.headers)
        get_url = resp.headers["operation-location"]
    except Exception as e:
        print("POST analyze failed:\n%s" % str(e))
        quit()

    n_tries = 15
    n_try = 0
    wait_sec = 5
    max_wait_sec = 60
    while n_try < n_tries:
        try:
            resp = get(url = get_url, headers = {"Ocp-Apim-Subscription-Key": apim_key})
            resp_json = resp.json()
            if resp.status_code != 200:
                print("GET analyze results failed:\n%s" % json.dumps(resp_json))
                quit()
            status = resp_json["status"]
            if status == "succeeded":
                print("Receipt Analysis succeeded...")
                os.remove("./data/image.pdf")
                return resp_json
                quit()
            if status == "failed":
                print("Analysis failed:\n%s" % json.dumps(resp_json))
                quit()
            # Analysis still running. Wait and retry.
            time.sleep(wait_sec)
            n_try += 1
            wait_sec = min(2*wait_sec, max_wait_sec)     
        except Exception as e:
            msg = "GET analyze results failed:\n%s" % str(e)
            print(msg)
            quit()
    print("Analyze operation did not complete within the allocated time.")