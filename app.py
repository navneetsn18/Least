from modules.AzureScan import *
from modules.Barcode import *
from modules.Img2Pdf import *
from modules.Downloadata import *
from flask import Flask,request,jsonify
import time
import os

app = Flask(__name__)

@app.route('/api/barcode',methods=['GET'])
def renderBarData():
    barcode=str(request.args['Query'])
    return jsonify({'item' : getDataFromBarCode(barcode)["items"][0]['title']})

@app.route('/api/imagescan',methods=['GET'])
def renderReciptData():
    result={}
    imagePath=str(request.args['Query'])
    downloadImage(imagePath)
    print("Data Downloaded..")
    makePDF(imagePath)
    os.remove(imagePath)
    data = makeJSON()
    n = len(data["analyzeResult"]["documentResults"][0]["fields"]["Items"]["valueArray"])
    for i in range(n):
        result[i] = data["analyzeResult"]["documentResults"][0]["fields"]["Items"]["valueArray"][i]["valueObject"]['Name']["text"]
    return jsonify(result)

@app.route('/')
def landing():
    return "Happy to serve you"

if __name__ == "__main__":
    app.run(debug=True,port=int(os.environ.get('PORT',5000)))