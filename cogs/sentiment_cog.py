from discord.ext import commands

COG_VERSION = "1.0"

POSITIVE = {"good", "great", "awesome", "love", "nice", "fantastic", "happy"}
NEGATIVE = {"bad", "terrible", "hate", "awful", "sad", "horrible", "angry"}


class SentimentCog(commands.Cog):
    """Very basic vibe check."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="vibecheck")
    async def vibecheck(self, ctx, *, text: str):
        words = set(text.lower().split())
        score = len(words & POSITIVE) - len(words & NEGATIVE)
        if score > 0:
            vibe = "Positive :smiley:"
        elif score < 0:
            vibe = "Negative :frowning:"
        else:
            vibe = "Neutral :neutral_face:"
        await ctx.send(vibe)


async def setup(bot: commands.Bot):
    await bot.add_cog(SentimentCog(bot))
