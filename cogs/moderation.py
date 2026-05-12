import discord
from discord.ext import commands
import asyncio

from utils.theme import success_embed

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # CLEAR COMMAND
    # =========================
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):

        await ctx.channel.purge(limit=amount + 1)

        embed = success_embed(
            "Messages Cleared",
            f"Deleted **{amount}** messages."
        )

        msg = await ctx.send(embed=embed)

        await asyncio.sleep(3)

        await msg.delete()

   
async def setup(bot):

    await bot.add_cog(Moderation(bot))