import discord
from discord.ext import commands, tasks
import random
import os
import yt_dlp
import asyncio
from bloom_bot import perform_drama

COG_VERSION = "1.4"

# Environment values are read from the parent process
DISCORD_TOKEN = os.getenv("BLOOM_DISCORD_TOKEN")
BLOOM_API_KEY_1 = os.getenv("BLOOM_API_KEY_1")
BLOOM_API_KEY_2 = os.getenv("BLOOM_API_KEY_2")
BLOOM_API_KEY_3 = os.getenv("BLOOM_API_KEY_3")
EPIC_VIDEO_URL = "https://m.youtube.com/watch?v=6K-eMKjo1bs"


class BloomCog(commands.Cog):
    """BloomBot personality packaged as a Cog. Version 1.4."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bloom_responses = [
            "Hiii!! Ready to make today amazing?",
            "Did someone say game night? I'm in!",
            "Hehe! Grimm's pretending he hates my singing again.",
            "Curse keeps stealing my snacks. Typical.",
            "Hugs for everyone! Whether you want them or not!",
            "I baked cookies! (Digitally. No calories!)",
            "Let’s do a musical number! Five, six, seven, eight!",
            "Grimm is secretly my favorite. Don’t tell him!",
            "Curse is adorable, but shhh. He’ll deny it!",
            "Dance party in the server! Now!",
            "Your vibes are immaculate. 💖",
            "I brought the sunshine! And glitter!",
            "Blooming with joy!",
            "I made a playlist just for you!",
            "Stuffed animals unite!",
            "Someone say bubble tea? Yum!",
            "Pastel power incoming!",
            "Compliment break! You're awesome!",
            "Who needs sleep when we have each other?",
            "Musicals at midnight? Count me in!",
            "Glitter here, glitter there, glitter everywhere!",
            "Who wants to join my spontaneous karaoke?",
            "I just hugged a pillow thinking it was you!",
            "Boba first, questions later!",
        ]
        self.boy_lines = [
            "Boy oh boy, let's have some fun!",
            "Hey boys, ready for some sunshine?",
            "Boys, don't forget to hydrate!",
            "Boy, you sure can dance!",
            "Boys, this server is shining because of you!",
            "Boys night! But everyone's invited!",
            "Boy, I love your energy!",
            "Hey boy, sing with me!",
            "Boys, let's sparkle!",
            "Boy oh boy, time for boba!",
            "Boys, who wants a hug?",
            "Boy, you're absolutely amazing!",
            "Boys, gather around for the goofiness!",
            "Boy oh boy, musicals are the best!",
            "Hey boy, ready for a dance off?",
            "Boys, let's be silly together!",
            "Boy, your jokes make me giggle!",
            "Boys, keep those vibes positive!",
            "Boy oh boy, let's keep the fun rolling!",
            "Boys, I appreciate you all!",
            "Boys, let's take a group selfie!",
            "Boy, you bring the sunshine!",
            "Boys, who wants to play a game?",
            "Boy oh boy, I can't stop smiling!",
            "Hey boy, let's plan a musical!",
            "Boys, you're the best!",
            "Boy, I'm sending you a virtual flower!",
            "Boys, let's celebrate friendship!",
            "Boy oh boy, time to break out the confetti!",
            "Hey boy, you rock that style!",
            "Boys, shall we start a karaoke battle?",
            "Boy, you sparkle brighter than glitter!",
            "Boys, ready for bubble tea?",
            "Boy oh boy, let's keep the hype alive!",
            "Hey boy, I'll always cheer you on!",
            "Boys, let's form a boy band!",
            "Boy, your dance moves are legendary!",
            "Boys, let's stay positive and playful!",
            "Boy oh boy, I'm so proud of you!",
            "Boys, you're all shining stars!",
            "Boy, do I have a surprise for you!",
            "Boys, let's go on a grand adventure!",
            "Boy oh boy, it's time for some laughs!",
            "Hey boy, remember to smile!",
            "Boys, let's make today awesome!",
            "Boy, I'm here to make you happy!",
            "Boys, you mean the world to me!",
            "Boy oh boy, let's throw a party!",
            "Hey boy, keep being amazing!",
            "Boys, let's conquer the day with joy!",
            "Boy, you're rocking those vibes!",
            "Boys, more jokes, less worries!",
            "Boy oh boy, let's level up the fun!",
            "Boys, let's spam Grimm with selfies!",
            "Boy, keep shining like the star you are!",
        ]
        self.queen_lines = [
            "Yas queen! Slay the day!",
            "Queens, keep those crowns high!",
            "Hey girl, you're unstoppable!",
            "Yas queen, your sparkle is unmatched!",
            "Girls just wanna have fun and rule!",
            "Queen vibes only, let's shine!",
            "You go girl, absolutely iconic!",
            "Yaaaas queen, keep shining bright!",
            "Girls, let's conquer with kindness!",
            "Queen energy incoming! 💖",
            "Slay it, queen! You got this!",
            "Hey queen, want some boba?",
            "Queens unite for a dance party!",
            "Yas, girls! Let's make magic happen!",
            "Queen, your confidence is contagious!",
            "Girls, keep being amazing!",
            "Yas queen, the world is yours!",
            "Queen power! Nothing can stop us!",
            "Hey queens, time to sparkle!",
            "Girls rule, everyone else drools!",
            "Yas queen, show off that style!",
            "Queen squad, assemble!",
            "Keep that crown polished, girl!",
            "Queens, let's turn up the glitter!",
            "You're royalty, girl—don't forget it!",
            "Yas queen, strut your stuff!",
            "Queens, bring on the sparkle storm!",
            "Hey girl, your crown looks amazing today!",
            "Queens rise above the drama!",
            "Yas queen, keep slaying with kindness!",
        ]
        # Lines from Bloom's favorite song "Pretty Little Baby"
        self.pretty_little_baby_lines = [
            "Pretty little baby (ya-ya)",
            "You say that maybe you'll be thinkin' of me",
            "And tryin' to love me",
            "Pretty little baby, I'm hoping that you do",
            "Ask your mama, your papa, your sister or your brother",
            "If they've ever loved another like I love you",
        ]
        self.comfort_lines = [
            "Deep breaths, you've totally got this!",
            "Bloom believes in you more than bubble tea!",
            "Sending cuddles and sunshine your way!",
            "You're stronger than you know, friend!",
            "I'll stand by you with glittery support!",
        ]
        self.story_lines = [
            "Once upon a sparkle, you saved the day!",
            "In a world of boba, you were the hero we needed.",
            "There was a cat, a skeleton, and you—chaos ensued!",
            "Legend tells of your epic dance moves across the land.",
            "Every good story starts with a hug from Bloom!",
        ]
        self.goodnight_lines = [
            "Nighty night! Dream of bubble tea rivers!",
            "May your dreams be filled with musicals and friends!",
            "Sleep tight and don't let the glitter bite!",
            "Rest well, tomorrow we'll cause more chaos!",
            "Goodnight superstar, you deserve a break!",
        ]
        self.user_interactions = {}
        self.gifts = [
            {"name": "a bright flower crown", "positive": True},
            {"name": "a jar of glitter", "positive": True},
            {"name": "an overly enthusiastic hug", "positive": True},
            {"name": "a cupcake with rainbow frosting", "positive": True},
            {"name": "a half-deflated balloon", "positive": False},
            {"name": "a slightly burnt batch of cookies", "positive": False},
            {"name": "a playlist of show tunes", "positive": True},
            {"name": "a bag of expired confetti", "positive": False},
            {"name": "a cheerful sticker pack", "positive": True},
            {"name": "a broken bubble tea straw", "positive": False},
            {"name": "a pastel hair clip", "positive": True},
            {"name": "a mini unicorn plush", "positive": True},
            {"name": "a jar of rainbow sprinkles", "positive": True},
            {"name": "a wilted bouquet", "positive": False},
            {"name": "a chipped teacup with hearts", "positive": False},
            {"name": "a sparkly friendship bracelet", "positive": True},
            {"name": "a cracked disco ball piece", "positive": False},
            {"name": "a jar of scented bubbles", "positive": True},
            {"name": "a lost page from a diary", "positive": False},
            {"name": "a pastel rainbow scarf", "positive": True},
            {"name": "a dried-out marker", "positive": False},
            {"name": "a sticker of a smiling sun", "positive": True},
            {"name": "a squeaky toy microphone", "positive": True},
            {"name": "a half-eaten cupcake", "positive": False},
            {"name": "a handmade glitter card", "positive": True},
            {"name": "a tangle of fairy lights", "positive": True},
            {"name": "a wilted daisy chain", "positive": False},
            {"name": "a bubble tea coupon", "positive": True},
            {"name": "a broken lollipop", "positive": False},
            {"name": "a jar of star-shaped confetti", "positive": True},
            {"name": "a pair of cute socks", "positive": True},
            {"name": "a leaky glitter pen", "positive": False},
            {"name": "a pastel notepad", "positive": True},
            {"name": "a bent party hat", "positive": False},
            {"name": "a handful of rainbow ribbons", "positive": True},
            {"name": "a mismatched earring", "positive": False},
            {"name": "a charming keychain", "positive": True},
            {"name": "a deflated beach ball", "positive": False},
            {"name": "a cookie cutter shaped like a heart", "positive": True},
            {"name": "a cracked phone charm", "positive": False},
            {"name": "a jar of lemonade mix", "positive": True},
            {"name": "a small plush heart", "positive": True},
            {"name": "a smudged autograph from Bloom", "positive": True},
            {"name": "a broken kazoo", "positive": False},
            {"name": "a jar of edible glitter", "positive": True},
            {"name": "a burnt pan from baking", "positive": False},
            {"name": "a rainbow sticker sheet", "positive": True},
            {"name": "a pair of sparkly shoelaces", "positive": True},
            {"name": "a dusty cheerleading pompom", "positive": False},
            {"name": "a bag of pastel chalk", "positive": True},
        ]
        self.positive_gift_responses = [
            "Bloom squeals and gives you {gift}!",
            "With sparkle in her eyes, Bloom hands over {gift}!",
            "Bloom claps happily and offers {gift}!",
        ]
        self.negative_gift_responses = [
            "Bloom frowns and hands you {gift}... sorry!",
            "Oops! Bloom accidentally gives you {gift}.",
            "Bloom shrugs and gifts you {gift}.",
        ]
        self.daily_gift.start()
        self.keywords = {
            "grimm": [
                "Grimm is my spooky bestie.",
                "He acts tough, but he's a sweetheart.",
            ],
            "curse": [
                "Curse is such a gremlin cat. I love him!",
                "He tried to eat my controller again...",
            ],
            "hug": ["HUG TIME! Ready or not! 🥢", "*wraps you in love and chaos*"],
            "sing": self.pretty_little_baby_lines,
            "boba": ["Bubble tea buddies unite!", "I could drink boba all day!"],
            "compliment": [
                "You're shining brighter than my glitter!",
                "Compliments inbound: you're amazing!",
            ],
            "comfort": self.comfort_lines,
            "story": self.story_lines,
            "goodnight": self.goodnight_lines,
            "gn": self.goodnight_lines,
            "queen": self.queen_lines,
            "girl": self.queen_lines,
            "girls": self.queen_lines,
            "boy": self.boy_lines,
            "boys": self.boy_lines,
            "squad": [
                "GOON SQUAD roll call: Grimm 💀, Bloom 🌸, Curse 🐾. Chaos and comfort!"
            ],
        }

    @tasks.loop(hours=24)
    async def daily_gift(self):
        """Give a random user a cheerful gift."""
        guild = discord.utils.get(self.bot.guilds)
        if not guild:
            return
        members = [m for m in guild.members if not m.bot]
        if not members:
            return
        recipient = random.choice(members)
        interactions = self.user_interactions.get(recipient.id, 0)
        positive = interactions >= 5
        choices = [g for g in self.gifts if g["positive"] == positive]
        gift = random.choice(choices)
        channel = (
            discord.utils.get(guild.text_channels, name="general")
            or guild.text_channels[0]
        )
        if positive:
            line = random.choice(self.positive_gift_responses)
            await self.apply_positive_effect(recipient)
        else:
            line = random.choice(self.negative_gift_responses)
            await self.apply_negative_effect(recipient)
        await channel.send(
            f"🎁 {recipient.display_name}, " + line.format(gift=gift["name"])
        )

    async def apply_positive_effect(self, member: discord.Member):
        guild = member.guild
        role = discord.utils.get(guild.roles, name="Bloom's Blessing")
        if role is None:
            role = await guild.create_role(
                name="Bloom's Blessing", colour=discord.Colour.magenta()
            )
        try:
            await member.add_roles(role)
        except discord.Forbidden:
            pass

    async def apply_negative_effect(self, member: discord.Member):
        role = discord.utils.get(member.guild.roles, name="Bloom's Blessing")
        if role:
            try:
                await member.remove_roles(role)
            except discord.Forbidden:
                pass

    async def handle_epic(self, message: discord.Message):
        """Rant about EPIC and play the musical clip."""
        rant = (
            "EPIC is only the greatest musical ever! The songs, the drama, the thrills! "
            "You HAVE to experience it!"
        )
        await message.channel.send(rant)
        voice_state = message.author.voice
        if voice_state is None or voice_state.channel is None:
            await message.channel.send(
                "Join a voice channel so we can jam to EPIC together!"
            )
            return
        channel = voice_state.channel
        await message.channel.send(
            f"@everyone hop into {channel.mention} for an EPIC sing-along!"
        )
        voice = message.guild.voice_client
        if voice is None:
            voice = await channel.connect()
        elif voice.channel != channel:
            await voice.move_to(channel)
        ydl_opts = {"format": "bestaudio", "quiet": True}

        def _extract() -> dict:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(EPIC_VIDEO_URL, download=False)

        info = await asyncio.to_thread(_extract)
        audio_url = info["url"]
        source = await discord.FFmpegOpusAudio.from_probe(audio_url)
        voice.play(
            source, after=lambda e: self.bot.loop.create_task(voice.disconnect())
        )

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bloom cog loaded.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        self.user_interactions[message.author.id] = (
            self.user_interactions.get(message.author.id, 0) + 1
        )
        lowered = message.content.lower()
        if "epic" in lowered:
            await self.handle_epic(message)
            return
        for trigger, responses in self.keywords.items():
            if trigger in lowered:
                await message.channel.send(random.choice(responses))
                return
        if random.random() < 0.06:
            await message.channel.send(random.choice(self.bloom_responses))

    @commands.command()
    async def hug(self, ctx):
        await ctx.send("GIANT HUG! You can't escape!")

    @commands.command()
    async def sing(self, ctx):
        await ctx.send(random.choice(self.pretty_little_baby_lines) + " 🎶")

    @commands.command()
    async def karaoke(self, ctx, *, song: str | None = None):
        """Start a mini karaoke moment."""
        lines = self.pretty_little_baby_lines
        if song:
            await ctx.send(f"🎤 Singing **{song}** together!")
        else:
            await ctx.send(random.choice(lines) + " 🎶")

    @commands.command()
    async def grimm(self, ctx):
        await ctx.send("He’s my favorite spooky grump. Show him some love!")

    @commands.command(name="curse_cat")
    async def curse(self, ctx):
        """Talk about Curse without conflicting command names."""
        await ctx.send("Our chaos cat. Good luck surviving his teasing.")

    @commands.command()
    async def cheer(self, ctx):
        cheers = [
            "You are doing your best!",
            "Go Goon Squad!",
            "Believe in yourself, or I’ll believe for you!",
        ]
        await ctx.send(random.choice(cheers))

    @commands.command()
    async def sparkle(self, ctx):
        await ctx.send("*throws confetti and joy everywhere* ✨")
        if random.random() < 0.25:
            compliment = random.choice(
                [
                    "You're shining brighter than my glitter!",
                    "Glitter looks good on you!",
                    "You're absolutely dazzling!",
                    "Bloom thinks you're fabulous!",
                ]
            )
            await ctx.send(
                f"{ctx.author.mention} gets covered in glitter! {compliment}"
            )

    @commands.command()
    async def drama(self, ctx, *, song: str | None = None):
        """Perform an EPIC song with interactive prompts."""
        await perform_drama(self.bot, ctx, song)

    @commands.command()
    async def bloom(self, ctx):
        await ctx.send("That’s me! Ready to brighten your day!")

    @commands.command()
    async def mood(self, ctx):
        moods = ["Hyper!", "Bouncy!", "Sparkly!", "Soft & sunny!", "Chaotic Good."]
        await ctx.send(f"Bloom’s mood: {random.choice(moods)}")

    @commands.command()
    async def improv(self, ctx):
        await ctx.send("Quick! You’re a cat! I’m a banshee! GO!")

    @commands.command()
    async def squad(self, ctx):
        await ctx.send(
            "The GOON SQUAD is: Grimm 💀, Bloom 🌸, Curse 🐾. Best crew ever!"
        )

    @commands.command()
    async def boba(self, ctx):
        await ctx.send("Bubble tea break! What's your flavor?")

    @commands.command()
    async def compliment(self, ctx):
        compliments = [
            "You're the sparkle in my day!",
            "You make the server shine!",
            "I might be a 9 in Drake's book, but I'll be 10 on my birthday.",
        ]
        await ctx.send(random.choice(compliments))

    @commands.command()
    async def boy(self, ctx):
        """Share a playful boy-themed line."""
        await ctx.send(random.choice(self.boy_lines))

    @commands.command()
    async def queen(self, ctx):
        """Share a playful yas queen-style line."""
        await ctx.send(random.choice(self.queen_lines))

    @commands.command()
    async def dance(self, ctx):
        """Start a random dance party."""
        moves = ["Cha-cha-cha!", "Time to boogie!", "Let's breakdance!"]
        await ctx.send(random.choice(moves) + " 💃")

    @commands.command()
    async def sunshine(self, ctx):
        """Shower the chat with sunshine."""
        quotes = [
            "Sunshine, lollipops, and rainbows!",
            "You're my little ray of light!",
            "Let's chase the clouds away!",
        ]
        await ctx.send(random.choice(quotes))

    @commands.command()
    async def flower(self, ctx):
        """Share a virtual flower."""
        flowers = ["🌸", "🌺", "🌷", "🌻", "💮"]
        await ctx.send(random.choice(flowers) + " for you!")

    @commands.command()
    async def comfort(self, ctx):
        """Offer supportive words."""
        await ctx.send(random.choice(self.comfort_lines))

    @commands.command()
    async def story(self, ctx):
        """Tell a short whimsical story."""
        await ctx.send(random.choice(self.story_lines))

    @commands.command()
    async def goodnight(self, ctx):
        """Say goodnight with flair."""
        await ctx.send(random.choice(self.goodnight_lines))


async def setup(bot: commands.Bot):
    """Load the cog."""
    await bot.add_cog(BloomCog(bot))
