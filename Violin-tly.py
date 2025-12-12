import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import yt_dlp

BOT_TOKEN = "..."

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
    print("Bot is now online!")

@bot.command()
async def join(ctx):
    """Bot joins the user's voice channel."""
    if ctx.author.voice is None:
        await ctx.send("You must be in a voice channel first.")
        return

    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send("I joined your voice channel.")

@bot.command()
async def play(ctx, url: str):
    """Plays audio from a YouTube URL."""
    if ctx.voice_client is None:
        if ctx.author.voice is None:
            await ctx.send("Join a voice channel first.")
            return
        await ctx.author.voice.channel.connect()

    voice_client = ctx.voice_client

    if voice_client.is_playing():
        voice_client.stop()

    try:
        info = ytdlp.extract_info(url, download=False)
        audio_url = info["url"]

        audio_source = FFmpegPCMAudio(audio_url)
        voice_client.play(audio_source)

        await ctx.send("Playing your audio!")
    except Exception:
        await ctx.send("I could not play that link.")

@bot.command()
async def stop(ctx):
    """Stops the currently playing audio."""
    if ctx.voice_client is None:
        await ctx.send("I am not in a voice channel.")
        return

    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("I stopped the audio.")
    else:
        await ctx.send("No audio is currently playing.")

@bot.command()
async def leave(ctx):
    """Bot leaves the voice channel."""
    if ctx.voice_client is None:
        await ctx.send("I am not in a voice channel.")
        return

    await ctx.voice_client.disconnect()
    await ctx.send("I left the voice channel.")

bot.run(BOT_TOKEN)
