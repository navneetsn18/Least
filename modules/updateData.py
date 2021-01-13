import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from collections import Counter
import csv

cred = credentials.Certificate('./data/least1-firebase-adminsdk-7ymjw-af9148c4b8.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection(u'user').get()

def updateDataNow():
    print("Process Started...")
    dataset=set()
    with open('./data/itemdata.csv','w',newline='') as file:
        write = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write.writerow(['itemId', 'item'])
        for userId in doc_ref:
            doc = db.collection(u'user').document(userId.id).collection("history").get()
            products=list()
            for i in doc:
                products.append(i.to_dict()["item"].lower())
            for j in products:
                dataset.add(j)
        dataset=sorted(list(dataset))
        for i in enumerate(dataset):
            write = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            write.writerow([i[0]+1,i[1]])

    with open('./data/ratings.csv','w',newline='') as file:
        write = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write.writerow(['userId', 'item','rating'])
        for userId in doc_ref:
            doc = db.collection(u'user').document(userId.id).collection("history").get()
            customer_history=list()
            for i in doc:
                customer_history.append(i.to_dict()["item"].lower())
                product_count=Counter(customer_history)
            for i in product_count:
                write = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                write.writerow([userId.id,i,product_count[i]*10/len(product_count)])
        print("Completed...")