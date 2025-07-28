import dotenv; dotenv.load_dotenv()
import os
import discord
import openai

TOKEN = os.getenv('DISCORD_TOKEN_BOT3')
OPENAI_KEY = os.getenv('OPENAI_API_KEY_BOT3')

openai.api_key = OPENAI_KEY

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"bot3 logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith('!bot3'):
        prompt = message.content[len('!bot3'):].strip()
        if not prompt:
            await message.channel.send('Hello from bot3!')
            return
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        await message.channel.send(response.choices[0].message.content)

def main():
    if not TOKEN:
        raise ValueError('DISCORD_TOKEN_BOT3 is not set')
    client.run(TOKEN)

if __name__ == '__main__':
    main()
