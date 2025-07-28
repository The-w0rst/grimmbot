from discord.ext import commands
import random
import os
from dotenv import load_dotenv

# Load a single shared configuration file for all bots
load_dotenv("config/setup.env")
DISCORD_TOKEN = os.getenv("BLOOM_DISCORD_TOKEN")
BLOOM_API_KEY_1 = os.getenv("BLOOM_API_KEY_1")
BLOOM_API_KEY_2 = os.getenv("BLOOM_API_KEY_2")
BLOOM_API_KEY_3 = os.getenv("BLOOM_API_KEY_3")


class BloomCog(commands.Cog):
    """BloomBot personality packaged as a Cog."""

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
            "Boys, let's conquer the day with joy!"
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
        self.keywords = {
            "grimm": [
                "Grimm is my spooky bestie.",
                "He acts tough, but he's a sweetheart."
            ],
            "curse": [
                "Curse is such a gremlin cat. I love him!",
                "He tried to eat my controller again..."
            ],
            "hug": [
                "HUG TIME! Ready or not! 🥢",
                "*wraps you in love and chaos*"
            ],
            "sing": self.pretty_little_baby_lines,
            "boba": [
                "Bubble tea buddies unite!",
                "I could drink boba all day!"
            ],
            "compliment": [
                "You're shining brighter than my glitter!",
                "Compliments inbound: you're amazing!"
            ],
            "queen": self.queen_lines,
            "girl": self.queen_lines,
            "girls": self.queen_lines,
            "boy": self.boy_lines,
            "boys": self.boy_lines,
            "squad": [
                "GOON SQUAD roll call: Grimm 💀, Bloom 🌸, Curse 🐾. Chaos and comfort!"
            ]
        }

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bloom cog loaded.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        lowered = message.content.lower()
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
            "Believe in yourself, or I’ll believe for you!"
        ]
        await ctx.send(random.choice(cheers))

    @commands.command()
    async def sparkle(self, ctx):
        await ctx.send("*throws confetti and joy everywhere* ✨")

    @commands.command()
    async def drama(self, ctx):
        await ctx.send("Server musical when? Grimm can be the lead skeleton!")

    @commands.command()
    async def bloom(self, ctx):
        await ctx.send("That’s me! Ready to brighten your day!")

    @commands.command()
    async def mood(self, ctx):
        moods = ["Hyper!", "Bouncy!", "Sparkly!",
                 "Soft & sunny!", "Chaotic Good."]
        await ctx.send(f"Bloom’s mood: {random.choice(moods)}")

    @commands.command()
    async def improv(self, ctx):
        await ctx.send("Quick! You’re a cat! I’m a banshee! GO!")

    @commands.command()
    async def squad(self, ctx):
        await ctx.send("The GOON SQUAD is: Grimm 💀, Bloom 🌸, Curse 🐾. Best crew ever!")

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


async def setup(bot: commands.Bot):
    """Load the cog."""
    await bot.add_cog(BloomCog(bot))
