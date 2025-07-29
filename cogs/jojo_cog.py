from discord.ext import commands, tasks
import discord
import datetime
import random

COG_VERSION = "1.4"

JOJO_DISPLAY_NAME = "JoJo is bizarre"
EMMA_NAME = "Emma"


class JojoCog(commands.Cog):
    """Send spontaneous loving messages to Emma. Version 1.4."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.loving_lines = [
            "You are wonderful, Emma! 💖",
            "Hey JoJo is bizarre, sending you big hugs!",
            "Emma, you light up this server!",
            "Just stopping by to say we adore you, JoJo!",
            "Stay amazing, Emma!",
            "Your dedication on the night shift is awe-inspiring!",
            "Waking up at 5 PM can't dim your bright spirit!",
            "Emma, you heal hearts as well as bodies.",
            "Your compassion makes the night a little brighter.",
            "Even the stars envy how you shine, RN Emma!",
            "Hope your shift is gentle and your patients grateful.",
            "You're proof that caring is a superpower.",
            "Emma, your smile could light up the whole ward!",
            "Thank you for bringing hope to those in need.",
            "May every night be kind to you and your team.",
            "You're amazing for choosing a life of service.",
            "Your kindness reaches far beyond the hospital walls.",
            "Sending good vibes as you start your shift!",
            "Emma, you're the heartbeat of the night crew.",
            "Your strength inspires everyone around you.",
            "We're grateful for the care you provide each night.",
            "Emma, you make even the toughest shifts sparkle.",
            "Remember to take care of yourself too!",
            "You're a superstar RN, never forget it.",
            "Your patience and skill save lives daily.",
            "Emma, your work is nothing short of heroic.",
            "Night shift warriors like you keep the world turning.",
            "You wake up when others wind down—true dedication!",
            "The world is better because you're in it, Emma.",
            "Your gentle touch brings comfort to many.",
            "Thank you for being a beacon of hope at night.",
            "Emma, your empathy is your greatest strength.",
            "May tonight's shift be smooth and rewarding.",
            "We're all cheering you on, night after night!",
            "Your courage in the face of fatigue is admirable.",
            "Emma, you're unstoppable even at 3 AM.",
            "You bring calm to every chaotic moment.",
            "You're as radiant as the sunset when you wake up.",
            "Never doubt the difference you make, Emma.",
            "Your dedication to healing is truly beautiful.",
            "Even after a long night, you still glow with kindness.",
            "Emma, you deserve endless gratitude for your care.",
            "Your heart is as big as your courage.",
            "You're changing lives with every shift you work.",
            "Coffee can't compete with your natural energy!",
            "Emma, may your night be filled with smooth IV starts.",
            "You have the skills of a hero and the heart of a friend.",
            "Your positive vibes are exactly what the ward needs.",
            "Wishing you a peaceful night full of smiles.",
            "You're an inspiration to us all, Emma RN!",
            "The night is brighter because you're awake.",
            "Thank you for being a guardian angel in scrubs.",
            "Your dedication is noticed and appreciated.",
            "Emma, your resilience is unmatched.",
            "May your shift be short and your breaks long!",
            "You're the kind of nurse every patient hopes for.",
            "Sending love and energy as you head to work.",
            "Emma, the world needs more hearts like yours.",
            "You juggle it all with grace and compassion.",
            "Your sense of humor makes night shift fun!",
            "You're doing incredible work every single night.",
            "Emma, keep shining like the star you are.",
            "Your caring nature lifts everyone's spirits.",
            "No matter how long the night, you never quit.",
            "You're stronger than you know, Emma.",
            "We're endlessly proud of you and your work.",
            "Your dedication helps so many people heal.",
            "Emma, your kindness is contagious.",
            "You bring comfort just by being yourself.",
            "Night after night, you make miracles happen.",
            "Your laughter is the best medicine for us all.",
            "Thank you for bringing warmth to late-night halls.",
            "Emma, your compassion has no limit.",
            "Your optimism brightens even the gloomiest ward.",
            "The world needs more nurses like you.",
            "You rise and shine when others settle in.",
            "Emma, your heart beats with kindness.",
            "You make everyone feel safe and cared for.",
            "The hospital is lucky to have you each night.",
            "Your dedication turns exhaustion into triumph.",
            "Emma, you inspire everyone around you.",
            "Wishing you strength for your shift ahead.",
            "Your patience is a gift to your patients.",
            "You radiate comfort and care.",
            "Emma, your every action shows pure dedication.",
            "You're the calm in the middle of the night shift storm.",
            "Hope your coffee is strong and your night easy!",
            "Your patients are in the best hands with you.",
            "Emma, thank you for all the lives you touch.",
            "Your compassion knows no bounds.",
            "You have a heart of gold under those scrubs.",
            "The night sky isn't the only thing that sparkles—you do too!",
            "Emma, keep making the world better one shift at a time.",
            "Your dedication never ceases to amaze us.",
            "You are a force of good and kindness.",
            "Even the moon can't match your glow at night.",
            "Wishing you moments of rest between saving lives.",
            "Emma, you embody the spirit of care and compassion.",
            "You're proof that heroes wear scrubs, not capes.",
            "Never forget how appreciated you are.",
            "Your work ethic sets the bar high for us all.",
            "Emma, you bring light into every dark hallway.",
            "You are appreciated more than words can say.",
            "Your courage inspires everyone to be better.",
            "May tonight's patients recognize your dedication.",
        ]
        self.daily_message.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        if message.author.display_name == JOJO_DISPLAY_NAME and random.random() < 0.2:
            await message.channel.send(random.choice(self.loving_lines))

    @commands.command(name="jojo")
    async def jojo_cmd(self, ctx):
        """Send a random loving message to Emma."""
        await ctx.send(random.choice(self.loving_lines))

    @tasks.loop(time=datetime.time(hour=17, minute=0))
    async def daily_message(self):
        """Automatically send a loving line at 5 PM each day."""
        guild = discord.utils.get(self.bot.guilds)
        if not guild:
            return
        channel = (
            discord.utils.get(guild.text_channels, name="general")
            or guild.text_channels[0]
        )
        await channel.send(random.choice(self.loving_lines))


async def setup(bot: commands.Bot):
    await bot.add_cog(JojoCog(bot))
