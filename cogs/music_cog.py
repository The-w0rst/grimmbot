import discord
from discord.ext import commands
import yt_dlp
import os
import random
import asyncio
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class MusicCog(commands.Cog):
    """Basic music playback commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        load_dotenv("config/goon.env")
        self.playlist_url = os.getenv("SPOTIFY_PLAYLIST_URL")
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        if client_id and client_secret:
            self.spotify = spotipy.Spotify(
                auth_manager=SpotifyClientCredentials(
                    client_id=client_id, client_secret=client_secret
                )
            )
        else:
            self.spotify = None

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

    @commands.command(name="playlist")
    async def playlist(self, ctx):
        """Shuffle and play the configured Spotify playlist."""
        if not self.spotify or not self.playlist_url:
            await ctx.send("Spotify credentials are not configured.")
            return

        voice = await self.ensure_voice(ctx)
        if not voice:
            return

        results = self.spotify.playlist_tracks(self.playlist_url)
        tracks = results["items"]
        while results.get("next"):
            results = self.spotify.next(results)
            tracks.extend(results["items"])

        queue = []
        for item in tracks:
            track = item.get("track")
            if not track:
                continue
            artists = ", ".join(a["name"] for a in track.get("artists", []))
            queue.append(f"{track['name']} {artists}")

        random.shuffle(queue)

        for query in queue:
            await ctx.send(f"Up next: {query}")
            ydl_opts = {"format": "bestaudio", "quiet": True, "noplaylist": True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)
                info = info["entries"][0]
                audio_url = info["url"]
            source = await discord.FFmpegOpusAudio.from_probe(audio_url)
            voice.play(source)
            while voice.is_playing():
                await asyncio.sleep(1)

    @commands.command()
    async def stop(self, ctx):
        """Stop playback and disconnect."""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Disconnected.")


async def setup(bot: commands.Bot):
    await bot.add_cog(MusicCog(bot))
