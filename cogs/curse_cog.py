
import discord
from discord.ext import commands, tasks
import random
import os
from dotenv import load_dotenv
from pathlib import Path
COG_VERSION = "1.2"

# Load a single shared configuration file for all bots
ENV_PATH = Path(__file__).resolve().parents[1] / "config" / "setup.env"
load_dotenv(ENV_PATH)
DISCORD_TOKEN = os.getenv("CURSE_DISCORD_TOKEN")
CURSE_API_KEY_1 = os.getenv("CURSE_API_KEY_1")
CURSE_API_KEY_2 = os.getenv("CURSE_API_KEY_2")
CURSE_API_KEY_3 = os.getenv("CURSE_API_KEY_3")


class CurseCog(commands.Cog):
    """CurseBot personality packaged as a Cog. Version 1.1."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cursed_user_id = None
        self.cursed_user_name = None
        self.curse_responses = [
            "You smell like expired sushi. 🤢",
            "Did you really think that would work? Cursed move.",
            "I’d help, but I’m morally opposed to effort.",
            "You're cursed. Figure it out. 😽",
            "Lick my paw and mind your business.",
            "Hope you like hairballs in your shoes.",
            "Your luck is as bad as your taste in cat food.",
            "May your pillow forever smell of catnip."
        ]
        self.curse_keywords = {
            "grimm": ["Oh look, it’s the spooky skeleton again."],
            "bloom": ["Too much glitter. Not enough chaos."],
            "sushi": ["BACK OFF. It’s mine."],
            "pet": ["Touch me and lose a finger."],
            "curse": ["You rang? Someone's getting hexed."],
            "meow": ["I'm not cute. I’m cursed. Get it right."],
            "tuna": ["Step away from the tuna."],
            "treat": ["No treats for you."],
            "cursed": ["Curse intensifies."]
        }
        self.gifts = [
            {"name": "a bucket of fent", "positive": False},
            {"name": "some fresh sushi", "positive": True},
            {"name": "a cursed hairball", "positive": False},
            {"name": "a shiny fish scale", "positive": True},
            {"name": "a slightly chewed toy mouse", "positive": False},
            {"name": "a jar of ghost peppers", "positive": False},
            {"name": "a mysterious paw print", "positive": False},
            {"name": "a half-empty bottle of catnip", "positive": True},
            {"name": "a tiny scythe keychain", "positive": True},
            {"name": "a worn out scratching post", "positive": False},
            {"name": "a glitter bomb from Bloom", "positive": True},
            {"name": "a sardine-scented candle", "positive": False},
            {"name": "a skeleton shaped cookie", "positive": True},
            {"name": "a bottle of midnight ink", "positive": True},
            {"name": "a creepy lullaby record", "positive": False},
            {"name": "a stack of ominous fortunes", "positive": False},
            {"name": "a black lace collar", "positive": False},
            {"name": "a box of ancient bones", "positive": False},
            {"name": "a cracked mirror shard", "positive": False},
            {"name": "a haunted feather toy", "positive": False},
            {"name": "a whispering seashell", "positive": True},
            {"name": "a mysterious potion vial", "positive": False},
            {"name": "a cursed collar bell", "positive": False},
            {"name": "a pair of glow-in-the-dark eyes", "positive": True},
            {"name": "a bag of shadow dust", "positive": False},
            {"name": "a mini spellbook", "positive": True},
            {"name": "a jar of swirling mist", "positive": False},
            {"name": "a spiky chew toy", "positive": True},
            {"name": "a midnight-blue ribbon", "positive": True},
            {"name": "a scratched-up diary", "positive": False},
            {"name": "a sinister plush bat", "positive": True},
            {"name": "a tattered pirate flag", "positive": False},
            {"name": "a small potion of mischief", "positive": True},
            {"name": "a cursed fortune cookie", "positive": False},
            {"name": "a cracked crystal ball", "positive": False},
            {"name": "a pinch of phantom fur", "positive": False},
            {"name": "a haunted treat bag", "positive": False},
            {"name": "a glow stick stash", "positive": True},
            {"name": "a vial of spooky slime", "positive": False},
            {"name": "a lock of spectral hair", "positive": False},
            {"name": "a weathered treasure map", "positive": True},
            {"name": "a bowl of strange soup", "positive": False},
            {"name": "a ball of tangled yarn", "positive": True},
            {"name": "a rogue lightning bug", "positive": True},
            {"name": "a packet of dry ice", "positive": False},
            {"name": "a cat-shaped voodoo doll", "positive": False},
            {"name": "a cursed sticker pack", "positive": False},
            {"name": "a gnarled tree branch", "positive": False},
            {"name": "a bag of sour candy", "positive": True},
            {"name": "an ominous black envelope", "positive": False},
        ]
        self.positive_gift_responses = [
            "Curse reluctantly gives you {gift}.",
            "With a sly grin, Curse drops {gift} in your lap.",
            "Curse acts indifferent but slides you {gift}.",
        ]
        self.negative_gift_responses = [
            "Curse hisses and tosses {gift} at you.",
            "You get {gift}. Curse smirks wickedly.",
            "Curse dumps {gift} on you with a laugh.",
        ]
        self.pick_daily_cursed.start()
        self.daily_gift.start()

    @tasks.loop(hours=24)
    async def pick_daily_cursed(self):
        guild = discord.utils.get(self.bot.guilds)
        if not guild:
            return
        members = [m for m in guild.members if not m.bot]
        if not members:
            return
        chosen = random.choice(members)
        self.cursed_user_id = chosen.id
        self.cursed_user_name = chosen.display_name
        channel = discord.utils.get(
            guild.text_channels, name="general") or guild.text_channels[0]
        await channel.send(f"😼 A new curse has been cast... {self.cursed_user_name} is now cursed for 24 hours.")

    @tasks.loop(hours=24)
    async def daily_gift(self):
        """Give a random user a random gift from Curse."""
        guild = discord.utils.get(self.bot.guilds)
        if not guild:
            return
        members = [m for m in guild.members if not m.bot]
        if not members:
            return
        recipient = random.choice(members)
        gift = random.choice(self.gifts)
        channel = discord.utils.get(guild.text_channels, name="general") or guild.text_channels[0]
        if gift["positive"]:
            line = random.choice(self.positive_gift_responses)
        else:
            line = random.choice(self.negative_gift_responses)
        await channel.send(f"🎁 {recipient.display_name}, " + line.format(gift=gift['name']))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Curse cog loaded.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        lowered = message.content.lower()
        if message.author.id == self.cursed_user_id and random.random() < 0.2:
            await message.channel.send(f"{message.author.display_name}, {random.choice(self.curse_responses)}")
            return
        for trigger, responses in self.curse_keywords.items():
            if trigger in lowered:
                await message.channel.send(random.choice(responses))
                return

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def curse(self, ctx, member: discord.Member):
        self.cursed_user_id = member.id
        self.cursed_user_name = member.display_name
        await ctx.send(f"😾 Manual curse activated. {member.display_name} is now cursed.")

    @commands.command()
    async def whois_cursed(self, ctx):
        if self.cursed_user_name:
            await ctx.send(f"😼 {self.cursed_user_name} is still cursed... for now.")
        else:
            await ctx.send("No one's cursed. Weak.")

    @commands.command()
    async def sushi(self, ctx):
        await ctx.send("🍣 You’re not worthy of the sacred tuna.")

    @commands.command()
    async def flick(self, ctx):
        await ctx.send("*flicks tail in mild contempt*")

    @commands.command()
    async def insult(self, ctx):
        burns = [
            "You're the reason instructions exist.",
            "If I had feelings, you'd hurt them.",
            "You bring shame to sushi lovers everywhere.",
            "Your aura is soggy cardboard."
        ]
        await ctx.send(random.choice(burns))

    @commands.command()
    async def hiss(self, ctx):
        await ctx.send("Hissss! Keep your distance.")

    @commands.command()
    async def scratch(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send(f"*scratches {member.display_name} just because*")

    @commands.command()
    async def pet(self, ctx):
        """Attempt to pet Curse."""
        if random.random() < 0.5:
            await ctx.send("😼 *purrs softly* Maybe I'll spare you... for now.")
        else:
            await ctx.send(
                f"*scratches {ctx.author.display_name} and hisses.* You're cursed now!"
            )
            self.cursed_user_id = ctx.author.id
            self.cursed_user_name = ctx.author.display_name
            try:
                await ctx.author.edit(nick=f"Cursed {ctx.author.display_name}")
            except discord.Forbidden:
                pass
            guild = ctx.guild
            role = discord.utils.get(guild.roles, name="Cursed")
            if role is None:
                role = await guild.create_role(
                    name="Cursed", colour=discord.Colour.purple()
                )
            try:
                await ctx.author.add_roles(role)
            except discord.Forbidden:
                pass

    @commands.command()
    async def curse_me(self, ctx):
        self.cursed_user_id = ctx.author.id
        self.cursed_user_name = ctx.author.display_name
        await ctx.send(f"😾 Fine. {ctx.author.display_name} is now cursed.")

    @commands.command()
    async def hairball(self, ctx):
        """Share a lovely hairball."""
        await ctx.send("*coughs up a hairball on your shoes*")

    @commands.command()
    async def pounce(self, ctx, member: discord.Member | None = None):
        """Pounce on someone."""
        member = member or ctx.author
        await ctx.send(f"*pounces on {member.display_name} unexpectedly*")

    @commands.command()
    async def nap(self, ctx):
        """Announce that Curse is taking a nap."""
        await ctx.send("😼 Curling up for a nap. Don't bother me.")


async def setup(bot: commands.Bot):
    """Load the cog."""
    await bot.add_cog(CurseCog(bot))
