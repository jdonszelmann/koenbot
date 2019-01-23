
import discord 
import asyncio
import re 
import namechanger
import reactions
from constants import Constants
import questions



with open("config.txt") as f:
	TOKEN = f.readlines()[0].strip()

Constants.client = discord.Client()

@Constants.client.event
async def on_message(message):
	try:
		# we do not want the bot to reply to itself
		if message.author == Constants.client.user:
			return

		content = message.content.lower()

		await reactions.check_reactions(message)

		await questions.onmessage(message)

		if "bot" not in message.channel.name:
			return


		if content.startswith(".help"):
			await Constants.client.send_message(message.channel, "this is koenbot. amazing!")
		
	except Exception as e:
		print(e)
		pass


async def every10sec():
	while True:
		newnick = namechanger.generate_expr("jona","than")
		try:
			await Constants.client.change_nickname(
				Constants.membersbyid["131399667442384896"][0],
				newnick
			)
		except KeyError:
			exit("keyerror id not found")

			print("changed to {}".format(newnick))
		await asyncio.sleep(10)

async def every5sec():
	while True:
		await asyncio.sleep(5)

async def every30sec():
	while True:
		await asyncio.sleep(30)

async def every60sec():
	while True:
		await asyncio.sleep(60)

@Constants.client.event
async def on_ready():
	global members,servers,general,creator,bot,texchannels

	questions.init()

	print("retrieving server info")
	for server in Constants.client.servers:
		Constants.servers[server.name] = server
		for channel in server.channels:
			if str(channel.type) == "text":
				Constants.texchannels[(channel.name,server.name)] = channel
		for member in server.members:
			if member.name in Constants.membersbyname:
				Constants.membersbyname[member.name][1].append(server)
			else:
				Constants.membersbyname[member.name] = [member,[server]]

			if member.name in Constants.membersbyid:
				Constants.membersbyid[member.id][1].append(server)
			else:
				Constants.membersbyid[member.id] = [member,[server]]
	print("starting...")

	#await client.send_message(general,"pr(oof)")

	try:
		await Constants.client.change_nickname(Constants.membersbyid["507492645195743252"][0], "(.)koenbot")
	except KeyError:
		exit("keyerror id not found")

	# role = get(bot.server.roles, name="Beta")
	# await client.add_roles(bot, role)

	print('koenbot started')

	loop = asyncio.get_event_loop()
	task = loop.create_task(every60sec())
	task = loop.create_task(every30sec())
	task = loop.create_task(every10sec())
	task = loop.create_task(every5sec())


Constants.client.run(TOKEN)
