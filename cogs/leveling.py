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

    # =========================================
    # LOAD XP
    # =========================================
    def load_data(self):

        with open("data/levels.json", "r") as f:
            return json.load(f)

    # =========================================
    # SAVE XP
    # =========================================
    def save_data(self, data):

        with open("data/levels.json", "w") as f:
            json.dump(data, f, indent=4)

    # =========================================
    # XP EVENT
    # =========================================
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        data = self.load_data()

        user_id = str(message.author.id)

        # register user baru
        if user_id not in data:
            data[user_id] = 0

        xp_gain = 5

        # VIP BONUS
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
                "⬆️ LEVEL UP!",
                f"{message.author.mention} reached level **{level}** 🎉"
            )

            await message.channel.send(embed=embed)

            # =====================================
            # ACHIEVEMENT SYSTEM
            # =====================================
            achievement_cog = self.bot.get_cog(
                "Achievements"
            )

            if achievement_cog:

                fake_ctx = await self.bot.get_context(
                    message
                )

                # LEVEL 5
                if level >= 5:

                    await achievement_cog.give_achievement(
                        fake_ctx,
                        message.author,
                        "level_5",
                        "🌱 Beginner"
                    )

                # LEVEL 10
                if level >= 10:

                    await achievement_cog.give_achievement(
                        fake_ctx,
                        message.author,
                        "level_10",
                        "⚡ Active"
                    )

            await message.channel.send(embed=embed)

    # =========================================
    # LEVEL COMMAND
    # =========================================
    @commands.command()
    async def level(self, ctx, member: discord.Member = None):

        member = member or ctx.author

        data = self.load_data()

        user_id = str(member.id)

        xp = data.get(user_id, 0)

        level = xp // 100

        embed = default_embed(
            "📊 LEVEL SYSTEM"
        )

        embed.set_thumbnail(
            url=member.avatar.url
            if member.avatar
            else member.default_avatar.url
        )

        embed.add_field(
            name="👤 User",
            value=member.display_name,
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

    # =========================================
    # GLOBAL LEVEL LEADERBOARD
    # =========================================
    @commands.command()
    async def globallevel(self, ctx):

        data = self.load_data()

        leaderboard = []

        # ambil semua user
        for user_id, xp in data.items():

            level = xp // 100

            leaderboard.append(
                (int(user_id), level, xp)
            )

        # sort berdasarkan XP
        leaderboard.sort(
            key=lambda x: x[2],
            reverse=True
        )

        embed = discord.Embed(
            title="🌍 GLOBAL LEVEL LEADERBOARD",
            description="🏆 Top LeonBot Users",
            color=0x5865F2
        )

        # top 10
        for i, (user_id, level, xp) in enumerate(
            leaderboard[:10],
            start=1
        ):

            # ambil member dari server
            member = ctx.guild.get_member(user_id)

            if member:
                username = member.display_name
            else:
                username = "Unknown User"

            medals = {
                1: "🥇",
                2: "🥈",
                3: "🥉"
            }

            medal = medals.get(i, "🏅")

            embed.add_field(
                name=f"{medal} #{i} • {username}",
                value=(
                    f"🏆 Level: **{level}**\n"
                    f"⚡ XP: **{xp}**"
                ),
                inline=False
            )

        embed.set_footer(
            text="LeonBot • Futuristic Leveling System"
        )

        await ctx.send(embed=embed)


# =========================================
# LOAD COG
# =========================================
async def setup(bot):

    await bot.add_cog(Leveling(bot))