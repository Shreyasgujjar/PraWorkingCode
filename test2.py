import pyrebase

config = {
  "apiKey": "AIzaSyAvbcA36dCFDGs8r8OpvdfLVl-Unh9CCT4",
    "authDomain": "commuteapp-90b42.firebaseapp.com",
    "databaseURL": "https://commuteapp-90b42.firebaseio.com",
    "projectId": "commuteapp-90b42",
    "storageBucket": "commuteapp-90b42.appspot.com",
	"serviceAccount": "./commuteapp-90b42-firebase-adminsdk-ct2h6-926c224be6.json"
}

firebase = pyrebase.initialize_app(config)

data =  {
	"folder_1": {
		"file_1": "Readme.txt",
		"file_2": "sample.java",
		"file_3": "repo.java",
		"folder_1": {
			"file_1": "helloworld.java"
		}
	}, "folder_2": {
		"file_1": "sample.xml",
		"file_2": "peace.xml"
	}, "file_1": "chill.xml",
	"file_2": "repo.xml",
	"file_3": "helloworld.xml"
}
db = firebase.database()
db.child("agents").set({"shreyas/shreyas/shreyas": "hello"})