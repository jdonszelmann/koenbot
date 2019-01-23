from constants import Constants
import os
import threading
import http.server
import socketserver
import json
import traceback

path = os.path.dirname(os.path.abspath(__file__))
with open("config.txt") as f:
	lines = f.readlines()
	baseurl = lines[1].strip()
	PORT = int(lines[2].strip())

def escape(msg):
	if type(msg) == str:
		return msg.replace(
			"\"","\\\""
		).replace(
			"\'","\\\'"
		).replace(
			"`","\\`"
		).replace(
			"<","&lt"
		).replace(
			">","&gt"
		)
	return msg

def serverproc():
	os.chdir(os.path.join(path,"serverfiles"))
	Handler = http.server.SimpleHTTPRequestHandler

	def do_POST(self):
		data = self.rfile.read(int(self.headers['Content-Length']))
		if type(data) == bytes:
			data = data.decode("utf-8")

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

			self.send_response(200)
			self.send_header('Content-type', 'application/json; charset=UTF-8')
			self.end_headers()

			self.wfile.write(json.dumps({
				"location":'index.html'.format(baseurl)
			}).encode("utf-8"))
			return

		except Exception as e:
			traceback.print_exc()

			self.send_response(200)
			self.send_header('Content-type', 'application/json; charset=UTF-8')
			self.end_headers()

			self.wfile.write(json.dumps({
				"location":'error.html'.format(baseurl)
			}).encode("utf-8"))

			return


	Handler.do_POST = do_POST

	httpd = socketserver.TCPServer(("", PORT), Handler)
	print("serving at port", PORT)
	httpd.serve_forever()

def init():
	threading.Thread(target=serverproc,daemon=True).start()
	try:
		for i in os.listdir(os.path.join(path,"serverfiles","questions")):
			print("removing {}".format(i))
			if os.path.isfile(os.path.join(path,"serverfiles","questions",i)):
				os.remove(os.path.join(path,"serverfiles","questions",i))
	except FileNotFoundError:
		os.mkdir(os.path.join(path,"serverfiles","questions"))


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
								escape(i.content),
								escape(i.id),
								escape(i.author.name),
								escape(i.author.id),
								escape(message.channel.name),
								escape(message.channel.id),
								escape(questionnumber),
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
				) + "\nhttp://{}/questions/q{}.html".format(
					"192.168.2.12:8800",
					str(questionnumber)
				)
			)

	if message.channel.id in Constants.last50msgs:
		Constants.last50msgs[message.channel.id].append(message)
		while len(Constants.last50msgs[message.channel.id]) > 50:
			Constants.last50msgs[message.channel.id].pop(0)
	else:
		Constants.last50msgs[message.channel.id] = [message]
