import discord
from discord.ext import commands
import json

from utils.theme import (
    default_embed
)

from utils.economy_utils import (
    load_data,
    create_account,
    format_money
)


class Profile(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # PROFILE
    # =========================
    @commands.command(aliases=["pf"])
    async def profile(
        self,
        ctx,
        member: discord.Member = None
    ):

        if member is None:
            member = ctx.author

        # =========================
        # LOAD ECONOMY DATA
        # =========================
        data = load_data()

        create_account(data, member.id)

        user = data[str(member.id)]

        wallet = user["wallet"]
        bank = user["bank"]

        total = wallet + bank

        # =========================
        # LOAD LEVEL DATA
        # =========================
        try:

            with open("data/levels.json", "r") as f:

                level_data = json.load(f)

        except:

            level_data = {}

        xp = 0
        level = 0

        if str(member.id) in level_data:

            xp = level_data[str(member.id)]

            level = xp // 100

        # =========================
        # LOAD ACHIEVEMENTS DATA
        # =========================
        try:

            with open(
                "data/achievements.json",
                "r"
            ) as f:

                achievement_data = json.load(f)

        except:

            achievement_data = {}

        user_achievements = achievement_data.get(
            str(member.id),
            []
        )

        # =========================
        # LEADERBOARD RANK
        # =========================
        leaderboard = []

        for user_id, user_data in data.items():

            total_money = (
                user_data["wallet"] +
                user_data["bank"]
            )

            leaderboard.append(
                (user_id, total_money)
            )

        leaderboard = sorted(
            leaderboard,
            key=lambda x: x[1],
            reverse=True
        )

        rank = 1

        for i, (user_id, money) in enumerate(leaderboard):

            if str(member.id) == str(user_id):

                rank = i + 1
                break

        # =========================
        # EMBED
        # =========================
        embed = default_embed(
            "🌌 LEON PROFILE",
            (
                f"👤 User: {member.mention}\n"
                f"🏆 Rank: `#{rank}`"
            )
        )

        # ECONOMY
        embed.add_field(
            name="💰 Economy",
            value=(
                f"💵 Wallet: `{format_money(wallet)}`\n"
                f"🏦 Bank: `{format_money(bank)}`\n"
                f"💎 Total: `{format_money(total)}`"
            ),
            inline=True
        )

        # LEVELING
        embed.add_field(
            name="🏆 Leveling",
            value=(
                f"⭐ Level: `{level}`\n"
                f"✨ XP: `{xp}`"
            ),
            inline=True
        )

        # =========================
        # ACHIEVEMENTS
        # =========================
        if user_achievements:

            achievement_icons = {

                "vip": "💎",
                "gambler": "🎲",
                "jackpot": "🎰",
                "level_5": "🌱",
                "level_10": "⚡"
            }

            achievement_text = ""

            for achievement in user_achievements:

                achievement_text += (
                    f"{achievement_icons.get(achievement, '🏆')} "
                )

        else:

            achievement_text = (
                "Belum ada achievement."
            )

        embed.add_field(
            name="🏆 Achievements",
            value=achievement_text,
            inline=False
        )

        # INFO

        # VIP BADGE
        vip_role = discord.utils.get(
            member.roles,
            name="VIP"
        )

        if vip_role:

            embed.add_field(
                name="👑 VIP STATUS",
                value="🌟 VIP MEMBER",
                inline=True
            )

        embed.add_field(
            name="🤖 LeonBot",
            value=(
                "⚡ Futuristic User Profile\n"
                "🌌 Competitive Economy System"
            ),
            inline=True
        )

        # THUMBNAIL
        if member.avatar:

            embed.set_thumbnail(
                url=member.avatar.url
            )

        await ctx.send(embed=embed)


# =========================
# SETUP
# =========================
async def setup(bot):

    await bot.add_cog(Profile(bot))