# Personality Customization

Each bot keeps its stock one‑liners in arrays inside the bot's Python file. To tweak a bot's vibe or add new jokes simply append to these lists. For example `grimm_bot.py` defines a large `grimm_responses` array.

If the lists start getting unwieldy you can move them into JSON files and load them at runtime:

```python
import json
with open("data/grimm_responses.json") as f:
    grimm_responses = json.load(f)
```

Feel free to submit PRs expanding the lines for Grimm, Bloom or Curse—the more personality the better.
