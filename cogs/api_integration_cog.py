import json
import requests
from discord.ext import commands

COG_VERSION = "1.0"


class ApiIntegrationCog(commands.Cog):
    """Simple wrapper for external API requests."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def apiget(self, ctx, url: str):
        """Fetch JSON from a URL and display it."""
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            text = json.dumps(data, indent=2)[:1900]
            await ctx.send(f"```json\n{text}\n```")
        except Exception:
            await ctx.send("Failed to fetch data.")


async def setup(bot: commands.Bot):
    await bot.add_cog(ApiIntegrationCog(bot))
