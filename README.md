# CIS1051FinalProject
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import yt_dlp
BOT_TOKEN = "MTQ0NzcwMDA3MTIyNjU0MDEzNQ.GkrC7I.gAWIEEiX3qSC4jsiOMgex5OZaRVWduf4q-nPmQ"
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
ytdlp_options = {
    "format": "bestaudio/best",
    "quiet": True,
    "noplaylist": True
}

ytdlp = yt_dlp.YoutubeDL(ytdlp_options)

@bot.event
async def on_ready():
    print("Bot is online! You can now use the commands.")

@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("You must be in a voice channel first.")
        return

    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send("I joined your voice channel.")

@bot.command()
async def play(ctx, url: str):
    if ctx.voice_client is None:
        if ctx.author.voice is None:
            await ctx.send("Join a voice channel and try again.")
            return
        else:
            await ctx.author.voice.channel.connect()

    voice_client = ctx.voice_client

    if voice_client.is_playing():
        voice_client.stop()

    try:
        info = ytdlp.extract_info(url, download=False)
        audio_url = info["url"]

        audio_source = FFmpegPCMAudio(audio_url)

        voice_client.play(audio_source)

        await ctx.send("Playing the requested audio link.")
    except Exception as error:
        await ctx.send("I could not play that link.")

@bot.command()
async def stop(ctx):
    if ctx.voice_client is None:
        await ctx.send("I am not in a voice channel.")
        return

    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("I stopped the music.")
    else:
        await ctx.send("There is no music playing.")

async def leave(ctx):
    if ctx.voice_client is None:
        await ctx.send("I am not in a voice channel.")
        return

    await ctx.voice_client.disconnect()
    await ctx.send("I left the voice channel.")

bot.run("MTQ0NzcwMDA3MTIyNjU0MDEzNQ.GkrC7I.gAWIEEiX3qSC4jsiOMgex5OZaRVWduf4q-nPmQ")



https://github.com/user-attachments/assets/67c1f7ae-076c-4447-af25-525f79c18b39
