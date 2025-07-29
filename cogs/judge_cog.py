import discord
from discord.ext import commands
import asyncio
from collections import Counter
from src.logger import log_message
import random

COG_VERSION = "1.0"

PERSONALITIES = {
    "Grimm": {
        "prefix": "Grimm drawls, ",
        "style": "ominous and sarcastic",
        "intro": [
            "let's get this over with.",
            "another spat? very well.",
            "state your grievances.",
            "you know the drill, argue.",
            "fine, I'll listen this time.",
            "give me your sides already.",
            "here we go again.",
            "can't wait to hear this nonsense.",
            "i'm all ears, unfortunately.",
            "let the misery begin.",
            "this better be worth it.",
            "talk, and make it quick.",
            "i live for drama, sadly.",
            "go on then, enlighten me.",
            "another glorious dispute.",
        ],
        "User1": [
            "User1 presented the clearer stance.",
            "User1's logic held more weight.",
            "User1 edged ahead with reason.",
            "I must concede to User1's points.",
            "User1 simply argued better.",
            "It's User1 who swayed me more.",
            "User1's side was less flawed.",
            "User1 outmatched the opposition.",
            "User1's reasoning rang truer.",
            "User1 wins this gloomy round.",
            "User1's case had the edge.",
            "I side with User1 here.",
            "User1 carried the stronger argument.",
            "User1 convinced me, begrudgingly.",
            "User1 takes it, sigh.",
        ],
        "User2": [
            "User2 actually makes more sense.",
            "User2's logic was sounder.",
            "User2 had the upper hand.",
            "User2 argued with grim precision.",
            "I find User2's points weightier.",
            "User2 edges this dreary contest.",
            "User2 made the better case.",
            "User2 persuaded me, somehow.",
            "User2's stance was stronger.",
            "User2 gets the nod.",
            "User2 wins, to my surprise.",
            "I lean toward User2 here.",
            "User2 takes the lead.",
            "I have to give it to User2.",
            "User2 carried the day.",
        ],
        "Both should compromise": [
            "neither of you impressed me.",
            "this is a deadlock, compromise.",
            "both arguments falter equally.",
            "no clear victor; meet halfway.",
            "both sides could be better.",
            "tie. work it out together.",
            "i'm calling it even.",
            "no winner, only weary judges.",
            "both lack the upper hand.",
            "no decisive blow landed.",
            "split decision: compromise.",
            "equal parts flawed, sadly.",
            "you're both partly right.",
            "neither dominates this round.",
            "call it even and move on.",
        ],
    },
    "Bloom": {
        "prefix": "Bloom chirps, ",
        "style": "playful and loving",
        "intro": [
            "hi friends! let's hash this out.",
            "ooh, a juicy debate!", 
            "tell me everything!", 
            "let's talk it through!", 
            "i'm all ears, lovelies.",
            "spill the tea, kindly.",
            "i'm ready to listen!",
            "let's get comfy and share.",
            "go ahead, i'm excited!",
            "yay, another discussion!",
            "i promise to be fair.",
            "share your hearts with me!",
            "let's sort this sweetly.",
            "i'm here to help!",
            "let the story unfold!",
        ],
        "User1": [
            "User1's view sparkled brighter!",
            "i felt User1's point more.",
            "User1's words rang truest.",
            "my vote leans to User1!",
            "User1's reasoning sang loudest.",
            "i'm charmed by User1's case.",
            "User1 had the clearer thought.",
            "i think User1 won me over!",
            "User1's stance felt more loving.",
            "User1 edges it with kindness.",
            "User1 brought better vibes!",
            "i'm on User1's side this time.",
            "User1 gave the stronger reason.",
            "User1's passion convinced me!",
            "it's User1 for the win!",
        ],
        "User2": [
            "User2's side shone brighter!",
            "User2 has my vote this round.",
            "User2's point felt more solid.",
            "User2 made me smile with logic.",
            "User2 argued so sweetly!",
            "i'm convinced by User2 here.",
            "User2's reasoning warmed my heart.",
            "User2 wins me over today.",
            "User2's stance took flight!",
            "i agree more with User2!",
            "User2 shared the clearer view.",
            "User2's case felt more complete.",
            "User2 just barely edges ahead!",
            "my vote goes to User2!",
            "User2 charmed me, honestly.",
        ],
        "Both should compromise": [
            "aww, i think you both have points!",
            "hmm, maybe meet in the middle?",
            "i can't pick a clear winner!",
            "let's agree you both tried!",
            "it's a tie! share some love.",
            "i'm split, let's compromise.",
            "both sides shine equally!",
            "nobody wins, but nobody loses!",
            "let's hug it out!",
            "it's even, so work together!",
            "call it a draw, friends!",
            "equal strengths, i say!",
            "you both make sense to me!",
            "i vote for teamwork here!",
            "no winner, only collaboration!",
        ],
    },
    "Curse": {
        "prefix": "Curse snickers, ",
        "style": "chaotic and blunt",
        "intro": [
            "alright, who's causing trouble?",
            "heh, another squabble!",
            "spill it quick!",
            "i'm bored, entertain me.",
            "let's stir the pot!",
            "i'm all about chaos, let's go!",
            "time for some mischief!",
            "give me the dirt already.",
            "i'm here to judge, sorta.",
            "this should be fun!",
            "hope you've got good drama!",
            "let's see who's right!",
            "who started this mess?",
            "bring on the arguments!",
            "this'll be a blast!",
        ],
        "User1": [
            "User1 actually makes sense!",
            "User1's got the edge here.",
            "i'm with User1 on this.",
            "User1 wins, deal with it.",
            "User1's arguments slap harder.",
            "User1 just owned it.",
            "User1 takes the crown today.",
            "User1 argues better, shockingly.",
            "i side with User1 this time.",
            "User1 beats User2, simple.",
            "User1's points are sharper.",
            "User1 is the clear winner.",
            "yeah, User1 is right.",
            "User1 outplays you, User2.",
            "User1 for the win, obviously.",
        ],
        "User2": [
            "User2's argument rules!",
            "User2 totally wins this.",
            "i'm siding with User2, sorry.",
            "User2's points hit harder.",
            "User2 takes the cake.",
            "User2 smashed it.",
            "i prefer User2's logic.",
            "User2 all the way!",
            "User2 just outdid User1.",
            "User2 is obviously right.",
            "User2's stance is stronger.",
            "User2 got this in the bag.",
            "yep, User2 wins easily.",
            "User2 out-argued you, User1.",
            "User2 for the chaotic win!",
        ],
        "Both should compromise": [
            "meh, you both lose.",
            "neither side thrills me.",
            "i call it a draw, boring!",
            "compromise or keep fighting, whatever.",
            "no winner, how dull.",
            "tie! i expected more chaos.",
            "you're both wrong and right.",
            "no clear champ this round.",
            "both of you need a rethink.",
            "this one's even, sigh.",
            "nobody's convincing today.",
            "equal faults on both sides.",
            "try harder next time, both of you.",
            "i can't pick, so don't ask.",
            "ugh, just compromise already.",
        ],
    },
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
        intro = random.choice(info["intro"])
        ruling = random.choice(info[vote])
        return f"{info['prefix']}{intro} {ruling}"

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
