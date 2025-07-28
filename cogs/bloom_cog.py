from discord.ext import commands
import random
import os
from dotenv import load_dotenv

load_dotenv("config/bloom.env")
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
            "sing": [
                "Let’s karaoke! I call lead!",
                "SING IT OUT! LOUDER!"
            ],
            "boba": [
                "Bubble tea buddies unite!",
                "I could drink boba all day!"
            ],
            "compliment": [
                "You're shining brighter than my glitter!",
                "Compliments inbound: you're amazing!"
            ],
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
        await ctx.send("*bursts into a Broadway solo* 🎙️✨")

    @commands.command()
    async def karaoke(self, ctx, *, song: str | None = None):
        """Start a mini karaoke moment."""
        lines = [
            "Don’t stop believin’!",
            "Let it gooooooo!",
            "Mamma mia, here I go again!",
            "Just a small-town girl, living in a lonely world…",
        ]
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
        moods = ["Hyper!", "Bouncy!", "Sparkly!", "Soft & sunny!", "Chaotic Good."]
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

