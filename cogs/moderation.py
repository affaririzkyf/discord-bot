import discord
from discord.ext import commands
import asyncio

from utils.theme import success_embed, error_embed

OWNER_ID = 1464209826010763463 


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================================
    # CLEAR COMMAND
    # =========================================
    @commands.command()
    async def clear(self, ctx, amount: int):

        # OWNER BYPASS
        if ctx.author.id != OWNER_ID:

            # cek permission user
            if not ctx.author.guild_permissions.manage_messages:

                embed = error_embed(
                    "🚫 NO PERMISSION",
                    "Lu tidak punya permission\nuntuk menggunakan command ini."
                )

                await ctx.send(embed=embed)
                return

        # cek permission bot
        if not ctx.guild.me.guild_permissions.manage_messages:

            embed = error_embed(
                "❌ BOT NO PERMISSION",
                "Bot tidak punya permission `Manage Messages`."
            )

            await ctx.send(embed=embed)
            return

        await ctx.channel.purge(limit=amount + 1)

        embed = success_embed(
            "🧹 Messages Cleared",
            f"Deleted **{amount}** messages."
        )

        msg = await ctx.send(embed=embed)

        await asyncio.sleep(3)

        await msg.delete()

    # =========================================
    # ADD ROLE
    # =========================================
    @commands.command()
    async def addrole(
        self,
        ctx,
        member: discord.Member,
        *,
        role: discord.Role
    ):

        # OWNER BYPASS
        if ctx.author.id != OWNER_ID:

            # cek permission user
            if not ctx.author.guild_permissions.manage_roles:

                embed = error_embed(
                    "🚫 NO PERMISSION",
                    "Lu tidak punya permission\nuntuk menggunakan command ini."
                )

                await ctx.send(embed=embed)
                return

        # cek permission bot
        if not ctx.guild.me.guild_permissions.manage_roles:

            embed = error_embed(
                "❌ BOT NO PERMISSION",
                "Bot tidak punya permission `Manage Roles`."
            )

            await ctx.send(embed=embed)
            return

        # role bot harus lebih tinggi
        if role >= ctx.guild.me.top_role:

            embed = error_embed(
                "❌ ROLE TOO HIGH",
                "Role tersebut lebih tinggi dari role bot."
            )

            await ctx.send(embed=embed)
            return

        # user sudah punya role
        if role in member.roles:

            embed = error_embed(
                "⚠ ROLE EXISTS",
                f"{member.mention} sudah memiliki role `{role.name}`"
            )

            await ctx.send(embed=embed)
            return

        try:

            await member.add_roles(role)

            embed = success_embed(
                "✅ ROLE ADDED",
                f"Berhasil menambahkan role `{role.name}` ke {member.mention}"
            )

            embed.set_thumbnail(url=member.display_avatar.url)

            await ctx.send(embed=embed)

        except discord.Forbidden:

            embed = error_embed(
                "❌ FORBIDDEN",
                "Bot tidak memiliki izin untuk mengatur role."
            )

            await ctx.send(embed=embed)

        except Exception as e:

            embed = error_embed(
                "❌ ERROR",
                f"```{e}```"
            )

            await ctx.send(embed=embed)

    # =========================================
    # REMOVE ROLE
    # =========================================
    @commands.command()
    async def removerole(
        self,
        ctx,
        member: discord.Member,
        *,
        role: discord.Role
    ):

        # OWNER BYPASS
        if ctx.author.id != OWNER_ID:

            if not ctx.author.guild_permissions.manage_roles:

                embed = error_embed(
                    "🚫 NO PERMISSION",
                    "Lu tidak punya permission\nuntuk menggunakan command ini."
                )

                await ctx.send(embed=embed)
                return

        # bot permission
        if not ctx.guild.me.guild_permissions.manage_roles:

            embed = error_embed(
                "❌ BOT NO PERMISSION",
                "Bot tidak punya permission `Manage Roles`."
            )

            await ctx.send(embed=embed)
            return

        # role hierarchy
        if role >= ctx.guild.me.top_role:

            embed = error_embed(
                "❌ ROLE TOO HIGH",
                "Role tersebut lebih tinggi dari role bot."
            )

            await ctx.send(embed=embed)
            return

        # user tidak punya role
        if role not in member.roles:

            embed = error_embed(
                "⚠ ROLE NOT FOUND",
                f"{member.mention} tidak memiliki role `{role.name}`"
            )

            await ctx.send(embed=embed)
            return

        try:

            await member.remove_roles(role)

            embed = success_embed(
                "✅ ROLE REMOVED",
                f"Berhasil menghapus role `{role.name}` dari {member.mention}"
            )

            embed.set_thumbnail(url=member.display_avatar.url)

            await ctx.send(embed=embed)

        except Exception as e:

            embed = error_embed(
                "❌ ERROR",
                f"```{e}```"
            )

            await ctx.send(embed=embed)

    # =========================================
    # ERROR HANDLER
    # =========================================
    @clear.error
    async def clear_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):

            embed = error_embed(
                "⚠ MISSING ARGUMENT",
                "Usage:\n`?clear <amount>`"
            )

            await ctx.send(embed=embed)

    @addrole.error
    async def addrole_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):

            embed = error_embed(
                "⚠ MISSING ARGUMENT",
                "Usage:\n`?addrole @user role`"
            )

            await ctx.send(embed=embed)

    @removerole.error
    async def removerole_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):

            embed = error_embed(
                "⚠ MISSING ARGUMENT",
                "Usage:\n`?removerole @user role`"
            )

            await ctx.send(embed=embed)


async def setup(bot):

    await bot.add_cog(Moderation(bot))