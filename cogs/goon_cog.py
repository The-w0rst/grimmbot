import random
from discord.ext import commands

COG_VERSION = "1.4"


class GoonCog(commands.Cog):
    """Group lines from all bots together. Version 1.4."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.greetings = [
            "Grimm grumbles, Bloom cheers and Curse hisses: the goons arrive!",
            "The squad assembles – Bloom waves, Grimm nods and Curse flicks his tail.",
            "You summoned all of us! Expect chaos and hugs... and hissing.",
        ]
        self.reactions = [
            "All three chatter at once, making an utter mess of the chat.",
            "Grimm sighs, Bloom giggles, Curse paws at you. Goon squad energy!",
            "The room suddenly feels crowded with goons.",
        ]

    @commands.command()
    async def greetall(self, ctx):
        """Greet from the entire goon squad."""
        await ctx.send(random.choice(self.greetings))

    @commands.command()
    async def goonsay(self, ctx, *, text: str):
        """Echo a message with squad flair."""
        await ctx.send(f"Grimm, Bloom and Curse chant together: {text}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        lowered = message.content.lower()
        if any(k in lowered for k in ("goons", "squad")) and random.random() < 0.2:
            await message.channel.send(random.choice(self.reactions))


async def setup(bot: commands.Bot):
    await bot.add_cog(GoonCog(bot))
