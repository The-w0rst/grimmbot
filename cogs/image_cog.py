import io
import requests
from PIL import Image, ImageDraw, ImageFont
import discord
from discord.ext import commands

COG_VERSION = "1.0"


class ImageCog(commands.Cog):
    """Basic image editing commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def caption(self, ctx, url: str, *, text: str):
        """Add a caption to an image URL."""
        resp = requests.get(url, timeout=10)
        img = Image.open(io.BytesIO(resp.content))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except Exception:
            font = ImageFont.load_default()
        draw.text((10, 10), text, fill="white", font=font)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        await ctx.send(file=discord.File(buffer, filename="caption.png"))

    @commands.command()
    async def invert(self, ctx, url: str):
        """Invert an image from a URL."""
        resp = requests.get(url, timeout=10)
        img = Image.open(io.BytesIO(resp.content))
        inv = Image.eval(img, lambda x: 255 - x)
        buffer = io.BytesIO()
        inv.save(buffer, format="PNG")
        buffer.seek(0)
        await ctx.send(file=discord.File(buffer, filename="invert.png"))


async def setup(bot: commands.Bot):
    await bot.add_cog(ImageCog(bot))
