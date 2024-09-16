import discord
from discord.ext import commands, tasks
import os
import asyncio
from itertools import cycle

discord.utils.setup_logging()
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

bot_statuses = cycle(["Status One", "Status Two", "Status Three", "Finished!"])

@tasks.loop(seconds=30)
async def change_bot_status():
    await bot.change_presence(activity=discord.Game(next(bot_statuses)))

@bot.event 
async def on_ready():
    print("Bot ready!")
    change_bot_status.start()
    try:
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        print("An error with syncing application commands has occurred: ", e)

@bot.tree.command(name="hello", description="Says hello back to the command user")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention} Hello there!")


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello there, {ctx.author.mention}!")

@bot.command(aliases=["gm", "morning"])
async def goodmorning(ctx):
    await ctx.send(f"Good morning, {ctx.author.mention}!")

with open("token.txt") as file:
    token = file.read()

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start(token)

asyncio.run(main())




