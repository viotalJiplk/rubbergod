import datetime
from random import choice

import discord
from discord.ext import commands

import utils
from config import config, messages

config = config.Config
messages = messages.Messages

uhoh_counter = 0
arcas_time = (datetime.datetime.utcnow() -
              datetime.timedelta(hours=config.arcas_delay))


class Meme(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        global uhoh_counter

        if message.author.bot:
            return

        elif config.uhoh_string in message.content.lower():
            await message.channel.send("uh oh")
            uhoh_counter += 1
        elif message.content == "PR":
            await message.channel.send(messages.pr_meme)

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        global arcas_time
        if arcas_time + datetime.timedelta(hours=config.arcas_delay) <\
           when and config.arcas_id == user.id:
            arcas_time = when
            gif = discord.Embed()
            gif.set_image(url="https://i.imgur.com/v2ueHcl.gif")
            await channel.send(embed=gif)

    @commands.command()
    async def uhoh(self, ctx):
        await ctx.send(messages.uhoh_counter.format(uhohs=uhoh_counter))
        await ctx.send("Testing reload and pull")

    @commands.cooldown(rate=5, per=20.0, type=commands.BucketType.user)
    @commands.command()
    async def hug(self, ctx, user: discord.Member = None, intensity: int = 0):
        """Because everyone likes hugs"""
        if user is None:
            user = ctx.author
        elif user == self.bot.user:
            await ctx.send("<:huggers:602823825880514561>")
            return

        emojis = config.hug_emojis

        user = discord.utils.escape_markdown(user.display_name)
        if 0 <= intensity < len(emojis):
            await ctx.send(emojis[intensity] + f" **{user}**")
        else:
            await ctx.send(choice(emojis) + f" **{user}**")

    @hug.error
    async def hug_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(
                messages.member_not_found
                .format(user=utils.generate_mention(ctx.author.id)))


def setup(bot):
    bot.add_cog(Meme(bot))
