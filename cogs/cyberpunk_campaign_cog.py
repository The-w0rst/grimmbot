import random
import pathlib
from discord.ext import commands


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
        ]

        base = pathlib.Path(__file__).resolve().parent.parent / "ascii_art"
        self.visuals = {}
        for name in ["grimm", "bloom", "curse"]:
            path = base / f"{name}.txt"
            try:
                self.visuals[name] = path.read_text()
            except FileNotFoundError:
                self.visuals[name] = f"[Missing art for {name}]"

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
            "Welcome to **Neon Goon City**, a hive of neon lights. "
            "Grimm reluctantly guides you, Bloom offers cheerful help, "
            "and Curse schemes as the cyber villain. "
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
        await ctx.send(random.choice(self.scenarios))

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

    @commands.command(name="cybervisual")
    async def cyber_visual(self, ctx, character: str | None = None):
        """Display cyberpunk ASCII art for a character."""
        if character:
            key = character.lower()
            art = self.visuals.get(key)
            if art:
                await ctx.send(f"```{art}```")
            else:
                await ctx.send("No art for that character.")
        else:
            for art in self.visuals.values():
                await ctx.send(f"```{art}```")


async def setup(bot: commands.Bot):
    await bot.add_cog(CyberpunkCampaignCog(bot))
