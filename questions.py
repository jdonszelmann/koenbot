from constants import Constants
import os
import threading
import http.server
import socketserver
import json

path = os.path.dirname(os.path.abspath(__file__))
baseurl = "localhost:80"

def serverproc():
	PORT = 80

	os.chdir(os.path.join(path,"serverfiles"))
	Handler = http.server.SimpleHTTPRequestHandler

	def do_POST(self):
		data = self.rfile.read(int(self.headers['Content-Length']))


		try:
			jsondata = json.loads(data)

			print("POST")

			with open(os.path.join(path,"serverfiles","questions.json")) as f:
				currentjson = json.load(f)

			selected = list(filter(lambda i:i["selected"], jsondata["messages"]))

			if len(selected) > 0:
				currentjson.append({
					"questions":selected,
					"channel":selected[0]["channelname"],
					"name":jsondata["name"]
				})


				with open(os.path.join(path,"serverfiles","questions.json"), "w") as f:
					json.dump(currentjson,f,indent=2)
			else:
				pass

			self.wfile.write(json.dumps({
				"location":'http://{}/index.html'.format(baseurl)
			}).encode("utf-8"))
			self.send_response(200)
			self.end_headers()
			return

		except Exception as e:
			print(e)

			self.wfile.write(json.dumps({
				"location":'http://{}/error.html'.format(baseurl)
			}).encode("utf-8"))
			self.send_response(200)
			self.end_headers()

			return


	Handler.do_POST = do_POST

	with socketserver.TCPServer(("", PORT), Handler) as httpd:
		print("serving at port", PORT)
		httpd.serve_forever()

def init():
	threading.Thread(target=serverproc,daemon=True).start()

	for i in os.listdir(os.path.join(path,"serverfiles","questions")):
		print("removing {}".format(i))
		if os.path.isfile(os.path.join(path,"serverfiles","questions",i)):
			os.remove(os.path.join(path,"serverfiles","questions",i))



async def onmessage(message):

	content = message.content.lower()

	if content.startswith(".question"):
			with open(os.path.join(path,"serverfiles","template.html")) as f:
				template = f.read()

			questionnumber = Constants.questioncounter
			Constants.questioncounter += 1

			if message.channel.id in Constants.last50msgs:
				newfile = template.replace(
					"XXXXXXXXXXXXXXXXXXXXX",
					",".join((
							"{" + "content:\"{}\",id:\"{}\",author:\"{}\",authorid:\"{}\",channelname:\"{}\",channelid:\"{}\",selected:false,qid:\"{}\"".format(
								i.content,
								i.id,
								i.author.name,
								i.author.id,
								message.channel.name,
								message.channel.id,
								questionnumber,
							) + "}"
							for i in Constants.last50msgs[message.channel.id]
						))
				)
			else:
				newfile = template.replace(
					"XXXXXXXXXXXXXXXXXXXXX",""
				)


			with open(
				os.path.join(
					path,
					"serverfiles",
					"questions",
					"q" + str(questionnumber) + ".html"
				), "w") as f:
				f.write(newfile)

	
			await Constants.client.send_message(
				message.channel,
				"http://{}/questions/q{}.html".format(
					baseurl,
					str(questionnumber)
				)
			)

	if message.channel.id in Constants.last50msgs:
		Constants.last50msgs[message.channel.id].append(message)
		while len(Constants.last50msgs[message.channel.id]) > 50:
			Constants.last50msgs[message.channel.id].pop(0)
	else:
		Constants.last50msgs[message.channel.id] = [message]
