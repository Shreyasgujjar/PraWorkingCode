from flask import Flask, request
from twilio.rest import Client
from github import Github, GithubException

app = Flask(__name__)
# contents = repo.get_commits_traffic(per="week")
sid = "AC3de35d6b4b5246a899bade4f33c1fe8b"
token = "816d65fc8f364d4b1acdb0f4fec59765"

client = Client(sid, token)

fromWhatsApp = "whatsapp:+14155238886"
toWhatsApp = "whatsapp:+918050825266"

@app.route("/", methods = ['POST'])
def sampleCallMessage():
	data = request.data
	print(data)
	return "hello world"

@app.route("/sendViewTraffic", methods = ['GET'])
def sendViewTraffic():
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

if __name__ == "__main__":
	app.run(debug = True)

