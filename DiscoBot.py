import discord
from discord.ext import commands
from youtubesearchpython import VideosSearch

import requests
from datetime import datetime

from requests import get
from json import loads

import youtube_dl

###
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

###
players={}

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '?')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('with rk'))
    print("Bot is ready! Logged on as",client.user)


    

@client.event
async def on_member_join(member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
            await guild.system_channel.send(to_send)

@client.event
async def on_member_remove(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = "Goodbye {0.mention}. You will be missed :(".format(member)
        await guild.system_channel.send(to_send)

@client.command()
async def users(ctx):
    guild = client.get_guild(783699545653510175)
    await ctx.send(f"No. of users = {guild.member_count}")

        
@client.command(name = "p",help="Searches youtube videos")
async def p(ctx,*args):
    word = " ".join(args)
    if (word!=""):
        videosSearch = VideosSearch(word, limit = 2)
        s = videosSearch.result()
        if (s):
            await ctx.send(s["result"][0]["link"])
        else:
            await ctx.send("Song not found! :(")
    else:
        await ctx.send("Enter Song name to search!")


@client.command(name="quote",help="Random quotes generator")
async def quote(ctx):
    response = get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
    await ctx.send('{quoteText} - {quoteAuthor}'.format(**loads(response.text)))

 

@client.command()
async def use(ctx):
    await ctx.send("HELP")


@client.command()
async def w(ctx,*args):
    city = " ".join(args)
    if (city!=""):
        res=requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city+'&APPID=ddd6e280766a9cecafd25d6b3906f25b&units=metric').json()
        if (res['cod']==200):
            s = f">>> ***{city} {res['sys']['country']}***\n\n**Weather**\n{res['weather'][0]['description']}\n\n**Temperature**\n{res['main']['temp']}°C\n\n"
            s+=f"**Atmospheric Pressure**\n{res['main']['pressure']}Pa\n\n**Humidity**\n{res['main']['humidity']}%\n\n**Wind speed**\n{res['wind']['speed']}m/s\n\n**Wind direction**\n{res['wind']['deg']}°\n\n"
            s+=f"**Sun Rise**\n{datetime.utcfromtimestamp(int(res['sys']['sunrise'])).strftime('%H:%M:%S')}\n\n**Sun Set**\n{datetime.utcfromtimestamp(int(res['sys']['sunset'])).strftime('%H:%M:%S')}\n\n**Visibility**\n{res['visibility']}"

            await ctx.send(s)
        else:
            await ctx.send("City not found!")
    else:
        await ctx.send("Enter City to fetch data!")

#####
'''
@client.command(name='play',help = "helps to play music")
async def play(ctx):
    if ctx.message.author.voice:
        channel = ctx.message.author.voice.channel
        
    else:
        
        await ctx.send("Please connect to a voice channel to play music.")
        return

    await channel.connect()
    

@client.command(name='stop',help = "helps to stop music")
async def leave(ctx):
    v_client = ctx.message.guild.voice_client
    await v_client.disconnect()

    
@client.command(pass_context=True)
async def leave(ctx):
    await ctx.voice_client.disconnect()

@client.command(pass_context=True)
async def play(ctx,url):
    server = ctx.message.server
    vc = client.voice_client_in(server)
    player = await vc.create_ytdl_player(url)
    players[server.id] = player
    player.start()
'''


@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


# command to play sound from a youtube URL
@client.command()
async def play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with youtube_dl(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('Bot is playing')

# check if the bot is already playing
    else:
        await ctx.send("Bot is already playing")
        return


# command to resume voice if it is paused
@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('Bot is resuming')


# command to pause voice if it is playing
@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('Bot has been paused')


# command to stop voice
@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('Stopping...')


# command to clear channel messages
@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Messages have been cleared")
    
    
client.run("")

