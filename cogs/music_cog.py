import discord
from discord.ext import commands
import yt_dlp
import asyncio
import requests
from bs4 import BeautifulSoup
from typing import Dict, List

from . import PACKAGE_VERSION as COG_VERSION


class MusicCog(commands.Cog):
    """Basic music playback commands with queue support. Version 1.6."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.queues: Dict[int, List[dict]] = {}

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

    async def play_next(self, ctx):
        guild_id = ctx.guild.id
        voice = ctx.voice_client
        queue = self.queues.get(guild_id)
        if not queue:
            if voice and voice.is_connected():
                await ctx.send("Queue ended.")
            return
        next_track = queue.pop(0)
        source = await discord.FFmpegOpusAudio.from_probe(next_track["url"])
        voice.play(
            source,
            after=lambda _: self.bot.loop.create_task(self.play_next(ctx)),
        )
        await ctx.send(f"Now playing: {next_track.get('title', 'unknown')}")

    @commands.command()
    async def play(self, ctx, url: str):
        """Queue a YouTube URL or playlist."""
        voice = await self.ensure_voice(ctx)
        if not voice:
            return

        guild_id = ctx.guild.id
        queue = self.queues.setdefault(guild_id, [])
        ydl_opts = {"format": "bestaudio", "quiet": True}

        def _extract() -> dict:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=False)

        info = await asyncio.to_thread(_extract)

        if "entries" in info:
            for entry in info["entries"]:
                queue.append({"url": entry["url"], "title": entry.get("title")})
            await ctx.send(f"Added {len(info['entries'])} songs to the queue.")
        else:
            queue.append({"url": info["url"], "title": info.get("title")})
            await ctx.send(f"Queued: {info.get('title', 'unknown')}")

        if not voice.is_playing():
            await self.play_next(ctx)

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

    @commands.command(name="next")
    async def next_song(self, ctx):
        """Skip to the next song in the queue."""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        await self.play_next(ctx)

    @commands.command(name="queue")
    async def queue_list(self, ctx):
        """Display the upcoming songs."""
        queue = self.queues.get(ctx.guild.id, [])
        if not queue:
            await ctx.send("Queue is empty.")
            return
        msg = "Upcoming songs:\n" + "\n".join(
            f"{idx + 1}. {item.get('title', 'unknown')}"
            for idx, item in enumerate(queue)
        )
        await ctx.send(msg)

    @commands.command()
    async def stop(self, ctx):
        """Stop playback and disconnect."""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        self.queues.pop(ctx.guild.id, None)
        await ctx.send("Disconnected.")


async def setup(bot: commands.Bot):
    await bot.add_cog(MusicCog(bot))
