
import discord 
import asyncio
import random 
import requests 
from discord.utils import get 
import re 
import json

with open("config.txt") as f:
	TOKEN = f.read().strip()

client = discord.Client()

async def get_emoji(name):
	for i in client.get_all_emojis():
		#print(i.name)
		if name in i.name:
			return i
	print(name)
	print("PANIC")	

@client.event
async def on_message(message):
	try:
		# we do not want the bot to reply to itself
		if message.author == client.user:
			return

		content = message.content.lower()
		if "oof" in content and not ":oof:" in content:
			await client.add_reaction(message,await get_emoji("oof"))

		elif ("kerrie" in content or "kerry" in content or "carry" in content or "otto" in content) and not ":kerrie:" in content:
			await client.add_reaction(message,"🇰")
			await client.add_reaction(message,"🇪")
			await client.add_reaction(message,"🇷")
			await client.add_reaction(message,await get_emoji("kerrier"))
			# await client.add_reaction(message,"®️")
			await client.add_reaction(message,"🇮")
			await client.add_reaction(message,await get_emoji("kerriee"))
			# await client.add_reaction(message,"🇪")

		elif "blob" in content and not ":blob:" in content:
			await client.add_reaction(message, await get_emoji("blob"))

		elif "java" in content and not ":java:" in content:
			await client.add_reaction(message,await get_emoji("java"))

		elif "c++" in content:
			await client.add_reaction(message,await get_emoji("cpp"))	

		elif "python" in content and not ":python:" in content:
			await client.add_reaction(message,await get_emoji("python"))
					
		elif ("js" in content or "javascript" in content) and not ":js:" in content:
			await client.add_reaction(message,await get_emoji("js"))

		elif ("c#" in content or ("c" in content and "sharp" in content)) and not ":csharp:" in content:
			await client.add_reaction(message,await get_emoji("csharp"))

		elif ("amazing" in content or "it depends" in content):
			await client.add_reaction(message, await get_emoji("blueball"))

		elif ("fraud" in content or "fr00d" in content or "copy" in content or "copie" in content) and not ":fr00d:" in content:
			await client.add_reaction(message,await get_emoji("fr00d"))

		if content.startswith(".rank"):
			if message.channel.name == "advent-of-code":
				print(getscores())
				await client.send_message(message.channel,getscores())

		if "bot" not in message.channel.name:
			return


		if content.startswith(".help"):
			await client.send_message(message.channel, "this is koenbot. amazing!")
		
	except Exception as e:
		print(e)
		pass

def getscores():
	try:
		res = requests.get("https://adventofcode.com/2018/leaderboard/private/view/395883.json",cookies={"session": "53616c7465645f5ffe6659953d46f55651eb1b50cdc3173c9903ea6d3b0480cb9da3c9fd2027cc4d609864228ef4fc07"}).json()
	except:
		return "an error occured"
	table = """```
rank    name                    stars  score
"""
	
	for index, value in enumerate(sorted(list(res["members"].values()), key=lambda item:item["local_score"],reverse=True)):
		print(value)
		table += str(index).ljust(8)+str(value["name"]).ljust(24)+str(value["stars"]).ljust(8)+str(value["local_score"]).ljust(8)+"\n"
	table += "```"
	
	return table



def generate_expr():
	a = "jona"
	b = "than"

	infront = ""
	operator = "^"

	def invertandor():
		nonlocal operator,a,b,infront

		if random.choice([True,False]):
			if  a.startswith("¬") and operator == "v":
				a = a[1:]
				operator = "->"

			elif b.startswith("¬") and operator == "^" and infront.startswith("¬"):
				b = b[1:]
				operator = "->"
				infront = infront[1:]
			return

		if operator == "->":
			choice = random.choice([0,1,2,3,4,5,6])
			if choice == 1:
				operator = "v"
				a = "¬" + a
			elif choice == 2:
				operator = "^"
				b = "¬" + b
				infront = "¬" + infront

			elif choice == 3:
				if a.startswith("¬") and b.startswith("¬"):
					if random.choice([True,False]):
						a = a[1:]
						b = b[1:]
						a,b=b,a
					else:
						a = "¬" + a
						b = "¬" + b
						a,b=b,a
				else:
					a = "¬" + a
					b = "¬" + b
					a,b=b,a
			return

		choice = random.choice([0,1,2])

		if choice == 0:
			if a.startswith("¬") and b.startswith("¬") and infront.startswith("¬"):
				a = a[1:]
				b = b[1:]
				infront = infront[1:]
				if operator == "v":
					operator = "^"
				elif operator == "^":
					operator = "v"
			else:
				a = "¬" + a
				b = "¬" + b
				infront += "¬"
				if operator == "v":
					operator = "^"
				elif operator == "^":
					operator = "v"
		elif choice == 1:
			a = "¬" + a
			b = "¬" + b			
			infront += "¬"
			if operator == "v":
				operator = "^"
			elif operator == "^":
				operator = "v"

	while random.choice([True,True,True,True,True,True,True,True,True,False]):
		invertandor()

	while infront.startswith("¬¬¬¬¬"):
		infront = infront[2:]

	while a.startswith("¬¬¬¬¬"):
		a = a[2:]
	while b.startswith("¬¬¬¬¬"):
		b = b[2:]

	name = "(" + infront + "(" + a + " " + operator + " " + b + ")" + ")"
	return name


@client.event
async def on_ready():
	texchannels = []
	members = []
	servers = []
	general = None
	for server in client.servers:
		servers.append(server)
		for channel in server.channels:
			if str(channel.type) == "text":
				texchannels.append(channel)
				if "club" in channel.name:
					general = channel
		for member in server.members:
			members.append(member)

	#await client.send_message(general,"pr(oof)")

	creator = None
	elmedint = None
	bot = None

	for i in members:
		if i.id == "131399667442384896":
			creator = i
		elif i.id == "507492645195743252":
			bot = i 
		elif i.id == "481464825776570368":
			elmedin = i

	await client.change_nickname(bot, "(.)koenbot")

	# role = get(bot.server.roles, name="Beta")
	# await client.add_roles(bot, role)

	print('koenbot started')

	def randomcapitalize(x):
		return "".join((i.upper() if random.choice([True,False]) else i for i in x))

	async def amazing():
		while True:
			await asyncio.sleep(10)
			
			#await client.change_nickname(elmedin,randomcapitalize("doctor"))
			newnick = generate_expr()
			await client.change_nickname(creator, newnick)

			#print("changed to {}".format(newnick))

	await amazing()



client.run(TOKEN)
