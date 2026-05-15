import discord
from discord.ext import commands

from utils.theme import (
    default_embed,
    success_embed,
    error_embed
)

class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # HELP COMMAND
    # =========================
    @commands.hybrid_command()
    async def help(self, ctx):

        embed = default_embed(
            "📚 LEONBOT COMMANDS",
            "⚡ Futuristic Discord Bot"
        )

        # FUN
        embed.add_field(
            name="🎮 Fun",
            value=(
                "`$ping`\n"
                "`$hello`\n"
                "`$roll`"
            ),
            inline=True
        )

        # UTILITY
        embed.add_field(
            name="🛠 Utility",
            value=(
                "`$help`\n"
                "`$about`\n"
                "`$info`\n"
                "`$userinfo`\n"
                "`$avatar`\n"
                "`$server`"
            ),
            inline=True
        )

        # MODERATION
        embed.add_field(
            name="🛡 Moderation",
            value=(
                "`$clear`\n"
                "`$kick`\n"
                "`$ban`\n"
                "`$timeout`\n"
                "`$untimeout`\n"
                "`$addrole`\n"
                "`$removerole`"
            ),
            inline=True
        )

        # LEVELING
        embed.add_field(
            name="🏆 Leveling",
            value=(
                "`$level`\n"
                "`$globallevel`"
            ),
            inline=True
        )

        # ECONOMY
        embed.add_field(
            name="💰 Economy",
            value=(
                "`$bal`\n"
                "`$daily`\n"
                "`$work`\n"
                "`$beg`\n"
                "`$pay`\n"
                "`$deposit`\n"
                "`$withdraw`\n"
                "`$rich`"
            ),
            inline=True
        )

        # GAMES
        embed.add_field(
            name="🎰 Games",
            value=(
                "`$slot`\n"
                "`$coinflip`\n"
                "`$dice`\n"
                "`$guessnumber`"
            ),
            inline=True
        )

        # PROFILE
        embed.add_field(
            name="🌌 Profile",
            value=(
                "`$profile`\n"
                "`$achievements`\n"
                "`$pf`"
            ),
            inline=True
        )

        # SHOP
        embed.add_field(
            name="🛒 Shop",
            value=(
                "`$shop`\n"
                "`$buy`"
            ),
            inline=True
        )

        # OWNER
        embed.add_field(
            name="👑 Owner",
            value=(
                "`$shutdown`\n"
                "`$resetlevels`\n"
                "`$leave`\n"
                "`$reload`\n"
                "`$load`\n"
                "`$unload`\n"
                "`$addmoney`\n"
                "`$removemoney`\n"
                "`$setmoney`\n"
                "`$giveall`"
            ),
            inline=True
        )

        await ctx.send(embed=embed)
        
    # =========================
    # ABOUT
    # =========================
    @commands.hybrid_command()
    async def about(self, ctx):

        # PING
        ping = round(
            self.bot.latency * 1000
        )

        # SERVER COUNT
        server_count = len(
            self.bot.guilds
        )

        # USER COUNT
        user_count = 0

        for guild in self.bot.guilds:

            user_count += guild.member_count

        # EMBED
        embed = default_embed(
            "💠 🤖 ABOUT LEONBOT",
            (
                "⚡ Futuristic Discord Bot\n"
                "🌌 Competitive Economy System\n"
                "🎮 Minigames & Gambling\n"
                "🛡 Advanced Moderation\n"
                "🏆 Leveling & Profile System"
            )
        )

        # DEVELOPER
        embed.add_field(
            name="👨‍💻 Developer",
            value="@maumandiajah",
            inline=True
        )

        # LIBRARY
        embed.add_field(
            name="📚 Library",
            value="discord.py",
            inline=True
        )

        # PREFIX
        embed.add_field(
            name="⚙ Prefix",
            value="`$`",
            inline=True
        )

        # VERSION
        embed.add_field(
            name="📦 Version",
            value="`v1.0.0`",
            inline=True
        )

        # PING
        embed.add_field(
            name="⚡ Ping",
            value=f"`{ping}ms`",
            inline=True
        )

        # SERVERS
        embed.add_field(
            name="🌍 Servers",
            value=f"`{server_count}`",
            inline=True
        )

        # USERS
        embed.add_field(
            name="👥 Users",
            value=f"`{user_count}`",
            inline=True
        )

        # FEATURES
        embed.add_field(
            name="🚀 Current Features",
            value=(
                "💰 Economy System\n"
                "🎰 Gambling Games\n"
                "🎒 Inventory System\n"
                "🛒 Shop System\n"
                "👑 VIP Perks\n"
                "🏆 Leveling\n"
                "🌌 User Profile\n"
                "🛡 Moderation Tools"
            ),
            inline=False
        )

        # VISION
        embed.add_field(
            name="🌟 Vision",
            value=(
                "LeonBot dibuat untuk menjadi\n"
                "Discord bot modern dengan\n"
                "UI futuristic, competitive economy,\n"
                "dan community features premium."
            ),
            inline=False
        )

        # STATUS
        embed.add_field(
            name="🔥 Status",
            value="🟢 Online & Developing",
            inline=False
        )

        # THUMBNAIL
        if self.bot.user.avatar:

            embed.set_thumbnail(
                url=self.bot.user.avatar.url
            )

        # FOOTER
        embed.set_footer(
            text="LeonBot • Dark Neon System ⚡"
        )

        await ctx.send(embed=embed)
        
    # =========================
    # INFO COMMAND
    # =========================
    @commands.hybrid_command()
    async def info(self, ctx):

        embed = default_embed(
            "🤖 LeonBot",
            "Futuristic Discord Bot 🔥"
        )

        embed.add_field(
            name="👨‍💻 Creator",
            value="Leon",
            inline=True
        )

        embed.add_field(
            name="🐍 Language",
            value="Python",
            inline=True
        )

        embed.add_field(
            name="⚡ Library",
            value="discord.py",
            inline=True
        )

        embed.add_field(
            name="🌌 Theme",
            value="Dark Blurple Neon",
            inline=False
        )

        if self.bot.user.avatar:

            embed.set_thumbnail(
                url=self.bot.user.avatar.url
            )

        await ctx.send(embed=embed)

    # =========================
    # USER INFO
    # =========================
    @commands.hybrid_command()
    async def userinfo(self, ctx, member: discord.Member = None):

        member = member or ctx.author

        roles = [
            role.mention
            for role in member.roles[1:]
        ]

        embed = default_embed(
            "👤 User Information"
        )

        embed.set_thumbnail(
            url=member.avatar.url if member.avatar else member.default_avatar.url
        )

        embed.add_field(
            name="📝 Username",
            value=member.name,
            inline=True
        )

        embed.add_field(
            name="🆔 User ID",
            value=member.id,
            inline=True
        )

        embed.add_field(
            name="🤖 Bot",
            value="Yes" if member.bot else "No",
            inline=True
        )

        embed.add_field(
            name="📅 Joined Server",
            value=member.joined_at.strftime("%d/%m/%Y"),
            inline=False
        )

        embed.add_field(
            name="🎭 Roles",
            value=" ".join(roles) if roles else "No Roles",
            inline=False
        )

        await ctx.send(embed=embed)

    # =========================
    # AVATAR COMMAND
    # =========================
    @commands.hybrid_command()
    async def avatar(self, ctx, member: discord.Member = None):

        member = member or ctx.author

        embed = default_embed(
            f"🖼️ {member.name}'s Avatar"
        )

        embed.set_image(
            url=member.avatar.url if member.avatar else member.default_avatar.url
        )

        await ctx.send(embed=embed)

    # =========================
    # SERVER COMMAND
    # =========================
    @commands.hybrid_command()
    async def server(self, ctx):

        guild = ctx.guild

        embed = default_embed(
            "🖥️ Server Information"
        )

        embed.add_field(
            name="📛 Server Name",
            value=guild.name,
            inline=True
        )

        embed.add_field(
            name="👥 Members",
            value=guild.member_count,
            inline=True
        )

        embed.add_field(
            name="👑 Owner",
            value=f"<@{guild.owner_id}>",
            inline=False
        )

        embed.add_field(
            name="🆔 Server ID",
            value=guild.id,
            inline=False
        )

        embed.add_field(
            name="📅 Created At",
            value=guild.created_at.strftime("%d/%m/%Y"),
            inline=False
        )

        if guild.icon:

            embed.set_thumbnail(
                url=guild.icon.url
            )

        await ctx.send(embed=embed)

# =========================
# LOAD COG
# =========================
async def setup(bot):

    await bot.add_cog(Utility(bot))