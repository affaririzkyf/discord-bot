import discord
from discord.ext import commands, tasks
from discord import app_commands

class AutoMessage(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        # DATA PER SERVER
        self.guild_data = {}

        self.auto_message.start()

    # =========================
    # AUTO MESSAGE LOOP
    # =========================
    @tasks.loop(minutes=1)
    async def auto_message(self):

        for guild_id, data in self.guild_data.items():

            channel_id = data["channel_id"]
            message = data["message"]

            channel = self.bot.get_channel(channel_id)

            if channel is None:
                continue

            embed = discord.Embed(
                title="📢 LEONBOT AUTO MESSAGE",
                description=message,
                color=discord.Color.blue()
            )

            embed.set_footer(
                text="LeonBot • Auto Message"
            )

            try:
                await channel.send(embed=embed)

            except:
                pass

    @auto_message.before_loop
    async def before_auto_message(self):

        await self.bot.wait_until_ready()

    # =========================
    # SET AUTO MESSAGE
    # =========================
    @app_commands.command(
        name="setautomessage",
        description="Set auto message"
    )
    @app_commands.describe(
        channel="Pilih channel",
        message="Isi pesan"
    )
    async def setautomessage(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        message: str
    ):

        guild_id = interaction.guild.id

        self.guild_data[guild_id] = {
            "channel_id": channel.id,
            "message": message
        }

        embed = discord.Embed(
            title="✅ AUTO MESSAGE SET",
            description=(
                f"📢 Channel: {channel.mention}\n\n"
                f"💬 Message:\n{message}\n\n"
                f"⏱ Interval: `1 menit`"
            ),
            color=discord.Color.green()
        )

        await interaction.response.send_message(
            embed=embed
        )

    # =========================
    # STOP AUTO MESSAGE
    # =========================
    @app_commands.command(
        name="stopautomessage",
        description="Stop auto message"
    )
    async def stopautomessage(
        self,
        interaction: discord.Interaction
    ):

        guild_id = interaction.guild.id

        if guild_id in self.guild_data:

            del self.guild_data[guild_id]

        embed = discord.Embed(
            title="🛑 AUTO MESSAGE STOPPED",
            description="Auto message dihentikan.",
            color=discord.Color.red()
        )

        await interaction.response.send_message(
            embed=embed
        )

# =========================
# SETUP
# =========================
async def setup(bot):

    await bot.add_cog(
        AutoMessage(bot)
    )