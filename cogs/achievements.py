import discord
from discord.ext import commands
import json

from utils.theme import (
    default_embed,
    success_embed
)


class Achievements(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================================
    # LOAD DATA
    # =========================================
    def load_data(self):

        with open("data/achievements.json", "r") as f:
            return json.load(f)

    # =========================================
    # SAVE DATA
    # =========================================
    def save_data(self, data):

        with open("data/achievements.json", "w") as f:
            json.dump(data, f, indent=4)

    # =========================================
    # GIVE ACHIEVEMENT
    # =========================================
    async def give_achievement(
        self,
        ctx,
        member,
        achievement_id,
        achievement_name
    ):

        data = self.load_data()

        user_id = str(member.id)

        # register user
        if user_id not in data:
            data[user_id] = []

        # sudah punya achievement
        if achievement_id in data[user_id]:
            return

        # tambah achievement
        data[user_id].append(achievement_id)

        self.save_data(data)

        embed = success_embed(
            "🏆 ACHIEVEMENT UNLOCKED!",
            f"{member.mention} unlocked:\n"
            f"**{achievement_name}**"
        )

        await ctx.send(embed=embed)

    # =========================================
    # ACHIEVEMENTS COMMAND
    # =========================================
    @commands.command(
        aliases=["ach"]
    )
    async def achievements(
        self,
        ctx,
        member: discord.Member = None
    ):

        member = member or ctx.author

        data = self.load_data()

        user_id = str(member.id)

        user_achievements = data.get(user_id, [])

        achievement_list = {

            "first_money": "💸 First Money",
            "gambler": "🎲 Gambler",
            "level_5": "🌱 Beginner",
            "level_10": "⚡ Active",
            "vip": "💎 VIP"
        }

        description = ""

        if not user_achievements:

            description = "Belum punya achievements."

        else:

            for achievement in user_achievements:

                achievement_name = achievement_list.get(
                    achievement,
                    achievement
                )

                description += f"{achievement_name}\n"

        embed = default_embed(
            "🏆 LEONBOT ACHIEVEMENTS",
            description
        )

        embed.set_thumbnail(
            url=member.display_avatar.url
        )

        embed.set_footer(
            text=f"Total: {len(user_achievements)} Achievements"
        )

        await ctx.send(embed=embed)


# =========================================
# LOAD COG
# =========================================
async def setup(bot):

    await bot.add_cog(Achievements(bot))