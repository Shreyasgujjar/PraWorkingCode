@app.route("/create_files", methods = ['POST'])
def createFiles():
	PostData = request.json
	templateAttr = PostData.get("struct")
	g = Github(PostData.get("username"), PostData.get("password"))
	user = g.get_user()
	repo = g.get_repo("Shreyasgujjar/example0")
	try:
		for item in templateAttr:
			print(item + " ")
			if type(templateAttr.get(item)) is dict:
				itemsInsideFolder = templateAttr.get(item)
				for items in itemsInsideFolder:
					if type(templateAttr.get(items)) is str:
						repo.create_file(item+"/"+itemsInsideFolder.get(items), "test", "")
						print("file " + itemsInsideFolder.get(items) + " is created")
				print("------------------Folder is created-----------------------")
			else:
				repo.create_file(templateAttr.get(item), "test", "test")
				print("file " + templateAttr.get(item) + " is created")
			print("-"*10)
		print("peace")
	except GithubException as e:
		return "There was some error creating the files " + str(e)
	db = firebase.database()
	db.child(PostData.get("repoName").split("/")[1]).set(templateAttr)
	return "The necessary file is created"
