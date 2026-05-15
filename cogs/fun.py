import discord
from discord.ext import commands
from utils.theme import (
    default_embed,
    success_embed,
    error_embed
)
import random

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # PING COMMAND
    # =========================
    @commands.hybrid_command()
    async def ping(self, ctx):

        ping = round(self.bot.latency * 1000)

        embed = success_embed(
            "🏓 Pong!",
            f"Latency: **{ping}ms**"
        )

        # =========================
        # AUTHOR
        # =========================
        embed.set_author(
            name="LeonBot System",
            icon_url=self.bot.user.avatar.url
        )

        # =========================
        # THUMBNAIL
        # =========================
        if self.bot.user.avatar:

            embed.set_thumbnail(
                url=self.bot.user.avatar.url
            )

        await ctx.send(embed=embed)

    # =========================
    # HELLO COMMAND
    # =========================
    @commands.hybrid_command()
    async def hello(self, ctx):

        embed = default_embed(
            "👋 Hello!",
            f"Welcome {ctx.author.mention}"
        )

        embed.set_author(
            name="LeonBot Greeting System",
            icon_url=self.bot.user.avatar.url
        )

        if self.bot.user.avatar:

            embed.set_thumbnail(
                url=self.bot.user.avatar.url
            )

        await ctx.send(embed=embed)

    # =========================
    # ROLL COMMAND
    # =========================
    @commands.hybrid_command()
    async def roll(self, ctx):

        number = random.randint(1, 100)

        embed = default_embed(
            "🎲 Dice Roll",
            f"You rolled **{number}**"
        )

        embed.set_author(
            name="LeonBot Fun System",
            icon_url=self.bot.user.avatar.url
        )

        if self.bot.user.avatar:

            embed.set_thumbnail(
                url=self.bot.user.avatar.url
            )

        embed.set_image(
             url="https://i.imgur.com/AfFp7pu.png"
        )

        await ctx.send(embed=embed)

# =========================
# LOAD COG
# =========================
async def setup(bot):

    await bot.add_cog(Fun(bot))