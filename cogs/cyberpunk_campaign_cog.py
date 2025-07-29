import os
import random
import openai
from discord.ext import commands

COG_VERSION = "1.3"

# Environment values are read from the parent process
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


class CyberpunkCampaignCog(commands.Cog):
    """Cyberpunk themed mini DnD campaign with simple character sheets. Version 1.3."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.sessions: dict[int, dict[str, int | str]] = {}
        self.opponents = {
            "Grimm": "Grimm cracks his bony knuckles. \"Let's see what you've got.\"",
            "Bloom": 'Bloom twirls a neon scythe. "Time for dramatic heroics!"',
            "Curse": 'Curse hisses, tail lashing. "I\'ll scratch more than your ego."',
        }
        self.character_prompts = {
            "Grimm": (
                "You are Grimm, a grumpy yet protective skeleton leader. "
                "Respond with short, sarcastic quips."
            ),
            "Bloom": (
                "You are Bloom, an energetic reaper who loves musicals, hugs "
                "and glitter. Speak with enthusiasm and emojis."
            ),
            "Curse": (
                "You are Curse, a mischievous talking cat obsessed with sushi "
                "and playful snark."
            ),
        }
        # 60 chance encounters split between upbeat and troublesome moments
        # Positive encounters encourage or reward the players, while negative
        # encounters hint at danger or complication. Players can interpret the
        # outcomes however they like during play.
        self.scenarios = [
            # --- Positive Encounters ---
            (
                "A street vendor gifts you neon stickers after Bloom compliments "
                "his music, brightening everyone's spirits."
            ),
            (
                "Grimm finds an old map etched on a wall, revealing a shortcut "
                "through the city."
            ),
            (
                "A kid recognizes Curse from a local legend and hands over a lucky "
                "charm."
            ),
            (
                "Bloom leads a spontaneous dance-off in the plaza, and the crowd "
                "cheers for the crew."
            ),
            (
                "You stumble across a hidden rooftop garden glowing in neon light, "
                "offering a quiet place to rest."
            ),
            (
                "A holographic poet recites verses that hint at safe paths through "
                "the undercity."
            ),
            (
                "Grimm's sarcasm actually amuses a patrol of enforcers who let you "
                "pass without hassle."
            ),
            (
                "Curse finds a stash of fresh sushi left out as an offering and "
                "shares it, begrudgingly."
            ),
            (
                "A rogue AI billboard flashes helpful tips about upcoming events in "
                "Neon Goon City."
            ),
            (
                "During a rainstorm, an umbrella drone offers everyone shelter, "
                "making travel easier."
            ),
            (
                "Bloom befriends a wandering spirit who offers cryptic guidance "
                "for the next objective."
            ),
            (
                "A local shopkeeper is so entertained by Grimm's dry humor that he "
                "throws in extra gear for free."
            ),
            (
                "You rescue a microbot from scrap dealers, and it projects a "
                "short-cut through the city's maze."
            ),
            (
                "An abandoned train car reveals a small cache of creds tucked "
                "behind a panel."
            ),
            (
                "Curse's tail accidentally triggers a hidden door leading to a "
                "secret arcade full of friendly hackers."
            ),
            (
                "A cheerful street artist paints your likeness, granting temporary "
                "fame among the locals."
            ),
            (
                "Grimm discovers an encrypted data chip that might hold leverage "
                "over your enemies."
            ),
            (
                "Bloom's song soothes a restless crowd, turning a potential riot "
                "into a block party."
            ),
            (
                "A passing courier mistakes you for VIPs and hands over invites to "
                "an exclusive club."
            ),
            (
                "The crew finds an abandoned mech frame ripe for salvage, giving "
                "you valuable parts."
            ),
            (
                "A radio tower broadcasts coded messages praising your recent deeds, "
                "boosting morale."
            ),
            (
                "You help a runaway droid evade capture, and it swears to repay the "
                "favor someday."
            ),
            ("Curse chases off a swarm of pesky drones, clearing the path ahead."),
            (
                "A hidden cache of neon graffiti supplies lets Bloom decorate the "
                "streets with uplifting art."
            ),
            (
                "You discover a quiet noodle bar where the owner remembers your "
                "heroics and offers a free meal."
            ),
            (
                "Grimm's quick thinking saves a musician from a collapsing stage, "
                "earning gratitude and new allies."
            ),
            (
                "A rogue taxi AI ferries you across town swiftly, avoiding known "
                "trouble spots."
            ),
            (
                "Bloom uncovers a stash of glittering credits hidden beneath a "
                "loose street tile."
            ),
            (
                "A friendly courier drone delivers forgotten supplies from an "
                "earlier mission."
            ),
            (
                "You cross paths with a legendary hacker who offers a favor in "
                "exchange for a story."
            ),
            # --- Negative Encounters ---
            (
                "A sudden blackout plunges the street into darkness as hostile "
                "voices close in."
            ),
            (
                "Grimm accidentally trips a silent alarm, drawing unwanted "
                "attention from patrols."
            ),
            (
                "Curse tries to swipe a snack and angers a stall owner who calls "
                "for backup."
            ),
            ("Bloom's humming attracts security drones that demand identification."),
            (
                "You hear rumors of a bounty on your heads spreading through the "
                "undercity."
            ),
            (
                "A rival gang tags the alley with threats, warning you to stay out "
                "of their territory."
            ),
            (
                "A neon sign shorts out, showering sparks and causing a nearby "
                "vendor to accuse you of sabotage."
            ),
            (
                "Curse catches sight of a mysterious figure tailing the crew, then "
                "loses them in the crowd."
            ),
            (
                "Grimm receives a hacked message claiming an old foe is back in "
                "town seeking revenge."
            ),
            (
                "Bloom slips on a slick street and nearly tumbles into a trash bot "
                "grinder."
            ),
            (
                "A faulty holo-advert projects a massive monster, causing chaos "
                "that obscures real threats."
            ),
            (
                "The crew stumbles into a restricted zone and must dodge roaming "
                "security mechs."
            ),
            (
                "A contact fails to show up, leaving you waiting while rumors of "
                "an ambush spread."
            ),
            (
                "Curse's latest prank enrages a street performer who vows payback "
                "with their own gang."
            ),
            (
                "Grimm's sarcasm offends a corporate officer, escalating into a "
                "tense standoff."
            ),
            (
                "A digital billboard glitches, flashing your faces with the word "
                "'Wanted'."
            ),
            (
                "You find an encrypted note hinting at betrayal from someone you "
                "consider an ally."
            ),
            (
                "Bloom hears a haunting melody that lures her toward a decrepit "
                "theater rumored to be cursed."
            ),
            ("A rogue drone steals a valuable gadget right out of Grimm's hands."),
            (
                "Street rumors point to a hidden trap ahead, but the only detour "
                "leads through enemy turf."
            ),
            (
                "A shady informant offers info for a price that seems far too high, "
                "hinting at a setup."
            ),
            (
                "Curse's whiskers twitch as toxic fumes seep from a nearby vent, "
                "forcing the crew to find clean air fast."
            ),
            (
                "Grimm suspects a gang is trailing you, but can't confirm how close "
                "they really are."
            ),
            (
                "The city speakers blare an emergency warning: curfew is starting "
                "early, trapping you outside."
            ),
            (
                "A surveillance drone broadcasts your location to unknown viewers "
                "before you can shut it down."
            ),
            (
                "Bloom spots ghostly figures flickering at the edge of vision, "
                "whispering ominous threats."
            ),
            (
                "Curse misreads a map and leads the party straight into a corporate "
                "checkpoint."
            ),
            (
                "An old contact betrays you, tipping off the authorities to your "
                "last safe house."
            ),
            (
                "A malfunctioning servo lift nearly drops you into the depths of "
                "the undercity."
            ),
            (
                "A mysterious broadcast hijacks nearby screens, claiming the crew "
                "holds the key to a dark prophecy."
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
        await ctx.send(", ".join(details))


async def setup(bot: commands.Bot):
    await bot.add_cog(CyberpunkCampaignCog(bot))
