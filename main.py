import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

# =========================
# LOAD ENV
# =========================
load_dotenv()

TOKEN = os.getenv("TOKEN")

# =========================
# INTENTS
# =========================
intents = discord.Intents.all()

# =========================
# BOT
# =========================
bot = commands.Bot(
    command_prefix="$",
    intents=intents,
    help_command=None
)

# =========================
# LOAD COGS
# =========================
async def load_cogs():

    for filename in os.listdir("./cogs"):

        if filename.endswith(".py") and filename != "__init__.py":

            try:

                await bot.load_extension(
                    f"cogs.{filename[:-3]}"
                )

                print(f"✅ Loaded: {filename}")

            except Exception as e:

                print(f"❌ Failed: {filename}")
                print(e)

# =========================
# PREFIX COMMAND ERROR
# =========================
@bot.event
async def on_command_error(ctx, error):

    # BIAR TIDAK DOUBLE ERROR
    if hasattr(ctx.command, "on_error"):
        return

    # COMMAND NOT FOUND
    if isinstance(error, commands.CommandNotFound):

        embed = discord.Embed(
            title="❌ COMMAND NOT FOUND",
            description=(
                "⚠ Command tidak ditemukan.\n\n"
                "📚 Gunakan `$help`\n"
                "untuk melihat semua command."
            ),
            color=discord.Color.red()
        )

        embed.set_footer(
            text="LeonBot • Futuristic Discord Bot"
        )

        await ctx.send(embed=embed)

    # MISSING ARGUMENT
    elif isinstance(error, commands.MissingRequiredArgument):

        embed = discord.Embed(
            title="⚠ MISSING ARGUMENT",
            description=(
                "Argument command belum lengkap."
            ),
            color=discord.Color.orange()
        )

        await ctx.send(embed=embed)

    # NO PERMISSION
    elif isinstance(error, commands.MissingPermissions):

        embed = discord.Embed(
            title="🚫 NO PERMISSION",
            description=(
                "Lu tidak punya permission\n"
                "untuk menggunakan command ini."
            ),
            color=discord.Color.red()
        )

        await ctx.send(embed=embed)

    # COOLDOWN
    elif isinstance(error, commands.CommandOnCooldown):

        embed = discord.Embed(
            title="⏳ COMMAND COOLDOWN",
            description=(
                f"Coba lagi dalam\n"
                f"`{round(error.retry_after, 1)} detik`"
            ),
            color=discord.Color.orange()
        )

        await ctx.send(embed=embed)

    # USER NOT FOUND
    elif isinstance(error, commands.MemberNotFound):

        await ctx.send("❌ Member tidak ditemukan.")

    # ERROR LAIN
    else:

        print("=" * 50)
        print("PREFIX COMMAND ERROR:")
        print(error)
        print("=" * 50)

# =========================
# SLASH COMMAND ERROR
# =========================
@bot.tree.error
async def on_app_command_error(interaction, error):

    # COMMAND ERROR
    if isinstance(error, discord.app_commands.CommandInvokeError):

        message = "❌ Terjadi error saat menjalankan command."

    # MISSING PERMISSION
    elif isinstance(error, discord.app_commands.MissingPermissions):

        message = "🚫 Kamu tidak punya permission."

    # COMMAND NOT FOUND
    elif isinstance(error, discord.app_commands.CommandNotFound):

        message = "❌ Slash command tidak ditemukan."

    else:

        print("=" * 50)
        print("SLASH COMMAND ERROR:")
        print(error)
        print("=" * 50)

        message = "❌ Terjadi error."

    try:

        if interaction.response.is_done():

            await interaction.followup.send(
                message,
                ephemeral=True
            )

        else:

            await interaction.response.send_message(
                message,
                ephemeral=True
            )

    except Exception as e:

        print(e)

# =========================
# READY
# =========================
@bot.event
async def on_ready():

    try:

        synced = await bot.tree.sync()

        print(f"🌍 Synced {len(synced)} slash commands")

    except Exception as e:

        print("Slash Sync Error:")
        print(e)

    await bot.change_presence(

        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="LeonBot | $help"
        )
    )

    print("=" * 40)
    print(f"✅ Logged in as {bot.user}")
    print("=" * 40)

# =========================
# MAIN
# =========================
async def main():

    async with bot:

        await load_cogs()

        await bot.start(TOKEN)

# =========================
# RUN BOT
# =========================
try:

    asyncio.run(main())

except KeyboardInterrupt:

    print("\n🛑 Bot stopped.")