import pyrebase
config = {
    "apiKey": "AIzaSyB0EJjDQ_MTuvwBq1im8HLfybPT6YKeOQ0",
    "authDomain": "least1.firebaseapp.com",
    "databaseURL": "https://least1.firebaseio.com",
    "projectId": "least1",
    "storageBucket": "least1.appspot.com",
    "messagingSenderId": "823923209815",
    "appId": "1:823923209815:web:a5c9bff5c5f69e38289512",
    "measurementId": "G-PVPGR3CW0C"
  }

def downloadImage(imgName):
  firebase = pyrebase.initialize_app(config)
  storage = firebase.storage()
  path_on_cloud = "images/"+str(imgName)
  storage.child(path_on_cloud).download(imgName)