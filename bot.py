import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    port = int(os.environ.get("PORT", 10000))  # Use Render's provided PORT, fallback to 10000 locally
    print(f"[Flask] Running on port {port}")
    app.run(host='0.0.0.0', port=port)

Thread(target=run).start()

# ENABLE INTENTS
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Replace with your user ID
YOUR_USER_ID = 759934480696999968

# Replace with the channel ID you want to monitor
CHANNEL_ID = 1398061028020981900

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == CHANNEL_ID:
        try:
            # Send message content to your DM
            user = await bot.fetch_user(YOUR_USER_ID)
            await user.send(f"{message.author} suggested: {message.content}")
            await message.delete()
        except Exception as e:
            print(f"Error: {e}")

    await bot.process_commands(message)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
if BOT_TOKEN is None:
    raise ValueError("Missing BOT_TOKEN environment variable.")
bot.run(BOT_TOKEN)
