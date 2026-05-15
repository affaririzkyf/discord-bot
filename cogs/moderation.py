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
            "🧹 MESSAGES CLEARED",
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
        *roles: discord.Role
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

        # cek apakah role dikirim
        if not roles:

            embed = error_embed(
                "⚠ NO ROLE",
                "Masukkan minimal 1 role."
            )

            await ctx.send(embed=embed)
            return

        added_roles = []
        failed_roles = []
        already_have = []

        for role in roles:

            # role hierarchy
            if role >= ctx.guild.me.top_role:
                failed_roles.append(f"{role.name} (Role terlalu tinggi)")
                continue

            # user sudah punya role
            if role in member.roles:
                already_have.append(role.name)
                continue

            try:

                await member.add_roles(role)
                added_roles.append(role.name)

            except discord.Forbidden:
                failed_roles.append(f"{role.name} (Forbidden)")

            except Exception as e:
                failed_roles.append(f"{role.name} ({e})")

        embed = success_embed(
            "✅ ROLE UPDATED",
            f"Role berhasil diproses untuk {member.mention}"
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        if added_roles:
            embed.add_field(
                name="✅ Added Roles",
                value="\n".join([f"`{r}`" for r in added_roles]),
                inline=False
            )

        if already_have:
            embed.add_field(
                name="⚠ Already Have",
                value="\n".join([f"`{r}`" for r in already_have]),
                inline=False
            )

        if failed_roles:
            embed.add_field(
                name="❌ Failed",
                value="\n".join([f"`{r}`" for r in failed_roles]),
                inline=False
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
                "⚠ COMMAND INCOMPLETE",
                "**Contoh Penggunaan:**\n"
                "`?clear 10`\n\n"
                "🧹 Menghapus 10 pesan."
            )

            await ctx.send(embed=embed)

    @addrole.error
    async def addrole_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):

            embed = error_embed(
                "⚠ COMMAND INCOMPLETE",
                "**Contoh Penggunaan:**\n"
                "`?addrole @User VIP`\n\n"
                "📌 Menambahkan role `VIP` ke user."
            )

            await ctx.send(embed=embed)

    @removerole.error
    async def removerole_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):

            embed = error_embed(
                "⚠ COMMAND INCOMPLETE",
                "**Contoh Penggunaan:**\n"
                "`?removerole @User VIP`\n\n"
                "📌 Menghapus role `VIP` dari user."
            )

            await ctx.send(embed=embed)


async def setup(bot):

    await bot.add_cog(Moderation(bot))