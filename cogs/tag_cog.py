import json
from pathlib import Path
from discord.ext import commands

COG_VERSION = "1.0"

TAGS_PATH = Path("config/tags.json")


def load_tags() -> dict:
    if TAGS_PATH.exists():
        try:
            return json.loads(TAGS_PATH.read_text())
        except Exception:
            return {}
    return {}


def save_tags(data: dict) -> None:
    TAGS_PATH.write_text(json.dumps(data, indent=2))


class TagCog(commands.Cog):
    """Store and retrieve text snippets."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.tags = load_tags()

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, name: str | None = None):
        """Retrieve a tag or show usage."""
        if not name:
            await ctx.send("Use `tag list` or `tag save <name> <text>`.")
            return
        text = self.tags.get(name.lower())
        if text:
            await ctx.send(text)
        else:
            await ctx.send("Tag not found.")

    @tag.command(name="save")
    @commands.has_permissions(manage_guild=True)
    async def tag_save(self, ctx, name: str, *, content: str):
        """Save a new tag."""
        self.tags[name.lower()] = content
        save_tags(self.tags)
        await ctx.send(f"Saved tag `{name}`.")

    @tag.command(name="delete")
    @commands.has_permissions(manage_guild=True)
    async def tag_delete(self, ctx, name: str):
        """Delete a tag."""
        if name.lower() in self.tags:
            del self.tags[name.lower()]
            save_tags(self.tags)
            await ctx.send(f"Deleted tag `{name}`.")
        else:
            await ctx.send("Tag not found.")

    @tag.command(name="list")
    async def tag_list(self, ctx):
        """List available tags."""
        if self.tags:
            await ctx.send(", ".join(sorted(self.tags.keys())))
        else:
            await ctx.send("No tags saved.")


async def setup(bot: commands.Bot):
    await bot.add_cog(TagCog(bot))
