# Creating New Cogs

So you want to add your own flavor to the Goon Squad? It's easy. Each cog is a
standard `discord.py` extension stored in the `cogs/` folder.

1. Create `cogs/my_cog.py` and define a subclass of `commands.Cog` with your
   commands.
2. Add an `async def setup(bot)` function that adds the cog:

```python
class MyCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello world!")

async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

3. When running `goon_bot.py`, it will automatically load any file ending with
   `_cog.py`. To load it manually, use the admin commands:

```
!load my_cog
```

That's all there is to it. Keep your cogs small and focused, and bump the
`COG_VERSION` constant if you make updates.

### Logging from your cog
Import `log_message` and sprinkle it around to see colored logs in the console:

```python
from src.logger import log_message

log_message("MyCog loaded")
```
