import discord
from discord.ext import commands, tasks
from discord import app_commands

class AutoMessage(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # DEFAULT
        self.channel_id = None
        self.message = (
            "🔥 Jangan lupa gunakan `/help`\n"
            "untuk melihat semua fitur LeonBot."
        )

        self.auto_message.start()

    def cog_unload(self):

        self.auto_message.cancel()

    # =========================
    # AUTO MESSAGE LOOP
    # =========================
    @tasks.loop(minutes=30)
    async def auto_message(self):

        if self.channel_id is None:
            return

        channel = self.bot.get_channel(self.channel_id)

        if channel is None:
            return

        embed = discord.Embed(
            title="📢 LEONBOT AUTO MESSAGE",
            description=self.message,
            color=discord.Color.blue()
        )

        embed.set_footer(
            text="LeonBot • Auto Message"
        )

        await channel.send(embed=embed)

    @auto_message.before_loop
    async def before_auto_message(self):

        await self.bot.wait_until_ready()

    # =========================
    # SET AUTO CHANNEL
    # =========================
    @app_commands.command(
        name="setautomessage",
        description="Set auto message channel"
    )
    @app_commands.describe(
        channel="Pilih channel auto message",
        minutes="Interval menit",
        message="Isi pesan auto message"
    )
    async def setautomessage(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        minutes: int,
        message: str
    ):

        # STOP LOOP LAMA
        self.auto_message.cancel()

        # SAVE DATA
        self.channel_id = channel.id
        self.message = message

        # START LOOP BARU
        self.auto_message.change_interval(
            minutes=minutes
        )

        self.auto_message.start()

        embed = discord.Embed(
            title="✅ AUTO MESSAGE SET",
            description=(
                f"📢 Channel: {channel.mention}\n"
                f"⏱ Interval: `{minutes} menit`\n\n"
                f"💬 Message:\n{message}"
            ),
            color=discord.Color.green()
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