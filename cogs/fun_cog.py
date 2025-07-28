from discord.ext import commands
import random

COG_VERSION = "1.3"


class FunCog(commands.Cog):
    """Random fun commands like dice rolls and an 8-ball. Version 1.3."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.quotes = [
            "Believe in the me that believes in you!",
            "Chaos is a ladder – climb it with style.",
            "Today is a great day for some shenanigans!",
            "Keep it goofy, keep it grand.",
        ]
        self.ball_responses = [
            "Absolutely yes.",
            "Nope, try again later.",
            "The outlook is hazy...",
            "Without a doubt!",
            "Ask me after a nap.",
            "I'd rather not say.",
        ]

    @commands.command()
    async def roll(self, ctx, sides: int = 6):
        """Roll a dice with the given number of sides."""
        if sides < 2:
            await ctx.send("Dice need at least 2 sides!")
            return
        result = random.randint(1, sides)
        await ctx.send(f"You rolled a {result} (1-{sides}).")

    @commands.command(name="8ball")
    async def eight_ball(self, ctx, *, question: str | None = None):
        """Ask the magic 8-ball a question."""
        if not question:
            await ctx.send("Ask a full question for the 8-ball to ponder.")
            return
        await ctx.send(random.choice(self.ball_responses))

    @commands.command()
    async def coinflip(self, ctx):
        """Flip a coin."""
        await ctx.send(random.choice(["Heads!", "Tails!"]))

    @commands.command()
    async def quote(self, ctx):
        """Share a random motivational quote."""
        await ctx.send(random.choice(self.quotes))


async def setup(bot: commands.Bot):
    await bot.add_cog(FunCog(bot))
