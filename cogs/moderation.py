import discord
from discord.ext import commands
import asyncio

from utils.theme import success_embed, error_embed

OWNER_ID = 123456789012345678  # ganti dengan ID Discord kamu

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # CHECK OWNER / PERMISSION
    # =========================
    async def cog_check(self, ctx):

        # Owner bypass
        if ctx.author.id == OWNER_ID:
            return True

        return True

    # =========================
    # CLEAR COMMAND
    # =========================
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):

        await ctx.channel.purge(limit=amount + 1)

        embed = success_embed(
            "🧹 Messages Cleared",
            f"Deleted **{amount}** messages."
        )

        msg = await ctx.send(embed=embed)

        await asyncio.sleep(3)

        await msg.delete()

    # =========================
    # ADD ROLE
    # =========================
    @commands.command()
    async def addrole(
        self,
        ctx,
        member: discord.Member,
        *,
        role: discord.Role
    ):

        # kalau bukan owner → cek permission
        if ctx.author.id != OWNER_ID:
            if not ctx.author.guild_permissions.manage_roles:

                embed = error_embed(
                    "❌ You need `Manage Roles` permission."
                )

                await ctx.send(embed=embed)
                return

        # role bot harus lebih tinggi
        if role >= ctx.guild.me.top_role:

            embed = error_embed(
                "❌ Role is higher than bot role."
            )

            await ctx.send(embed=embed)
            return

        # sudah punya role
        if role in member.roles:

            embed = error_embed(
                f"❌ {member.mention} already has `{role.name}`"
            )

            await ctx.send(embed=embed)
            return

        try:

            await member.add_roles(role)

            embed = success_embed(
                "✅ Role Added",
                f"Added `{role.name}` to {member.mention}"
            )

            await ctx.send(embed=embed)

        except discord.Forbidden:

            embed = error_embed(
                "❌ Bot missing permissions."
            )

            await ctx.send(embed=embed)

        except Exception as e:

            embed = error_embed(
                f"❌ Error:\n```{e}```"
            )

            await ctx.send(embed=embed)


async def setup(bot):

    await bot.add_cog(Moderation(bot))