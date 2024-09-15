import discord
from discord.ext import commands
import os
import asyncio

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event 
async def on_ready():
    print("Bot ready!")

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




