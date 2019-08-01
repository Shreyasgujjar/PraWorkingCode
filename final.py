import pyrebase
from firebase.firebase import FirebaseApplication
import json
from flask import Flask, request, jsonify, render_template
from github import Github, GithubException
import jenkins
import requests
from twilio.rest import Client
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
from requests.auth import HTTPBasicAuth

app = Flask(__name__)
sid = "AC3de35d6b4b5246a899bade4f33c1fe8b"
token = "816d65fc8f364d4b1acdb0f4fec59765"

client = Client(sid, token)
#http://serveo.net/
config = {
  "apiKey": "AIzaSyAvbcA36dCFDGs8r8OpvdfLVl-Unh9CCT4",
    "authDomain": "commuteapp-90b42.firebaseapp.com",
    "databaseURL": "https://commuteapp-90b42.firebaseio.com",
    "projectId": "commuteapp-90b42",
    "storageBucket": "commuteapp-90b42.appspot.com",
	"serviceAccount": "./commuteapp-90b42-firebase-adminsdk-ct2h6-926c224be6.json"
}

firebase = pyrebase.initialize_app(config)

@app.route("/", methods = ['GET', 'POST'])
def renderHomePage():
	return render_template("HomePage.html")

@app.route("/renderLoginAccessPage", methods = ['GET', 'POST'])
def renderLoginAccessPage():
	if request.method == 'POST':
		data = request.form.to_dict()
		print("JSON data: ", data)
		if data.get("username") is not None:
			g = Github(data.get("username"), data.get("password"))
		else:
			try:
				g = Github(data.get("accessToken"))
			except GithubException.BadCredentialsException as e:
				return render_template("Login_AccessToken.html")
			
		print(g)
		user = g.get_user()
		print(user)
		try:
			for repo in g.get_user().get_repos():
				print(repo.name)
		except GithubException as e:
			return render_template("Login_AccessToken.html")
		auth = True
		return render_template('Landing_Page.html')
	return render_template("Login_AccessToken.html")

# c9be439bd0f333037379f4c030b6f5c97f7b0611 accesstoken
@app.route("/authenticate", methods = ['GET','POST'])
def authenticate():
	if request.method == 'POST':
		data = request.form.to_dict()
		print("JSON data: ", data)
		# print("first ", data)
		# data = json.loads(data)
		# print("he;llo ",data)
		if data.get("username") is not None:
			g = Github(data.get("username"), data.get("password"))
		else:
			try:
				g = Github(data.get("accessToken"))
			except GithubException.BadCredentialsException as e:
				return render_template("login.html")
			
		print(g)
		user = g.get_user()
		print(user)
		try:
			for repo in g.get_user().get_repos():
				print(repo.name)
		except GithubException as e:
			return render_template("login.html")
		auth = True

		return render_template('Landing_Page.html')
	return render_template('login.html')

@app.route("/create_repo", methods=['GET', 'POST'])
def createRepo():
	call = True
	if request.method == 'POST':
		if call is True:
			call = False
			requestData = request.form.to_dict()
			print("hello",requestData)
			if "template_name" in requestData:
				temp_data = requestData.get("template_name")
			else:
				temp_data = requestData.get("category_name")
			temp_name_without_dot = ''.join(e for e in temp_data if e.isalnum())
			print(temp_name_without_dot)
			return render_template('createPage.html', mystring = temp_name_without_dot)
		else:
			if requestData.get("username") is not None:
				g = Github(requestData.get("username"), requestData.get("password"))
			else:
				g = Github(requestData.get("accessToken"))
			try:
				g = Github(requestData.get("username"), requestData.get("password"))
				user = g.get_user()
				repo = user.create_repo(requestData.get("repoName"))
				print(repo)
			except:
				return "Hey !! Awesome your repository is created !!! Naaaaaaa I am kidding its already there !!! Please create a new one"

			return "Hey !! Awesome your repository is created !!!"
	return render_template('createTemplate.html')

@app.route("/create_template", methods = ['POST'])
def createTemplate():
	PostData = request.json
	templateAttr = PostData.get("struct")
	db = firebase.database()
	db.child(PostData.get("tempName")).set(templateAttr)
	return "The necessary template is created"

@app.route("/existingTemplate", methods = ['POST','GET'])
def shreyas():
	print("dumb shreyas called")
	return render_template('existing_template.html')

@app.route("/use_Template", methods = ['POST','GET'])
def useTemplate():
	print("use Template")
	return render_template('new_createPage.html')
	

@app.route("/create_files", methods = ['POST','GET'])
def createFiles():
    print("inside create files")

    if request.method == 'POST':
        PostData = request.form.to_dict()

        firebase = FirebaseApplication("https://commuteapp-90b42.firebaseio.com")

        retrieveData = firebase.get("/" + PostData.get("category_name"), None)
        print("h ",type(retrieveData))
        templateAttr = json.dumps(retrieveData)
        templateAttr = json.loads(templateAttr)
        print(type(retrieveData))
        if PostData.get("uname") is not None:
            g = Github(PostData.get("uname"), PostData.get("psw"))
        else:
            g = Github(PostData.get("accessToken"))
        user = g.get_user()
        repo_data = PostData.get("reponame")
        repo_name = ''.join(e for e in repo_data if e.isalnum())
        repo = user.create_repo(repo_name)
        postLink = "http://rgs.serveo.net/createItem?name="+repo_name
        gitLink = "https://github.com/" + user.login + "/" + repo_name + ".git"
        configXMLFile = open('sample.xml', 'r')
        configXMLReplacedFile = configXMLFile.read().replace('https://github.com/Nihaarika98/qwerty.git', gitLink)
        # depth = 1
        try:
            # for item in templateAttr:
            #   print(item + " ")
            #   if type(templateAttr.get(item)) is dict:
            #       itemsInsideFolder = templateAttr.get(item)
            #       for items in itemsInsideFolder:
            #           if type(templateAttr.get(items)) is str:
            #               repo.create_file(item+"/"+itemsInsideFolder.get(items), "test", "")
            #               print("file " + itemsInsideFolder.get(items) + " is created")
            #           else:
            #               depth2 = itemsInsideFolder.get(items)
            #               for item2 in depth2:
            #                   if type(itemsInsideFolder.get(item2)) is str:
            #                       repo.create_file(item+"/"+itemsInsideFolder.get(items)+"/"+depth2.get(item2), "test", "")
            #                       print("file " + itemsInsideFolder.get(items) + " is created")
            #       print("------------------Folder is created-----------------------")
            #   else:
            #       repo.create_file(templateAttr.get(item), "test", "test")
            #       print("file " + templateAttr.get(item) + " is created")
                
            ################################################
            repo.create_file("docker.yaml", "config:\r\n  pre-unit:yes\r\n  post-unit:no\r\n  app:\r\n", "test")       
            for item in templateAttr:
                if type(templateAttr.get(item)) is dict:
                    
                    f1(item,templateAttr.get(item),repo)

                else:
                    repo.create_file(templateAttr.get(item), "test", "test")
                    print("file " + templateAttr.get(item) + " is created")

            print("-"*10)
            # repo.create_file("Docker.yaml", PostData.get("yamlfile"), "test")
            print("peace")


            ################################################
        except GithubException as e:
            return "There was some error creating the files " + str(e)
        # db = firebase.database()
        # db.child(PostData.get("repoName")).set(templateAttr)
        server = jenkins.Jenkins('http://rgs.serveo.net/', username = 'admin', password = "Muffin@98")
        crumbData = json.loads(requests.get('http://rgs.serveo.net/crumbIssuer/api/json', auth=HTTPBasicAuth('admin', 'Muffin@98')).content).get('crumb')
        # print(crumbData)
        dataHead = {'Content-Type': 'text/xml', 'Jenkins-Crumb': crumbData}
        filedata = open('sample.xml', 'r')
        createJenkin = requests.post(postLink, auth=HTTPBasicAuth('admin', 'Muffin@98'), headers = dataHead, data = configXMLReplacedFile)
        server.build_job(repo_name)
        return "The necessary file is created and the github link is - " + gitLink
    return "creating the repo"
	

def removepath(path):
	print("path v = " + path)
	ind = path.rfind("/")
	if "/" not in path:
		return path
	path = path[:ind]
	return path
def f1(path,item,repo):
	for i in item:
		if type(item.get(i)) is str:
			repo.create_file(path+"/"+item.get(i), "test", "test")
			print("file " + item.get(i) + " is created")
		else:
			f1(path+"/"+i,item.get(i),repo)
			path=removepath(path)

# @app.context_processor
# def f2(items):
# 	for i in items:
# 		if type(items.get(i)) is str:
# 			return(items.get(i))
# 		else:
# 			f2(items.get(i))



#sdbvjns

# def createFoldersAndFiles(path):
# 	for item in templateAttr:
# 		print(item + " ")
# 		if type(templateAttr.get(item)) is dict:
# 			itemsInsideFolder = templateAttr.get(item)
# 			for items in itemsInsideFolder:
# 				if type(templateAttr.get(items)) is str:
# 					repo.create_file(item+"/"+itemsInsideFolder.get(items), "test", "")
# 					print("file " + itemsInsideFolder.get(items) + " is created")
# 			print("------------------Folder is created-----------------------")
# 		else:
# 			repo.create_file(templateAttr.get(item), "test", "test")
# 			print("file " + templateAttr.get(item) + " is created")
# 		print("-"*10)

@app.route("/retrieve", methods=['GET'])
def retrieveData():
	firebase = FirebaseApplication("https://commuteapp-90b42.firebaseio.com")
	retrieveData = firebase.get("/Shreyas", None)
	print(dict(retrieveData))
	retrieveData = jsonify(retrieveData)
	print(type(retrieveData))
	return retrieveData
	# return render_template("datadisplay.html",data = firebase.get("/example0", None))

# shreyasshivajirao.pythonanywhere.com.

@app.route("/togglebuttons", methods = ['POST','GET'])
def togglebuttons():
	g = Github('shreyas.shivajirao@gmail.com', "Muffin@98")
	repo = g.get_repo("Shreyasgujjar/nih")
	contents = repo.get_contents("")

	data = ""
	while contents:
		file_content = contents.pop(0)
		if file_content.type != 'dir':
			if ".yaml" in file_content.name:
				data = file_content.decoded_content
				filename = file_content.name
	if request.method == "GET":
		ls = data.decode('utf-8').split("\r\n")
		while '' in ls:
			ls.remove('')
		return render_template("toggle.html", yamldata = str(ls))

	if request.method == "POST":
		ls = []
		if request.method == 'POST' :
			data = request.form.to_dict()
			for keys in data:
				values = data.get(keys)
				ls.append(keys + ":" + values)
			print(ls)
			finalString = ""
			for strings in ls:
				strings += "\r\n"
				finalString += strings
			print(finalString)
			yamlPath = repo.get_contents(filename)
			repo.update_file(yamlPath.path, "data", finalString.encode('utf-8'), yamlPath.sha, branch = "master")
		return render_template('toggle.html')

@app.route("/sendViewTraffic", methods = ['GET'])
def sendViewTraffic():

	fromWhatsApp = "whatsapp:+14155238886"
	toWhatsApp = "whatsapp:+918050825266"
	g = Github("shreyas.shivajirao@gmail.com", "Muffin@98")
	repo = g.get_repo("Shreyasgujjar/agresseion")
	contents = repo.get_views_traffic(per = "week")
	String = ""
	for keys in contents:
		if type(contents.get(keys)) is not list:
			String += keys + " - " + str(contents.get(keys)) + "\n"
		else:
			for elements in contents.get(keys):
				String += str(elements) + "\n"
	client.messages.create(body=String, from_ = fromWhatsApp, to = toWhatsApp)
	return "message sent"

@app.route("/getWhatsapp", methods = ['POST'])
def getWhatsapp():
	data = request.values.get("Body")
	print(data)
	if "Create repo" in data:
		data = data.replace("Create repo ", "")
		print(data)
		createRepo(data)
	if "Get views" in data:
		data = data.replace("Get views ", "")
		print(data)
		getViews(data)
	if "ls" in data:
		ls()
	return "haha"


def createRepo(repoName):
	try:
		fromWhatsApp = "whatsapp:+14155238886"
		toWhatsApp = "whatsapp:+918050825266"
		client.messages.create(body = "Request received, please wait while we process your request", from_ = fromWhatsApp, to = toWhatsApp)
		g = Github("shreyas.shivajirao@gmail.com", "Muffin@98")
		user = g.get_user()
		repo = user.create_repo(repoName)
		print(repo)
		client.messages.create(body = "Repo is created and the git link is - https://github.com/Shreyasgujjar/" + repoName + ".git",
			from_ = fromWhatsApp, to = toWhatsApp)
	except:
		client.messages.create(body = "Error occured", from_ = fromWhatsApp, to = toWhatsApp)
		print("error occured")

	return "Awesome"

def getViews(repoName):
	try:
		g = Github("shreyas.shivajirao@gmail.com", "Muffin@98")
		user = g.get_user()
		repo = g.get_repo("Shreyasgujjar/"+repoName)
		contents = repo.get_views_traffic(per = "week")
		String = ""
		fromWhatsApp = "whatsapp:+14155238886"
		toWhatsApp = "whatsapp:+918050825266"
		print("Contents obtained")
		for keys in contents:
			if type(contents.get(keys)) is not list:
				String += keys + " - " + str(contents.get(keys)) + "\n"
			else:
				for elements in contents.get(keys):
					String += str(elements) + "\n"
		client.messages.create(body=String, from_ = fromWhatsApp, to = toWhatsApp)
	except:
		print("error occured")
	return "message sent"

def ls():
	g = Github("shreyas.shivajirao@gmail.com", "Muffin@98")
	fromWhatsApp = "whatsapp:+14155238886"
	toWhatsApp = "whatsapp:+918050825266"
	string = ""
	try:
		for repo in g.get_user().get_repos():
			string += repo.name + "\n"
			print(repo.name)
		client.messages.create(body=string, from_ = fromWhatsApp, to = toWhatsApp)
	except GithubException as e:
		print("error occured")

if __name__ == '__main__':
	auth = False
	app.run(debug = False)