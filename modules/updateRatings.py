import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from collections import Counter
import csv

cred = credentials.Certificate('./data/least1-firebase-adminsdk-7ymjw-af9148c4b8.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection(u'user').get()

def updateRatingNow():
    print("Process Started...")
    # Use a service account
    with open('./data/ratings.csv','w',newline='') as file:
        write = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write.writerow(['userId', 'item','rating'])
        for userId in doc_ref:
            doc = db.collection(u'user').document(userId.id).collection("history").get()
            customer_history=list()
            for i in doc:
                customer_history.append(i.to_dict()["item"].title())
                product_count=Counter(customer_history)
            for i in product_count:
                write = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                write.writerow([userId.id,i.lower(),product_count[i]*10/len(product_count)])
        print("Completed...")