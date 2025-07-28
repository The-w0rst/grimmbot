import discord
from discord.ext import commands
import yt_dlp
import requests
from bs4 import BeautifulSoup

COG_VERSION = "1.1"


class MusicCog(commands.Cog):
    """Basic music playback commands. Version 1.1."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def ensure_voice(self, ctx):
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.send("Connect to a voice channel first.")
            return None
        voice = ctx.voice_client
        if voice is None:
            return await ctx.author.voice.channel.connect()
        if voice.channel != ctx.author.voice.channel:
            await voice.move_to(ctx.author.voice.channel)
        return voice

    @commands.command()
    async def play(self, ctx, url: str):
        """Stream audio from a YouTube URL."""
        voice = await self.ensure_voice(ctx)
        if not voice:
            return
        ydl_opts = {"format": "bestaudio", "quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info["url"]
        source = await discord.FFmpegOpusAudio.from_probe(audio_url)
        voice.play(source)
        await ctx.send(f"Now playing: {info.get('title', 'unknown')}")

    @commands.command()
    async def spotify(self, ctx, url: str):
        """Fetch track info from a Spotify URL and respond creatively."""
        if "spotify" not in url:
            await ctx.send("Please provide a valid Spotify link.")
            return
        try:
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")
            title = soup.title.text
            track = title.split(" | ")[0]
        except Exception:
            await ctx.send("Couldn't fetch that track, but imagine something epic!")
            return
        await ctx.send(f"Pretending to play **{track}** from Spotify. Feel the vibes!")

    @commands.command()
    async def stop(self, ctx):
        """Stop playback and disconnect."""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Disconnected.")


async def setup(bot: commands.Bot):
    await bot.add_cog(MusicCog(bot))
