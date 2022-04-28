import os
import discord
#for database, will be used soon
#from replit import db
#to make a http request to get data from an api
import requests
#for API that returns json
import json
import openai
import logging
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


#get covid cases in united kingdom --- NEED TO FIX
def get_uk_cases():
  response = requests.get("https://api.covid19api.com/live/country/united-kingdom/status/confirmed")
  json_data = json.loads(response.text)
  cases = str(json_data[0]['Cases']) + "  - " + json_data[0]['Country']
  return(cases)

#pull cat images off the cat tumblr images api
def get_cat_images():
  response = requests.get("https://api.thecatapi.com/v1/images/search")
  json_data = json.loads(response.text)
  cat_image = str(json_data[0]['url'])
  return(cat_image)

#ask the bot for a random yes/no reponse + gif --- NEED TO FIX
def get_yesno_images():
  response = requests.get("https://yesno.wtf/api?ref=apilist.fun")
  json_data = json.loads(response.text)
  yesno_image = str(json_data[0]['answer']) + json_data[0]['image']
  return(yesno_image)

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
  print(f'Currently at {len(bot.guilds)} servers!')

  #print servers connected to
  print('Servers connected to:')
  for guild in bot.guilds:
        if {len(bot.guilds)} < 30:
          print("DELTE ME")
          print(guild.name)
        

#for welcome message when somebody joins
@client.event
async def on_member_join(member):
  guild = client.get_guild(969304838330535957)
  channel = guild.get_channel(969304839563644961)
  await channel.send(f'Welcome to the server {member.mention} ! :partying_face:') # Welcome the member on the server
  await member.send(f'Welcome to the {member.guild.name} server, {member.name}!  :partying_face:') # welcome the member on a dm


#@client.event
#async def on_guild_join(guild):
#  channel_ = guild.channels[0]
#  await channel_.send("Hello, Welcome to D6! Try typing 6commands for a list of commands! If there are any issues, msg dynodaan#4984. Thanks.")

#when somebody sends a message
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  #the program

  # to replace msg.content
  msg = message.content

  #say hello if user says hello
  if msg.startswith('6hello'):
    #print("6hello")
    await message.channel.send(message.author.mention + 'Hello!')

  if msg.startswith('6intro'):
    await message.channel.send(message.author.mention + ' Hey there! Im D6, a chatbot designed to help make your Discord experience more fun and engaging! I can do all sorts of things, from talking to you and helping you with your server tasks! Feel free to message me with the keyword: "6", or 6talk if you want to google through me or talk to me! ')
    
  #report covid 19 cases
  if msg.startswith('6cases'):
    return
    #print("6cases")
    cases = get_uk_cases()
    await message.channel.send(message.author.mention + cases)

  #get and show images of cats to the user in discord
  if msg.startswith('6cats'):
    #print("6cats")
    cats = get_cat_images()
    await message.channel.send(message.author.mention)
    await message.channel.send(cats)

  #need to fix
  if msg.startswith('6yesno'):
    return
    yesno = get_yesno_images()
    await message.channel.send(message.author.mention + yesno)

  #commands list
  if msg.startswith('6commands'):
    await message.channel.send(message.author.mention + '')
    await message.channel.send('Hello!')
    await message.channel.send('Commands are..')
    await message.channel.send('6intro, 6hello, 6cases, 6cats, 6talk "words" (this is to talk to the bot), 6yesno, [BROKEN] 6convo hello + 6end (6end is to end convo)')

  #open ai ? https://beta.openai.com/examples/default-friend-chat
  #have a conversation with friend ai
  if msg.startswith('6talk'):
    logging.info('User said to AI: ' + msg[5:])
    #print('User said to AI: ' + msg[5:])
    content = msg.partition(" ")[2]
    response = open_ai(content)
    await message.channel.send(message.author.mention + response)

  
    
  #trigger to have a constant conversation with ai
  if msg.startswith('6convo hello'):
    return
    await message.channel.send("Conversation Started")
    a = True
    #print("Loop activated")
    while a:
      print("loop running")
      if message.author == client.user:
        print("Bot Spoke")
        return
      elif msg.startswith('6end'):
        print("6end")
        await message.channel.send("Conversation Ended")
        a = False
      elif msg.startswith(''):
        #sleep(10)
        print("Responding to user")
        logging.info('User said to AI: ' + msg)
        content = msg.partition(" ")
        response = open_ai(content)
        await message.channel.send(message.author.mention + response)
      
        
      
      






client.run(token)