
import asyncio
from constants import Constants

async def get_emoji(name):
	for i in Constants.client.get_all_emojis():
		#print(i.name)
		if name in i.name:
			return i
	print("could not find {}".format(name))	
	exit()


async def check_reactions(message):
	content = message.content.lower()
	if "oof" in content and not ":oof:" in content:
		await Constants.client.add_reaction(message,await get_emoji("oof"))

	if ("kerrie" in content or "kerry" in content or "carry" in content or "otto" in content) and not ":kerrie:" in content:
		await Constants.client.add_reaction(message,"🇰")
		await Constants.client.add_reaction(message,"🇪")
		await Constants.client.add_reaction(message,"🇷")
		await Constants.client.add_reaction(message,await get_emoji("kerrier"))
		# await Constants.client.add_reaction(message,"®️")
		await Constants.client.add_reaction(message,"🇮")
		await Constants.client.add_reaction(message,await get_emoji("kerriee"))
		# await Constants.client.add_reaction(message,"🇪")

	if "blob" in content and not ":blob:" in content:
		await Constants.client.add_reaction(message, await get_emoji("blob"))

	if "java" in content and not ":java:" in content:
		await Constants.client.add_reaction(message,await get_emoji("java"))

	if "c++" in content:
		await Constants.client.add_reaction(message,await get_emoji("cpp"))	

	if "python" in content and not ":python:" in content:
		await Constants.client.add_reaction(message,await get_emoji("python"))
				
	if ("js" in content or "javascript" in content) and not ":js:" in content:
		await Constants.client.add_reaction(message,await get_emoji("js"))

	if ("c#" in content or ("c" in content and "sharp" in content)) and not ":csharp:" in content:
		await Constants.client.add_reaction(message,await get_emoji("csharp"))

	if ("amazing" in content or "it depends" in content):
		await Constants.client.add_reaction(message, await get_emoji("blueball"))

	if ("fraud" in content or "fr00d" in content or "copy" in content or "copie" in content) and not ":fr00d:" in content:
		await Constants.client.add_reaction(message,await get_emoji("fr00d"))

	if "ns" in content:
		await Constants.client.add_reaction(message,await get_emoji("nederlandse_stoorwegen"))

	if "eclipse" in content:
		await Constants.client.add_reaction(message,await get_emoji("eclipse"))
