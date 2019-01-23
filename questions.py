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

		print("POST")

		try:
			jsondata = json.loads(data)
			print(jsondata)

			self.wfile.write(json.dumps({
				"location":'http://{}/index.html'.format(baseurl)
			}).encode("utf-8"))
			self.send_response(200)
			self.end_headers()
			return

		except:

			self.send_header('Content-type', 'application/json')
			self.send_response(200)
			self.end_headers()
			self.wfile.write(json.dumps({
				"location":'http://{}/error.html'.format(baseurl)
			}).encode("utf-8"))

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

			if message.channel.id in Constants.last100msgs:
				newfile = template.replace(
					"XXXXXXXXXXXXXXXXXXXXX",
					",".join((
							"{" + "content:\"{}\",id:\"{}\",author:\"{}\",authorid:\"{}\",channelname:\"{}\",channelid:\"{}\",selected:false".format(
								i.content,
								i.id,
								i.author.name,
								i.author.id,
								message.channel.name,
								message.channel.id,
							) + "}"
							for i in Constants.last100msgs[message.channel.id]
						))
				)
			else:
				newfile = template.replace(
					"XXXXXXXXXXXXXXXXXXXXX",""
				)


			questionnumber = Constants.questioncounter
			Constants.questioncounter += 1
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

	if message.channel.id in Constants.last100msgs:
		Constants.last100msgs[message.channel.id].append(message)
		while len(Constants.last100msgs[message.channel.id]) > 100:
			Constants.last100msgs[message.channel.id].pop(0)
	else:
		Constants.last100msgs[message.channel.id] = [message]
