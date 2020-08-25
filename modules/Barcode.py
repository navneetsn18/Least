import requests
def getDataFromBarCode(barcode):
    url = "https://api.upcitemdb.com/prod/trial/lookup?upc=" + str(barcode)
    request = requests.get(url)
    try:
        # return request.json()['items'][0]['title']
        return request.json()
    except :
        return "Not Found"
