import os
import discord
#for database, will be used soon
#from replit import db
#to make a http request to get data from an api
import requests
#for API that returns json
import json
import openai
#import logging
from time import sleep

#for Bot+bot stuff - who thought it was a good idea to have bot, bot, Bot all as different tags
prefix = "6"

#import new additions (Bot label and commands.)
from discord.ext import commands
from discord.ext.commands import Bot

#set the prefix with the bot
bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")



intents = discord.Intents.default()
intents.members = True

#bot = commands.Bot(command_prefix='!')


#for member caching
intents = discord.Intents.default()
intents.members = True

#secrets
token = os.environ['discord_bot_token']
ai_key = os.environ['open_ai_key']


#for 6talk and 6convo, the open AI that responds to the user (GTP-3 Best Model)
openai.api_key = ai_key
client = discord.Client(intents=intents)
print("Bot Running")
def open_ai(content):
  response = openai.Completion.create(
  engine="text-davinci-002",
  prompt=content,
  temperature=0.5,
  max_tokens=1000,
  top_p=1.0,
  frequency_penalty=0.5,
  presence_penalty=0.0,
  #stop=[""]
  )
  #print(response)
  json_data = json.loads(str(response)) #(response.text)
  #print(json_data['choices']['text'])
  text = (str(json_data['choices'][0]['text']))
  return text


#pull cat images off the cat tumblr images api
def get_cat_images():
  response = requests.get("https://api.thecatapi.com/v1/images/search")
  json_data = json.loads(response.text)
  cat_image = str(json_data[0]['url'])
  return(cat_image)

#ask the bot for a random yes/no reponse + gif --- Fixed, Assistance by rafidini on Github
def get_yesno_images():
    response = requests.get("https://yesno.wtf/api?ref=apilist.fun")

    # Try to handle non successful GET request
    if response.status_code != 200:
        return None

    # Get response as a dictionary
    json_data = response.json()

    # Return value @image key
    return json_data.get('image')

  #FUTURE ADDITIONS, STORING A DATABASE OF THINGS??? WHAT THINGS?? I DONT KNOW?? SOME THINGS??
#def update_database(message):
#  if "message" is db.key():
#    message = db["message"]


#When the bot is ready, set its status, and then print it's name, discord version, number of servers + servers connected to
@bot.event
@client.event
async def on_ready():
  #print('We have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='over this server | 6commands for a list of commands'))

  #print what bot its logged in as
  print('Logged in as')
  print('{0.user}'.format(client))
  print("Discord Version: " + discord.__version__)
  print('------')
  print(f'Currently at {len(client.guilds)} servers!')

  #print servers connected to
  print('Servers connected to:')
  #print(client.guilds)
  for guild in client.guilds:
        if len(client.guilds) < 30:
          #doesnt actually work
          print(guild.name)
        

#for welcome message when somebody joins
@client.event
async def on_member_join(member):
  user = await client.fetch_user("300635308989612032")
  await user.send(f' {member.name} Joined: {member.guild.name}')
  await user.send('ㅤ')
  #guild = client.get_guild(969304838330535957)
  #channel = guild.get_channel(969304839563644961)
  #await channel.send(f'Welcome to the server {member.mention} ! :partying_face:') # Welcome the member on the server
  await member.send(f' :tada: Welcome to the {member.guild.name} server, {member.name}!  :partying_face:') # welcome the member on a dm

@client.event
async def on_member_remove(member):
  user = await client.fetch_user("300635308989612032")
  await user.send(f' {member.name} Left: {member.guild.name}')
  await user.send('ㅤ')
  await member.send("ㅤ")
  await member.send(f' :wave: Farewell {member.name}, I hope your time in {member.guild.name} has been pleasant!  :cry:') # give a goodbye to the member on a dm
  await member.send("ㅤ")
  await member.send(f' {member.name} If you found this bot to be useful, maybe try it out on your own server? https://discord.com/api/oauth2/authorize?client_id=968592342426730507&permissions=8&scope=bot')
  await member.send("ㅤ")
  await member.send("Otherwise, You can suggest additions to the bot by DM's")
  await member.send("dynodaan#4984")

  


#when somebody sends a message
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if not message.guild:
        await message.channel.send('Hello, I am a bot.')
        await message.channel.send("ㅤ")
        await message.channel.send("I cannot respond to DM's")
        await message.channel.send("ㅤ")
        await message.channel.send("If you have any suggestions, DM the Developer of this bot at:")
        await message.channel.send("dynodaan#4984")


  # to replace msg.content
  msg = message.content

  #say hello if user says hello
  if msg.startswith('6hello'):
    #print("6hello")
    await message.channel.send(message.author.mention + 'Hello!')

  #respond with an introduction to 6intro
  if msg.startswith('6intro'):
    await message.channel.send(message.author.mention + ' Hey there! Im D6, a chatbot designed to help make your Discord experience more fun and engaging! I can do all sorts of things, from talking to you and helping you with your server tasks! Feel free to message me with the keyword: "6", or 6talk if you want to google through me or talk to me! ')
    

  #get and show images of cats to the user in discord
  if msg.startswith('6cats'):
    #print("6cats")
    cats = get_cat_images()
    await message.channel.send(message.author.mention)
    await message.channel.send(cats)

  #responds to the 6yesno by randomly sending a yes or no + a random gif from the api
  if msg.startswith('6yesno'):
    yesno = get_yesno_images()
    await message.channel.send(message.author.mention)
    await message.channel.send(yesno)

  #responds to 6commands by responding explainign what the commadns are
  if msg.startswith('6commands'):
    await message.channel.send(message.author.mention + '')
    await message.channel.send('Hello!')
    await message.channel.send('Commands are..')
    await message.channel.send('6intro, 6hello, 6cats, 6talk "words" (this is to talk to the bot), 6yesno')

  #open ai ? https://beta.openai.com/examples/default-friend-chat
  #have a conversation with friend ai
  if msg.startswith('6talk'):
    #logging.info('User said to AI: ' + msg[5:])
    #print('User said to AI: ' + msg[5:])
    content = msg.partition(" ")[2]
    response = open_ai(content)
    if len(response) < 2000:
      await message.channel.send(message.author.mention + response)
    else:
      await message.channel.send(message.author.mention + "Error | Word Limit is over 2000 characters | Please DM dynodaan#4984 if this continues")




client.run(token)