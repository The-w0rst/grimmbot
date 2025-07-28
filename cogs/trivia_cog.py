import random
import asyncio
from discord.ext import commands

COG_VERSION = "1.1"


class TriviaCog(commands.Cog):
    """Simple trivia game. Version 1.1."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.questions = [
            {"question": "What is the capital of France?", "answer": "paris"},
            {"question": "Who wrote '1984'?", "answer": "george orwell"},
            {"question": "What is the smallest prime number?", "answer": "2"},
            {"question": "Which planet is known as the Red Planet?", "answer": "mars"},
        ]

    @commands.command()
    async def trivia(self, ctx):
        """Ask a random trivia question and wait for an answer."""
        qa = random.choice(self.questions)
        await ctx.send(qa["question"])

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        try:
            msg = await self.bot.wait_for("message", timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(f"Time's up! The answer was **{qa['answer']}**.")
        else:
            if msg.content.lower().strip() == qa["answer"]:
                await ctx.send("Correct!")
            else:
                await ctx.send(f"Nope! The answer was **{qa['answer']}**.")

    @commands.command(name="addtrivia")
    @commands.is_owner()
    async def add_trivia(self, ctx, *, qa: str):
        """Add a new trivia question. Use `question | answer` format."""
        if "|" not in qa:
            await ctx.send("Format should be: question | answer")
            return
        question, answer = [part.strip() for part in qa.split("|", 1)]
        self.questions.append({"question": question, "answer": answer.lower()})
        await ctx.send("Trivia question added.")


async def setup(bot: commands.Bot):
    await bot.add_cog(TriviaCog(bot))
