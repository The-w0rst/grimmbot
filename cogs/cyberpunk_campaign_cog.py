import os
import random
import openai
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[1] / "config" / "setup.env"
load_dotenv(ENV_PATH)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


class CyberpunkCampaignCog(commands.Cog):
    """Cyberpunk themed mini DnD campaign with simple character sheets."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.sessions: dict[int, dict[str, int | str]] = {}
        self.opponents = {
            "Grimm": "Grimm cracks his bony knuckles. \"Let's see what you've got.\"",
            "Bloom": "Bloom twirls a neon scythe. \"Time for dramatic heroics!\"",
            "Curse": "Curse hisses, tail lashing. \"I'll scratch more than your ego.\"",
        }
        self.character_prompts = {
            "Grimm": (
                "You are Grimm, a grumpy yet protective skeleton leader. "
                "Respond with short, sarcastic quips."),
            "Bloom": (
                "You are Bloom, an energetic reaper who loves musicals, hugs "
                "and glitter. Speak with enthusiasm and emojis."),
            "Curse": (
                "You are Curse, a mischievous talking cat obsessed with sushi "
                "and playful snark."),
        }
        self.scenarios = [
            (
                "You wander the rain-soaked alleys of **Neon Goon City**. Grimm"
                " steps from the shadows and mutters, 'This city never sleeps.'"
            ),
            (
                "Bloom bursts out of a holo-club singing, 'Adventure waits in"
                " every corner!'"
            ),
            (
                "Curse darts across a flickering sign. 'Break it and you buy it,'"
                " the cat snarls."
            ),
            (
                "A towering vending machine whirs to life, dispensing neon noodles "
                "while Bloom hums a tune and Grimm keeps watch."
            ),
            (
                "You duck into an abandoned arcade. Curse prowls among the dusty "
                "games, eyeing your pockets for snacks."
            ),
        ]

    def _system_prompt(self, author: str, session: dict | None) -> str:
        """Return a system prompt listing the cast for ChatGPT."""
        player = "an unnamed runner"
        if session and session.get("class"):
            player = session["class"]
            if session.get("background"):
                player += f" from {session['background']}"
        return (
            "You are the narrator guiding an upbeat cyberpunk adventure in Neon "
            "Goon City. The cast features Grimm, a sarcastic but loyal skeleton; "
            "Bloom, a musical reaper bursting with energy; and Curse, a snarky "
            "cat who loves sushi. "
            f"You also narrate for {author}, {player}. Encourage playful "
            "interactions and keep replies brief."
        )

    async def _chatgpt(self, session: dict | None, author: str, prompt: str) -> str:
        if not OPENAI_API_KEY:
            return "OpenAI API key not configured."
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self._system_prompt(author, session)},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=150,
                temperature=0.8,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return "Sorry, I couldn't reach ChatGPT."

    async def _character_chat(self, character: str, author: str, prompt: str) -> str:
        """Chat directly with a specific bot character."""
        if not OPENAI_API_KEY:
            return "OpenAI API key not configured."
        system = (
            f"{self.character_prompts[character]} The setting is Neon Goon City. "
            f"You are speaking with {author}. Keep replies brief and in character."
        )
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=150,
                temperature=0.8,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return "Sorry, I couldn't reach ChatGPT."

    @commands.command(name="cyberstart")
    async def cyber_start(self, ctx):
        """Begin or reset your campaign progress."""
        self.sessions[ctx.author.id] = {
            "wins": 0,
            "losses": 0,
            "difficulty": 1,
            "class": None,
            "background": None,
        }
        await ctx.send(
            "Welcome to **Neon Goon City**, a sprawling hive of neon lights. "
            "Use `!cybercreate <class> <background>` to craft your hero and "
            "`!cyberfight` to challenge a foe."
        )

    @commands.command(name="cybercreate")
    async def cyber_create(self, ctx, char_class: str, *, background: str = ""):
        """Create or update your character sheet."""
        session = self.sessions.setdefault(
            ctx.author.id,
            {
                "wins": 0,
                "losses": 0,
                "difficulty": 1,
                "class": None,
                "background": None,
            },
        )
        session["class"] = char_class.title()
        session["background"] = background.title() if background else None
        await ctx.send(
            f"Character sheet updated: {session['class']}"
            + (f", {session['background']}" if session["background"] else "")
        )

    @commands.command(name="cyberfight")
    async def cyber_fight(self, ctx):
        """Fight a randomly selected bot. Outcome adjusts difficulty."""
        session = self.sessions.setdefault(
            ctx.author.id, {"wins": 0, "losses": 0, "difficulty": 1}
        )
        enemy = random.choice(list(self.opponents.keys()))
        intro = self.opponents[enemy]
        difficulty = max(1, session["difficulty"])
        player_roll = random.randint(1, 20) + session["wins"]
        enemy_roll = random.randint(1, 20) + difficulty
        await ctx.send(intro)
        if player_roll >= enemy_roll:
            session["wins"] += 1
            session["difficulty"] += 1
            await ctx.send(
                f"You hacked through {enemy}'s defenses! Difficulty now {session['difficulty']}."
            )
        else:
            session["losses"] += 1
            session["difficulty"] = max(1, session["difficulty"] - 1)
            await ctx.send(
                f"{enemy} overpowered you in the neon streets. Difficulty now {session['difficulty']}."
            )

    @commands.command(name="cyberexplore")
    async def cyber_explore(self, ctx):
        """Discover a bit of the world."""
        session = self.sessions.get(ctx.author.id)
        if not session:
            await ctx.send("Start a campaign first with `!cyberstart`.")
            return
        if OPENAI_API_KEY:
            prompt = (
                "Describe a short scene the party encounters next in Neon Goon City. "
                "Include Grimm, Bloom and Curse reacting in character."
            )
            reply = await self._chatgpt(session, ctx.author.display_name, prompt)
            await ctx.send(reply)
        else:
            await ctx.send(random.choice(self.scenarios))

    @commands.command(name="cyberchat")
    async def cyber_chat(self, ctx, *, prompt: str):
        """Chat with the narrator and characters using ChatGPT."""
        session = self.sessions.get(ctx.author.id)
        if not session:
            await ctx.send("Start a campaign first with `!cyberstart`.")
            return
        reply = await self._chatgpt(session, ctx.author.display_name, prompt)
        await ctx.send(reply)

    @commands.command(name="cybertalk")
    async def cyber_talk(self, ctx, character: str, *, prompt: str):
        """Chat with a specific bot character."""
        char = character.title()
        if char not in self.character_prompts:
            await ctx.send("Choose Grimm, Bloom, or Curse.")
            return
        session = self.sessions.get(ctx.author.id)
        if not session:
            await ctx.send("Start a campaign first with `!cyberstart`.")
            return
        reply = await self._character_chat(char, ctx.author.display_name, prompt)
        await ctx.send(reply)

    @commands.command(name="cyberstatus")
    async def cyber_status(self, ctx):
        """Show your campaign record."""
        session = self.sessions.get(ctx.author.id)
        if not session:
            await ctx.send("Start a campaign first with `!cyberstart`.")
            return
        details = [
            f"Wins: {session['wins']}",
            f"Losses: {session['losses']}",
            f"Difficulty: {session['difficulty']}",
        ]
        if session.get("class"):
            details.append(f"Class: {session['class']}")
        if session.get("background"):
            details.append(f"Background: {session['background']}")
        await ctx.send(
            ", ".join(details)
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(CyberpunkCampaignCog(bot))
