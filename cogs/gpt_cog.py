import os
import openai
from discord.ext import commands

COG_VERSION = "1.3"

# Environment values are read from the parent process
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

SYSTEM_MESSAGES = {
    "Grimm": "You are Grimm, a grumpy but caring skeleton leader. Keep replies short, sarcastic and protective.",
    "Bloom": "You are Bloom, an energetic reaper with a love of musicals and hugs. Speak with lots of enthusiasm and emojis!",
    "Curse": "You are Curse, a mischievous cat. Respond with playful snark and cat-like behavior.",
}


class GPTCog(commands.Cog):
    """Cog that adds a ChatGPT-based chat command and mention replies. Version 1.3."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _system_prompt(self) -> str:
        name = self.bot.user.name if self.bot.user else "GoonBot"
        return SYSTEM_MESSAGES.get(
            name, f"You are {name}, a helpful member of the Goon Squad."
        )

    async def _chatgpt(self, prompt: str) -> str:
        if not OPENAI_API_KEY:
            return "OpenAI API key not configured."
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self._system_prompt()},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=150,
                temperature=0.8,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return "Sorry, I couldn't reach ChatGPT."

    @commands.command(name="chat")
    async def chat(self, ctx, *, prompt: str):
        """Chat with the bot using ChatGPT."""
        reply = await self._chatgpt(prompt)
        await ctx.send(reply)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or self.bot.user not in message.mentions:
            return
        prompt = message.content.replace(self.bot.user.mention, "").strip()
        if not prompt:
            return
        reply = await self._chatgpt(prompt)
        await message.channel.send(reply)


async def setup(bot: commands.Bot):
    await bot.add_cog(GPTCog(bot))
