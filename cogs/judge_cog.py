import discord
from discord.ext import commands
import asyncio
from collections import Counter
from src.logger import log_message

COG_VERSION = "1.0"

PERSONALITIES = {
    "Grimm": {
        "prefix": "Grimm drawls, ",
        "style": "ominous and sarcastic",
    },
    "Bloom": {
        "prefix": "Bloom chirps, ",
        "style": "playful and loving",
    },
    "Curse": {
        "prefix": "Curse snickers, ",
        "style": "chaotic and blunt",
    },
}

REASONS = {
    "User1": "User1's argument edged out the other.",
    "User2": "User2 made the stronger point.",
    "Both should compromise": "Neither side convinced me completely.",
}


class JudgeCog(commands.Cog):
    """Relationship judge for the Goon Squad."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # track cases for potential appeals
        self.cases: dict[tuple[frozenset[int], str], dict] = {}

    def _decide_vote(self, side1: str, side2: str) -> str:
        if len(side1) > len(side2):
            return "User1"
        if len(side2) > len(side1):
            return "User2"
        return "Both should compromise"

    def _format_reason(self, persona: str, vote: str) -> str:
        info = PERSONALITIES[persona]
        return f"{info['prefix']}in a {info['style']} tone: {REASONS[vote]}"

    async def _collect_statement(self, member: discord.Member, issue: str) -> str | None:
        try:
            await member.send(f"What's your side on the issue '{issue}'?")
        except discord.Forbidden:
            return None

        def check(m: discord.Message) -> bool:
            return m.author == member and isinstance(m.channel, discord.DMChannel)

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=120)
        except asyncio.TimeoutError:
            return None
        return msg.content.strip()

    async def _run_judgement(self, issue: str, side_map: dict[int, str], user1: discord.Member, user2: discord.Member) -> str:
        results = {}
        votes = []
        for persona in ("Grimm", "Bloom", "Curse"):
            vote = self._decide_vote(side_map[user1.id], side_map[user2.id])
            reason = self._format_reason(persona, vote)
            results[persona] = {"reason": reason, "vote": vote}
            votes.append(vote)
        counts = Counter(votes)
        majority = None
        for choice, cnt in counts.items():
            if cnt >= 2:
                majority = choice
                break
        lines = []
        for persona in ("Grimm", "Bloom", "Curse"):
            entry = results[persona]
            lines.append(f"**{persona}**: {entry['reason']} \n**Vote:** {entry['vote']}")
        if majority:
            lines.append(f"\nThe Goon Squad has ruled: {majority}.")
        else:
            lines.append("\nIt's a tie! Both of you need to compromise.")
        return "\n\n".join(lines)

    @commands.command(name="judge")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def judge(self, ctx: commands.Context, users: commands.Greedy[discord.Member], *, issue: str):
        """Judge an argument between two people."""
        if len(users) == 0:
            await ctx.send("Mention the other participant.")
            return
        if len(users) == 1:
            user1 = ctx.author
            user2 = users[0]
        elif len(users) == 2 and ctx.author.guild_permissions.administrator:
            user1, user2 = users[0], users[1]
        else:
            await ctx.send("Only admins can judge for two other users.")
            return

        side1 = await self._collect_statement(user1, issue)
        if side1 is None:
            await ctx.send(f"Couldn't get {user1.display_name}'s statement.")
            return
        side2 = await self._collect_statement(user2, issue)
        if side2 is None:
            await ctx.send(f"Couldn't get {user2.display_name}'s statement.")
            return

        key = (frozenset({user1.id, user2.id}), issue.lower())
        self.cases[key] = {"users": (user1.id, user2.id), "sides": {user1.id: side1, user2.id: side2}, "appealed": False}

        result_text = await self._run_judgement(issue, self.cases[key]["sides"], user1, user2)
        for member in {user1, user2}:
            try:
                await member.send(result_text)
            except discord.Forbidden:
                pass
        await ctx.send("Judgement delivered via DM.")
        log_message(f"Judge case {user1.id} vs {user2.id} issue '{issue}'")

    @commands.command(name="appeal")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def appeal(self, ctx: commands.Context, other: discord.Member, *, issue: str):
        """Request a single rematch on a previous judgement."""
        key = (frozenset({ctx.author.id, other.id}), issue.lower())
        case = self.cases.get(key)
        if not case:
            await ctx.send("No judgement found for that issue.")
            return
        if case["appealed"]:
            await ctx.send("You've already appealed this argument once.")
            return
        case["appealed"] = True
        user1_id, user2_id = case["users"]
        user1 = ctx.guild.get_member(user1_id)
        user2 = ctx.guild.get_member(user2_id)
        result_text = await self._run_judgement(issue, case["sides"], user1, user2)
        for member in {user1, user2}:
            try:
                await member.send("Appeal result:\n" + result_text)
            except discord.Forbidden:
                pass
        await ctx.send("Appeal processed. Check your DMs.")
        log_message(f"Appeal case {user1_id} vs {user2_id} issue '{issue}'")


async def setup(bot: commands.Bot):
    await bot.add_cog(JudgeCog(bot))
