import discord
from discord.ext import commands
import os
from datetime import timedelta
import json

from utils.theme import (
    success_embed,
    error_embed,
    default_embed
)

from utils.economy_utils import (
    load_data,
    save_data,
    create_account,
    format_money
)

# =========================
# OWNER ID
# =========================
OWNER_ID = 1464209826010763463


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

   # =========================
    # OWNER CHECK
    # =========================
    def is_owner(self, ctx):

        # OWNER BOT
        if ctx.author.id == OWNER_ID:
            return True

        # OWNER SERVER
        if ctx.author == ctx.guild.owner:
            return True

        return False

    # =========================
    # SHUTDOWN
    # =========================
    @commands.command()
    async def shutdown(self, ctx):

        if not self.is_owner(ctx):
            return await ctx.send(
                embed=error_embed(
                    "❌ ACCESS DENIED",
                    "Command khusus owner."
                )
            )

        embed = success_embed(
            "🛑 SHUTDOWN",
            "LeonBot dimatikan."
        )

        await ctx.send(embed=embed)

        await self.bot.close()
        

    # =========================================
    # RESET ALL LEVEL
    # =========================================
    @commands.command()
    async def resetlevels(self, ctx):

        OWNER_ID = 1464209826010763463  # GANTI ID KAMU

        # OWNER CHECK
        if ctx.author.id != OWNER_ID:

            embed = error_embed(
                "🚫 NO PERMISSION",
                "Command ini hanya untuk owner bot."
            )

            return await ctx.send(embed=embed)

        # RESET DATA
        with open("data/levels.json", "w") as f:

            json.dump({}, f, indent=4)

        embed = success_embed(
            "🗑 LEVEL RESET",
            "Semua data level berhasil direset."
        )

        await ctx.send(embed=embed)

    # =========================
    # LEAVE SERVER
    # =========================
    @commands.command()
    async def leave(self, ctx):

        if not self.is_owner(ctx):
            return await ctx.send(
                embed=error_embed(
                    "❌ ACCESS DENIED",
                    "Command khusus owner."
                )
            )

        embed = success_embed(
            "👋 LEAVING SERVER",
            f"Keluar dari **{ctx.guild.name}**"
        )

        await ctx.send(embed=embed)

        await ctx.guild.leave()

    # =========================
    # RELOAD COG
    # =========================
    @commands.command()
    async def reload(self, ctx, cog=None):

        if not self.is_owner(ctx):
            return await ctx.send(
                embed=error_embed(
                    "❌ ACCESS DENIED",
                    "Command khusus owner."
                )
            )

        if cog is None:
            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID USAGE",
                    "Contoh: `$reload economy`"
                )
            )

        try:

            await self.bot.reload_extension(f"cogs.{cog}")

            embed = success_embed(
                "🔄 COG RELOADED",
                f"Berhasil reload `cogs.{cog}`"
            )

            await ctx.send(embed=embed)

        except Exception as e:

            await ctx.send(
                embed=error_embed(
                    "❌ RELOAD FAILED",
                    str(e)
                )
            )

    # =========================
    # LOAD COG
    # =========================
    @commands.command()
    async def load(self, ctx, cog=None):

        if not self.is_owner(ctx):
            return await ctx.send(
                embed=error_embed(
                    "❌ ACCESS DENIED",
                    "Command khusus owner."
                )
            )

        if cog is None:
            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID USAGE",
                    "Contoh: `$load music`"
                )
            )

        try:

            await self.bot.load_extension(f"cogs.{cog}")

            embed = success_embed(
                "📦 COG LOADED",
                f"Berhasil load `cogs.{cog}`"
            )

            await ctx.send(embed=embed)

        except Exception as e:

            await ctx.send(
                embed=error_embed(
                    "❌ LOAD FAILED",
                    str(e)
                )
            )

    # =========================
    # UNLOAD COG
    # =========================
    @commands.command()
    async def unload(self, ctx, cog=None):

        if not self.is_owner(ctx):
            return await ctx.send(
                embed=error_embed(
                    "❌ ACCESS DENIED",
                    "Command khusus owner."
                )
            )

        if cog is None:
            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID USAGE",
                    "Contoh: `$unload fun`"
                )
            )

        try:

            await self.bot.unload_extension(f"cogs.{cog}")

            embed = success_embed(
                "❌ COG UNLOADED",
                f"Berhasil unload `cogs.{cog}`"
            )

            await ctx.send(embed=embed)

        except Exception as e:

            await ctx.send(
                embed=error_embed(
                    "❌ UNLOAD FAILED",
                    str(e)
                )
            )

    # =========================
    # ADD MONEY
    # =========================
    @commands.command()
    async def addmoney(
        self,
        ctx,
        member: discord.Member = None,
        amount: int = None
    ):

        if not self.is_owner(ctx):
            return await ctx.send(
                embed=error_embed(
                    "❌ ACCESS DENIED",
                    "Command khusus owner."
                )
            )

        if member is None or amount is None:
            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID USAGE",
                    "Contoh: `$addmoney @user 5000`"
                )
            )

        data = load_data()

        create_account(data, member.id)

        user = data[str(member.id)]

        user["wallet"] += amount

        save_data(data)

        embed = success_embed(
            "💰 MONEY ADDED",
            (
                f"👤 User: {member.mention}\n"
                f"💵 Added: `{format_money(amount)}`"
            )
        )

        await ctx.send(embed=embed)

    # =========================
    # REMOVE MONEY
    # =========================
    @commands.command()
    async def removemoney(
        self,
        ctx,
        member: discord.Member = None,
        amount: int = None
    ):

        if not self.is_owner(ctx):
            return await ctx.send(
                embed=error_embed(
                    "❌ ACCESS DENIED",
                    "Command khusus owner."
                )
            )

        if member is None or amount is None:
            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID USAGE",
                    "Contoh: `$removemoney @user 5000`"
                )
            )

        data = load_data()

        create_account(data, member.id)

        user = data[str(member.id)]

        if user["wallet"] < amount:
            return await ctx.send(
                embed=error_embed(
                    "❌ NOT ENOUGH MONEY",
                    "Wallet user tidak cukup."
                )
            )

        user["wallet"] -= amount

        save_data(data)

        embed = success_embed(
            "💸 MONEY REMOVED",
            (
                f"👤 User: {member.mention}\n"
                f"💵 Removed: `{format_money(amount)}`"
            )
        )

        await ctx.send(embed=embed)

    # =========================
    # SET MONEY
    # =========================
    @commands.command()
    async def setmoney(
        self,
        ctx,
        member: discord.Member = None,
        amount: int = None
    ):

        if not self.is_owner(ctx):
            return await ctx.send(
                embed=error_embed(
                    "❌ ACCESS DENIED",
                    "Command khusus owner."
                )
            )

        if member is None or amount is None:
            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID USAGE",
                    "Contoh: `$setmoney @user 5000`"
                )
            )

        data = load_data()

        create_account(data, member.id)

        data[str(member.id)]["wallet"] = amount

        save_data(data)

        embed = success_embed(
            "⚡ MONEY SET",
            (
                f"👤 User: {member.mention}\n"
                f"💰 Wallet: `{format_money(amount)}`"
            )
        )

        await ctx.send(embed=embed)

    # =========================
    # RESET ECONOMY
    # =========================
    @commands.command()
    async def reseteconomy(self, ctx):

        if not self.is_owner(ctx):
            return await ctx.send(
                embed=error_embed(
                    "❌ ACCESS DENIED",
                    "Command khusus owner."
                )
            )

        save_data({})

        embed = success_embed(
            "🗑 ECONOMY RESET",
            "Semua data economy berhasil direset."
        )

        await ctx.send(embed=embed)

    # =========================
    # GIVE ALL
    # =========================
    @commands.command()
    async def giveall(self, ctx, amount: int = None):

        if not self.is_owner(ctx):
            return await ctx.send(
                embed=error_embed(
                    "❌ ACCESS DENIED",
                    "Command khusus owner."
                )
            )

        if amount is None:
            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID USAGE",
                    "Contoh: `$giveall 500`"
                )
            )

        data = load_data()

        for member in ctx.guild.members:

            if member.bot:
                continue

            create_account(data, member.id)

            data[str(member.id)]["wallet"] += amount

        save_data(data)

        embed = success_embed(
            "🎉 GIVEALL SUCCESS",
            (
                f"Semua member mendapat\n"
                f"💰 `{format_money(amount)}`"
            )
        )

        await ctx.send(embed=embed)

    # =========================
    # TIMEOUT
    # =========================
    @commands.command()
    async def timeout(
        self,
        ctx,
        user_id: int = None,
        duration=None,
        *,
        reason="No reason"
    ):

        if not self.is_owner(ctx):

            return await ctx.send(
                embed=error_embed(
                    "❌ ACCESS DENIED",
                    "Command khusus owner."
                )
            )

        # VALIDATION
        if user_id is None or duration is None:

            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID USAGE",
                    "Contoh:\n`$timeout 123456789 5m spam`"
                )
            )

        # GET MEMBER
        member = ctx.guild.get_member(user_id)

        if member is None:

            return await ctx.send(
                embed=error_embed(
                    "❌ USER NOT FOUND",
                    "User tidak ditemukan di server."
                )
            )

        # SELF
        if member == ctx.author:

            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID ACTION",
                    "Lu tidak bisa timeout diri sendiri."
                )
            )

        # BOT
        if member.bot:

            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID USER",
                    "Tidak bisa timeout bot."
                )
            )

        # ALREADY TIMEOUT
        if member.timed_out_until is not None:

            return await ctx.send(
                embed=error_embed(
                    "❌ ALREADY TIMEOUT",
                    "User sudah sedang timeout."
                )
            )

        # PARSE TIME
        try:

            time_unit = duration[-1].lower()
            time_amount = int(duration[:-1])

            if time_amount <= 0:

                return await ctx.send(
                    embed=error_embed(
                        "❌ INVALID TIME",
                        "Durasi harus lebih dari 0."
                    )
                )

            if time_unit == "m":

                delta = timedelta(minutes=time_amount)

            elif time_unit == "h":

                delta = timedelta(hours=time_amount)

            elif time_unit == "d":

                delta = timedelta(days=time_amount)

            else:

                return await ctx.send(
                    embed=error_embed(
                        "❌ INVALID FORMAT",
                        "Gunakan:\n`m` = menit\n`h` = jam\n`d` = hari"
                    )
                )

        except:

            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID TIME",
                    "Contoh:\n`5m`\n`2h`\n`1d`"
                )
            )

        # TIMEOUT USER
        try:

            await member.timeout(
                delta,
                reason=reason
            )

            embed = success_embed(
                "🔇 USER TIMEOUT",
                (
                    f"👤 User: {member.mention}\n"
                    f"🆔 ID: `{member.id}`\n"
                    f"⏳ Duration: `{duration}`\n"
                    f"📝 Reason: `{reason}`"
                )
            )

            await ctx.send(embed=embed)

        except Exception as e:

            await ctx.send(
                embed=error_embed(
                    "❌ TIMEOUT FAILED",
                    str(e)
                )
            )


    # =========================
    # UNTIMEOUT
    # =========================
    @commands.command()
    async def untimeout(
        self,
        ctx,
        user_id: int = None
    ):

        if not self.is_owner(ctx):

            return await ctx.send(
                embed=error_embed(
                    "❌ ACCESS DENIED",
                    "Command khusus owner."
                )
            )

        # VALIDATION
        if user_id is None:

            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID USAGE",
                    "Contoh:\n`$untimeout 123456789`"
                )
            )

        # GET MEMBER
        member = ctx.guild.get_member(user_id)

        if member is None:

            return await ctx.send(
                embed=error_embed(
                    "❌ USER NOT FOUND",
                    "User tidak ditemukan di server."
                )
            )

        # CHECK TIMEOUT
        if member.timed_out_until is None:

            return await ctx.send(
                embed=error_embed(
                    "❌ NOT TIMEOUTED",
                    "User tidak sedang timeout."
                )
            )

        # REMOVE TIMEOUT
        try:

            await member.timeout(None)

            embed = success_embed(
                "🔊 TIMEOUT REMOVED",
                (
                    f"👤 User: {member.mention}\n"
                    f"🆔 ID: `{member.id}`\n"
                    f"✅ Timeout berhasil dihapus."
                )
            )

            await ctx.send(embed=embed)

        except Exception as e:

            await ctx.send(
                embed=error_embed(
                    "❌ UNTIMEOUT FAILED",
                    str(e)
                )
            )

    # =========================
    # KICK
    # =========================
    @commands.command()
    async def kick(
        self,
        ctx,
        member: discord.Member = None,
        *,
        reason="No reason"
    ):

        if not self.is_owner(ctx):
            return await ctx.send(
                embed=error_embed(
                    "❌ ACCESS DENIED",
                    "Command khusus owner."
                )
            )

        await member.kick(reason=reason)

        embed = success_embed(
            "👢 USER KICKED",
            (
                f"👤 User: {member.mention}\n"
                f"📝 Reason: `{reason}`"
            )
        )

        await ctx.send(embed=embed)

    # =========================
    # BAN
    # =========================
    @commands.command()
    async def ban(
        self,
        ctx,
        member: discord.Member = None,
        *,
        reason="No reason"
    ):

        if not self.is_owner(ctx):
            return await ctx.send(
                embed=error_embed(
                    "❌ ACCESS DENIED",
                    "Command khusus owner."
                )
            )

        await member.ban(reason=reason)

        embed = success_embed(
            "🔨 USER BANNED",
            (
                f"👤 User: {member.mention}\n"
                f"📝 Reason: `{reason}`"
            )
        )

        await ctx.send(embed=embed)

    # =========================
    # UNBAN
    # =========================
    @commands.command()
    async def unban(self, ctx, user_id: int):

        if not self.is_owner(ctx):
            return await ctx.send(
                embed=error_embed(
                    "❌ ACCESS DENIED",
                    "Command khusus owner."
                )
            )

        user = await self.bot.fetch_user(user_id)

        await ctx.guild.unban(user)

        embed = success_embed(
            "🔓 USER UNBANNED",
            f"User ID `{user_id}` berhasil di-unban."
        )

        await ctx.send(embed=embed)


# =========================
# SETUP
# =========================
async def setup(bot):
    await bot.add_cog(Owner(bot))