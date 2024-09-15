import discord
from discord.ext import commands
from random import choice
import asyncpraw as praw

class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id="wd1I6Z0KHb-BUj8oUr0hPw", client_secret="NWXPZB2GArXrFl7DZQCCJBs6Tu8TRw", user_agent="script:developmentpractice:v1.0 (by u/DisputedGlory)")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready!")

    @commands.command()
    async def gaming(self, ctx: commands.Context):
        
        subreddit = await self.reddit.subreddit("gaming")
        posts_list = []

        async for post in subreddit.hot(limit=25):
            if not post.over_18 and post.author is not None and any(post.url.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif"]):
                author_name = post.author.name
                posts_list.append((post.url, post.title, author_name))
            if post.author is None:
                posts_list.append((post.url, post.title, "N/A"))

        if posts_list:

            random_post = choice(posts_list)

            gaming_embed = discord.Embed(title= random_post[1], color=discord.Color.random()
            )
            gaming_embed.set_author(name=f"Post requested by {ctx.author.name}", icon_url=ctx.author.avatar)
            gaming_embed.set_image(url=random_post[0])
            gaming_embed.set_footer(text=f"Post created by {random_post[2]}.", icon_url=None)
            await ctx.send(embed=gaming_embed)

        else:
            await ctx.send("Unable to fetch post, try again later.")

    def cog_unload(self):
        self.bot.loop.create_task(self.reddit.close())

async def setup(bot):
    await bot.add_cog(Reddit(bot))