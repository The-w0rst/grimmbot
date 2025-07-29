import discord
from discord.ext import commands
import asyncio
import random
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


# Extensive ruling responses for each persona.
JUDGE_LINES = {
    "Grimm": {
        "User1": [
            "User1 makes a sharper case. Bones don't lie.",
            "I grudgingly nod to User1's logic.",
            "User1's words sting truer than yours.",
            "Seems User1 dug the deeper grave for this issue.",
            "The reaper votes User1—deal with it.",
            "User1's argument chills the bone in a good way.",
            "Hard to admit, but User1 is right this time.",
            "User1 swings the scythe better today.",
            "Grudging respect to User1's point of view.",
            "User1's side rattles with conviction.",
            "I've heard worse than User2, but User1 wins.",
            "User1's logic hits like a tombstone.",
            "User1 edges out with grim certainty.",
            "My bones vote for User1's stance.",
            "Can't deny User1's eerie accuracy here.",
            "User1 dug up stronger evidence.",
            "The shadows lean toward User1's side.",
            "User1 buries User2 in this debate.",
            "User1's case rings hollow—in a good way.",
            "In this crypt, User1 stands tallest.",
        ],
        "Both should compromise": [
            "Neither of you impresses the bone pile.",
            "I've seen corpses with better arguments; call it even.",
            "Both cases clatter weakly—try again.",
            "No winner here. Just echoes in the crypt.",
            "You're both partially right and terribly wrong.",
            "This stalemate bores even me.",
            "Settle it yourselves, I need a nap.",
            "A draw. Now leave me to my gloom.",
            "Not convinced by either bony argument.",
            "Both sides creak equally.",
            "I shrug my ribs—it's a tie.",
            "Neither side has meat on these bones.",
            "Let's call it an undead heat.",
            "Both stumble in this grave debate.",
            "You're both doomed to mediocrity.",
            "I'm not picking a side. Deal with it.",
            "Equally convincing, which is to say barely at all.",
            "Call it a draw before I rot further.",
            "No clear victor emerges from this crypt dust.",
            "This argument is deadlocked like my heart.",
        ],
        "User2": [
            "User2's point rattles stronger today.",
            "I side with User2's grim reasoning.",
            "User2's stance has a chilling logic.",
            "User2 digs up the better evidence.",
            "The darkness favors User2's angle.",
            "User2's argument cuts deeper than yours.",
            "Hard truths lean toward User2.",
            "User2 buries User1 in wit.",
            "User2's words strike like a scythe.",
            "User2 casts a longer shadow here.",
            "User2 wins this morbid match.",
            "Bones agree with User2 today.",
            "User2 holds the stronger skeleton.",
            "User2 whispers the harsher truth.",
            "User2's case is carved in stone.",
            "I'm siding with User2's dark logic.",
            "User2 sounds slightly less foolish.",
            "The crypt echoes User2's perspective.",
            "User2's argument is the final nail.",
            "User2 claims victory from the grave.",
        ],
    },
    "Bloom": {
        "User1": [
            "User1's kindness shines brighter!",
            "I'm swayed by User1's cheerful spirit.",
            "User1 sparkles with convincing points.",
            "Going with User1 because love wins!",
            "User1's stance blooms beautifully.",
            "User1 wraps the issue in warm hugs.",
            "Gotta side with User1's sunny outlook.",
            "User1 just sounds sweeter to me.",
            "User1's heart is in the right place.",
            "User1 wins with wholesome vibes.",
            "I'll dance with User1's logic today.",
            "User1's approach sings to my heart.",
            "User1's words smell like fresh flowers!",
            "I feel User1's points buzzing happily.",
            "User1 has that spark of joy I adore.",
            "My petals point toward User1's side!",
            "User1 sprinkles more optimism around.",
            "User1's angle glitters a bit brighter.",
            "User1 radiates the sweetest reasoning.",
            "I pick User1 with a sunny grin!",
        ],
        "Both should compromise": [
            "Oh gosh, you both make some sense!",
            "Let's meet in the middle and hug it out.",
            "Neither side totally wins my heart.",
            "Can't we all hold paws and agree?",
            "This debate needs more positivity from both.",
            "It's a draw—time for group snacks!",
            "How about you both take a deep breath?",
            "I say compromise, then we all sing.",
            "Both of you sparkle about the same.",
            "Hard to choose, so let's tie a ribbon on it.",
            "Equal parts lovely and messy—call it a tie.",
            "Neither argument fully won me over.",
            "Let's decide later over cupcakes!",
            "Both of your hearts seem in the right place.",
            "I can't decide, so let's hug!",
            "You're both right and wrong together.",
            "How about a group handshake instead?",
            "Tie game! Everyone gets a flower!",
            "We need more harmony—no winner here.",
            "I'm undecided, but still cheering for you!",
        ],
        "User2": [
            "User2's passion steals the spotlight!",
            "I feel the warmth in User2's side more.",
            "User2 shines with heartfelt conviction.",
            "Gonna back User2's sparkling wisdom.",
            "User2's view blooms with promise.",
            "User2 wraps this up in a bow nicely.",
            "I sense more joy in User2's angle.",
            "User2's reasoning is a bouquet of logic.",
            "My heart flutters toward User2 today.",
            "User2 sings the sweeter tune here.",
            "I can't resist User2's loving approach.",
            "User2 fills me with colorful hope.",
            "I'm handing the victory flower to User2.",
            "User2's side sparkles brighter.",
            "User2 beams with the better answer.",
            "My vote twirls toward User2!",
            "User2 pours on the cheerful evidence.",
            "I dance with User2's viewpoint.",
            "User2 radiates vibrant reasoning.",
            "User2's spirit wins my vote!",
        ],
    },
    "Curse": {
        "User1": [
            "Fine, User1 makes more sense. Ugh.",
            "Guess I'll side with User1 this time.",
            "User1 isn't totally wrong for once.",
            "User1 claws ahead just barely.",
            "Even I admit User1's argument scratches deeper.",
            "User1's logic doesn't stink—surprise!",
            "User1 shows sharper claws in this fight.",
            "User1 wins, so stop whining, User2.",
            "Yep, User1 takes it. Don't get cocky.",
            "User1's side doesn't completely bore me.",
            "User1 just edges out with less nonsense.",
            "Ugh, User1 actually has a point.",
            "User1's case hits harder, like a hairball.",
            "I begrudgingly vote User1.",
            "User1's argument hisses louder.",
            "User1 pounces on the better logic.",
            "Looks like User1 snags the win.",
            "Fine. User1. Happy now?",
            "User1 scratches out a narrow victory.",
            "User1's angle is slightly less annoying.",
        ],
        "Both should compromise": [
            "Meh, you're both equally irritating.",
            "Can't decide, so you both lose.",
            "This debate bores my whiskers off.",
            "Neither of you earns a full hiss or purr.",
            "Tie. Now feed me.",
            "Both of you talk too much.",
            "I'm not impressed by either side.",
            "You're both wrong enough to tie.",
            "Whatever, call it even and move on.",
            "Not picking a side—go chase a laser pointer.",
            "Equal parts annoying, so it's a draw.",
            "Yawn. Wake me when you make sense.",
            "Neither side earns my precious energy.",
            "I'll flip a coin—nope, tie it is.",
            "Both fail to scratch an itch.",
            "No winner, just noise in my ears.",
            "You're both lacking sparkle today.",
            "Come back with better arguments.",
            "Tie, because I said so.",
            "I'm undecided and uninterested.",
        ],
        "User2": [
            "User2 wins. Don't make me repeat it.",
            "I side with User2 just to spite you.",
            "User2's point has sharper claws.",
            "User2 annoys me less, so there.",
            "I'll throw my vote to User2 today.",
            "User2 purrs with better logic.",
            "User2's case smells less fishy.",
            "User2 scratches out the win easily.",
            "Yeah yeah, User2 takes this round.",
            "User2 outwits User1, shockingly.",
            "The cat chooses User2—deal with it.",
            "User2's stance claws through the nonsense.",
            "User2 slinks ahead with a clever swipe.",
            "User2 meows a stronger argument.",
            "User2's reasoning makes more sense to me.",
            "User2 sinks fangs into the issue better.",
            "Fine, User2 has the upper paw.",
            "User2 leaps to victory here.",
            "User2 wins—now leave me alone.",
            "User2 has the edge, annoyingly enough.",
        ],
    },
}


POSITIVE_WORDS = {
    "please",
    "thank",
    "thanks",
    "sorry",
    "apologize",
    "love",
    "appreciate",
}

NEGATIVE_WORDS = {
    "hate",
    "stupid",
    "idiot",
    "terrible",
    "awful",
    "bad",
}


class JudgeCog(commands.Cog):
    """Relationship judge for the Goon Squad."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # track cases for potential appeals
        self.cases: dict[tuple[frozenset[int], str], dict] = {}

    def _score_statement(self, text: str) -> int:
        """Return a simple score for ``text`` based on length and keywords."""
        words = [w.strip(".,!?\"'").lower() for w in text.split()]
        score = len(words)
        score += sum(2 for w in words if w in POSITIVE_WORDS)
        score -= sum(2 for w in words if w in NEGATIVE_WORDS)
        return score

    def _decide_vote(self, side1: str, side2: str) -> str:
        """Choose a winner by comparing keyword-weighted scores."""
        score1 = self._score_statement(side1)
        score2 = self._score_statement(side2)
        if abs(score1 - score2) <= 1:
            return "Both should compromise"
        return "User1" if score1 > score2 else "User2"

    def _format_reason(self, persona: str, vote: str) -> str:
        info = PERSONALITIES[persona]
        line = random.choice(JUDGE_LINES[persona][vote])
        return f"{info['prefix']}{line}"

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
