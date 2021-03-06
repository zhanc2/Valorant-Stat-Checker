import os
import discord
import time
import compStatsGetter
import unratedStatsGetter
from discord.ext import commands
from urllib.request import urlopen, Request


client = commands.Bot(command_prefix="!")
client.remove_command('help')

@client.event
async def on_ready():
  print("Bot is running!\n")
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=" to !help"), status="!help for help", afk=False)

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("You probably forgot to put the episode and act after the name")
  elif isinstance(error, commands.CommandNotFound):
    await ctx.send("You probably spelled a command wrong")
  elif str(error) == "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\nIn embed: Embed size exceeds maximum size of 6000":
    await ctx.send("This player has no data for the gamemode/episode/act that you selected")
  elif str(error) == "Command raised an exception: HTTPError: HTTP Error 451: Unavailable For Legal Reasons":
    await ctx.send("This player hasn't signed in on tracker.gg/valorant yet")
  elif str(error) == "Command raised an exception: HTTPError: HTTP Error 404: Not Found":
    await ctx.send("You misspelled something")
  else:
    print(error, type(error))
    await ctx.send("The account you're trying to look at probably hasn't signed in on tracker.gg/valorant yet or you spelled something wrong")
    pass
  await ctx.send("Use \"!help\" for help")

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}

@client.command()
async def help(ctx):
  embed = discord.Embed(
    title= "Help",
    colour= discord.Colour.green(),
  )
  embed2 = discord.Embed(
    title= "tracker.gg/valorant",
    colour = discord.Colour.red(),
    url="http://tracker.gg/valorant"
  )
  embed.add_field(name="⠀", value= "The command to get someone's stats is **!compStats (the account)** or **!unratedStats (the account)**. It has to be the full account name with the information after the hastag\n**ex: !compStats Shooterdeath#2702** (Tong's account)\nIf the account has a space in it, the entire thing must be in quotes\n**ex: !compStats \"real account#abc\"**", inline = False)
  embed.add_field(name="⠀", value = "\"!compStats\" will get the competitive stats and \"unratedStats\" will get the unrated stats.", inline = False)
  embed.add_field(name=" ", value="You can also put the episode and act after the name in the format: \"e3a3\", or some other numbers. Not having this will just get the info for the current episode and season. Putting \"all\" will get the overall stats across all episodes and acts", inline=False)
  embed.add_field(name="⠀", value= "**Note**: the account you want to look at has to have signed in on tracker.gg/valorant for the account information to be accessible because Riot Games policy is dumb.", inline=False)

  await ctx.send(embed=embed)
  await ctx.send(embed=embed2)

@client.command()
async def compStats(ctx, account: str, episodeAct: str = None):
  startTime = time.time()
  print("Getting Stats for: ", account)

  newAccount = ""
  for char in account:
    if char == "#":
      newAccount += "%23"
    elif char == " ":
      newAccount += "%20"
    else:
      newAccount += char
  link = "https://tracker.gg/valorant/profile/riot/" + newAccount + "/overview"
  linkComp = link + "?playlist=competitive"

  if not episodeAct == None:
    linkComp += get_url_string(episodeAct)

  print("link: ", linkComp)

  compreq = Request(url=linkComp, headers=headers) 
  html = urlopen(compreq).read() 
  compPageHTML = html.decode("utf8")

  fullStats = discord.Embed(
    colour= discord.Colour.blue()
  )
  fullStats.set_author(name=account, icon_url=get_rank_img(compPageHTML))
  fullStats.set_thumbnail(url=get_profile_img(compPageHTML))

  print("Embed ready")

  compstats = compStatsGetter.getCompetitiveStats(compPageHTML)

  fullStats.add_field(name="‎‏‏‎ ‎‎", value=compstats[0], inline=True)
  fullStats.add_field(name="‎‏‏‎ ‎‎", value=compstats[1], inline=True)

  # fullStats.set_footer(text="⠀", icon_url=get_agent_img(compPageHTML))
  # print(fullStats.fields)

  endTime = time.time()
  print("Embed complete, Sending stats to Discord!")
  print("Took: ", endTime-startTime, "seconds\n")

  await ctx.send(embed=fullStats)

@client.command()
async def unratedStats(ctx, account: str, episodeAct: str = None):
  startTime = time.time()
  print("Getting Stats for: ", account)
  
  newAccount = ""
  for char in account:
    if char == "#":
      newAccount += "%23"
    else:
      newAccount += char
  link = "https://tracker.gg/valorant/profile/riot/" + newAccount + "/overview"

  linkUnrated = link + "?playlist=unrated"
  
  if not episodeAct == None:
    linkUnrated += get_url_string(episodeAct)

  print("link: ", linkUnrated)

  unratereq = Request(url=linkUnrated, headers=headers) 
  html = urlopen(unratereq).read() 
  unratedPageHTML = html.decode("utf8")

  fullStats = discord.Embed(
    colour= discord.Colour.purple()
  )
  fullStats.set_author(name=account, icon_url=get_agent_img(unratedPageHTML))
  fullStats.set_thumbnail(url=get_profile_img(unratedPageHTML))

  print("Embed ready")

  unratedStats = unratedStatsGetter.getUnrankedStats(unratedPageHTML)

  fullStats.add_field(name="⠀", value=unratedStats[0], inline=True)
  fullStats.add_field(name="⠀", value=unratedStats[1], inline=True)

  endTime = time.time()
  print("Embed complete, Sending stats to Discord!")
  print("Took: ", endTime-startTime, "seconds\n")

  await ctx.send(embed=fullStats)

def get_url_string(episodeAct: str):
  if episodeAct == "e3a3":
    return("&season=a16955a5-4ad0-f761-5e9e-389df1c892fb")
  elif episodeAct == "e3a2":
    return("?season=4cb622e1-4244-6da3-7276-8daaf1c01be2")
  elif episodeAct == "e3a1":
    return("?season=2a27e5d2-4d30-c9e2-b15a-93b8909a442c")
  elif episodeAct == "e2a3":
    return("?season=52e9749a-429b-7060-99fe-4595426a0cf7")
  elif episodeAct == "e2a2":
    return("?season=ab57ef51-4e59-da91-cc8d-51a5a2b9b8ff")
  elif episodeAct == "e2a1":
    return("?season=97b6e739-44cc-ffa7-49ad-398ba502ceb0")
  elif episodeAct == "e1a3":
    return("?season=46ea6166-4573-1128-9cea-60a15640059b")
  elif episodeAct == "e1a2":
    return("?season=0530b9c4-4980-f2ee-df5d-09864cd00542")
  elif episodeAct == "e1a1":
    return("?season=3f61c772-4560-cd3f-5d3f-a7ab5abda6b3")
  elif episodeAct == "all":
    return("&season=all")
  else:
    return None

def get_profile_img(pageHTML: str):
  a = pageHTML.find("decagon-avatar") + 613
  i = a
  while True:
    i += 1
    if pageHTML[i] == "\"":
      end = i
      break
  return pageHTML[a:end]

def get_rank_img(pageHTML: str):
  a = pageHTML.find("https://trackercdn.com/cdn/tracker.gg/valorant/icons/tiers/")
  i = a
  while True:
    i += 1
    if pageHTML[i] == "\"":
      end = i
      break
  return pageHTML[a:end]

def get_agent_img(pageHTML: str):
  a = pageHTML.find("https://titles.trackercdn.com/valorant-api/agents")
  i = a
  while True:
    i += 1
    if pageHTML[i] == "\"":
      end = i
      break
  return pageHTML[a:end]


client.run(os.getenv('TOKEN'))