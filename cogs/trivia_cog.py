import random
import asyncio
from discord.ext import commands

COG_VERSION = "1.5"

NUMBER_WORDS = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
    20: "twenty",
    30: "thirty",
    40: "forty",
    50: "fifty",
    60: "sixty",
    70: "seventy",
    80: "eighty",
    90: "ninety",
    100: "one hundred",
}


def number_to_words(n: int) -> str:
    if n in NUMBER_WORDS:
        return NUMBER_WORDS[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        word = NUMBER_WORDS[tens * 10]
        if ones:
            word += "-" + NUMBER_WORDS[ones]
        return word
    return str(n)


class TriviaCog(commands.Cog):
    """Randomized trivia game with 500 math questions. Version 1.4."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.questions = self._generate_questions(500)
        # add a few fixed general questions
        self.questions.extend(
            [
                {"question": "What is the capital of France?", "answers": ["paris"]},
                {
                    "question": "Who wrote '1984'?",
                    "answers": ["george orwell", "orwell"],
                },
                {
                    "question": "What is the smallest prime number?",
                    "answers": ["2", "two"],
                },
                {
                    "question": "Which planet is known as the Red Planet?",
                    "answers": ["mars"],
                },
            ]
        )

    def _generate_questions(self, count: int):
        questions = []
        operations = ["+", "-", "*"]
        for _ in range(count):
            op = random.choice(operations)
            if op == "+":
                a = random.randint(1, 100)
                b = random.randint(1, 100)
                question = f"What is {a} + {b}?"
                ans = a + b
            elif op == "-":
                a = random.randint(1, 100)
                b = random.randint(0, a)
                question = f"What is {a} - {b}?"
                ans = a - b
            else:
                a = random.randint(1, 12)
                b = random.randint(1, 12)
                question = f"What is {a} * {b}?"
                ans = a * b
            questions.append(
                {"question": question, "answers": [str(ans), number_to_words(ans)]}
            )
        return questions

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
            await ctx.send(f"Time's up! The answer was **{qa['answers'][0]}**.")
        else:
            content = msg.content.lower().strip()
            if any(content == ans for ans in qa["answers"]):
                await ctx.send("Correct!")
            else:
                await ctx.send(f"Nope! The answer was **{qa['answers'][0]}**.")

    @commands.command(name="addtrivia")
    @commands.is_owner()
    async def add_trivia(self, ctx, *, qa: str):
        """Add a new trivia question. Use `question | ans1 ; ans2` format."""
        if "|" not in qa:
            await ctx.send("Format should be: question | answer1 ; answer2")
            return
        question, answers = [part.strip() for part in qa.split("|", 1)]
        answer_list = [a.strip().lower() for a in answers.split(";") if a.strip()]
        if not answer_list:
            await ctx.send("No answers provided.")
            return
        self.questions.append({"question": question, "answers": answer_list})
        await ctx.send("Trivia question added.")


async def setup(bot: commands.Bot):
    await bot.add_cog(TriviaCog(bot))
