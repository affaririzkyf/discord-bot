import discord
from discord.ext import commands

class Welcome(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # MEMBER JOIN
    # =========================
    @commands.Cog.listener()
    async def on_member_join(self, member):

        channel = discord.utils.get(
            member.guild.text_channels,
            name="sweet-chat"
        )

        role = discord.utils.get(
            member.guild.roles,
            name="member"
        )

        if role:
            await member.add_roles(role)

        if channel:

            embed = discord.Embed(
                title="🎉 Welcome!",
                description=f"Welcome {member.mention}",
                color=discord.Color.blurple()
            )

            await channel.send(embed=embed)

async def setup(bot):

    await bot.add_cog(Welcome(bot))