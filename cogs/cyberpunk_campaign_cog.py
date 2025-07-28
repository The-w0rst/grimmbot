import random
from discord.ext import commands


class CyberpunkCampaignCog(commands.Cog):
    """Lightweight cyberpunk DnD campaign with dynamic difficulty."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.sessions: dict[int, dict[str, int]] = {}
        self.opponents = [
            "Grimm",  # leader skeleton
            "Bloom",  # enthusiastic reaper
            "Curse",  # mischievous cat
        ]

    @commands.command(name="cyberstart")
    async def cyber_start(self, ctx):
        """Begin or reset your campaign progress."""
        self.sessions[ctx.author.id] = {"wins": 0, "losses": 0, "difficulty": 1}
        await ctx.send(
            "Welcome to **Neon Goon City**, a cyberpunk DnD adventure! "
            "Use `!cyberfight` to challenge a cybernetic foe."
        )

    @commands.command(name="cyberfight")
    async def cyber_fight(self, ctx):
        """Fight a randomly selected bot. Outcome adjusts difficulty."""
        session = self.sessions.setdefault(
            ctx.author.id, {"wins": 0, "losses": 0, "difficulty": 1}
        )
        enemy = random.choice(self.opponents)
        difficulty = max(1, session["difficulty"])
        player_roll = random.randint(1, 20) + session["wins"]
        enemy_roll = random.randint(1, 20) + difficulty
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

    @commands.command(name="cyberstatus")
    async def cyber_status(self, ctx):
        """Show your campaign record."""
        session = self.sessions.get(ctx.author.id)
        if not session:
            await ctx.send("Start a campaign first with `!cyberstart`.")
            return
        await ctx.send(
            f"Wins: {session['wins']}, Losses: {session['losses']}, Difficulty: {session['difficulty']}"
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(CyberpunkCampaignCog(bot))
