import os
import discord
#for database, will be used soon
#from replit import db
#to make a http request to get data from an api
import requests
#for API that returns json
import json
#import openai

#for member caching
intents = discord.Intents.default()
intents.members = True

token = os.environ['discord_bot_token']
#ai_key = os.environ['open_ai_key']
#openai.api_key = #os.getenv(os.environ['ai_key'])
client = discord.Client()
print("Bot Running")

#response = openai.Completion.create(
#engine="text-davinci-002",
#prompt="I have heard of Open AI, but what is it?",
#temperature=0.5,
#max_tokens=60,
#top_p=1.0,
#frequency_penalty=0.5,
#presence_penalty=0.0,
#stop=[""])



#get covid cases in united kingdom
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

  
#def update_database(message):
#  if "message" is db.key():
#    message = db["message"]
    

#to make it work
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


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
    await message.channel.send('Hello!')
    
  #report covid 19 cases
  if msg.startswith('6cases'):
    #print("6cases")
    cases = get_uk_cases()
    await message.channel.send(cases)

  #get and show images of cats to the user in discord
  if msg.startswith('6cats'):
    #print("6cats")
    cases = get_cat_images()
    await message.channel.send(cases)

  #commands list
  if msg.startswith('6commands'):
    await message.channel.send('Hello!')
    await message.channel.send('Commands are..')
    await message.channel.send('6hello, 6cases, 6cats, 6convo, bye, etc')

  #open ai ? https://beta.openai.com/examples/default-friend-chat
  #have a conversation with friend ai
 # if msg.startswith('6convo'):
    #response


    
  #bye bye! need to find a way to merge the two together, or doesn't work.
  if msg.startswith('bye'):
    #print("bye")
    cases = get_cat_images()
    await message.channel.send("Bye Bye!")

  if msg.startswith('Bye'):
    #print("bye")
    cases = get_cat_images()
    await message.channel.send("Bye Bye!")







client.run(token)