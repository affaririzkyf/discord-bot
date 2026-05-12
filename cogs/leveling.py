import discord
from discord.ext import commands
import json

from utils.theme import (
    default_embed,
    success_embed,
    error_embed
)

class Leveling(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # LOAD XP
    # =========================
    def load_data(self):

        with open("data/levels.json", "r") as f:
            return json.load(f)

    # =========================
    # SAVE XP
    # =========================
    def save_data(self, data):

        with open("data/levels.json", "w") as f:
            json.dump(data, f, indent=4)

    # =========================
    # XP EVENT
    # =========================
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        data = self.load_data()

        user_id = str(message.author.id)

        if user_id not in data:
            data[user_id] = 0

        xp_gain = 5

        vip_role = discord.utils.get(
            message.author.roles,
            name="VIP"
        )

        if vip_role:

            xp_gain *= 2

        data[user_id] += xp_gain

        level = data[user_id] // 100

        self.save_data(data)

        # LEVEL UP
        if data[user_id] % 100 == 0:

            embed = success_embed(
                "⬆️ Level Up!",
                f"{message.author.mention} reached level **{level}** 🎉"
            )

            await message.channel.send(embed=embed)

    # =========================
    # LEVEL COMMAND
    # =========================
    @commands.command()
    async def level(self, ctx, member: discord.Member = None):

        member = member or ctx.author

        data = self.load_data()

        user_id = str(member.id)

        xp = data.get(user_id, 0)

        level = xp // 100

        embed = default_embed(
            "📊 Level System"
        )

        embed.set_thumbnail(
            url=member.avatar.url if member.avatar else member.default_avatar.url
        )

        embed.add_field(
            name="👤 User",
            value=member.mention,
            inline=False
        )

        embed.add_field(
            name="⭐ XP",
            value=xp,
            inline=True
        )

        embed.add_field(
            name="⬆️ Level",
            value=level,
            inline=True
        )

        await ctx.send(embed=embed)

# =========================
# LOAD COG
# =========================
async def setup(bot):

    await bot.add_cog(Leveling(bot))