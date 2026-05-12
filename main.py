import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True



bot = commands.Bot(
    command_prefix="?",
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
# COMMAND ERROR
# =========================
# =========================
# COMMAND ERROR
# =========================
@bot.event
async def on_command_error(ctx, error):

    # COMMAND TIDAK DITEMUKAN
    if isinstance(error, commands.CommandNotFound):

        embed = discord.Embed(
            title="❌ COMMAND NOT FOUND",
            description=(
                "⚠ Command tidak ditemukan.\n\n"
                "📚 Gunakan `?help`\n"
                "untuk melihat semua command."
            ),
            color=discord.Color.red()
        )

        embed.set_footer(
            text="LeonBot • Futuristic Discord Bot"
        )

        await ctx.send(embed=embed)

    # TIDAK PUNYA PERMISSION
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

    # COMMAND COOLDOWN
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

    # ERROR LAIN
    else:

        print("=" * 50)
        print("ERROR:")
        print(error)
        print("=" * 50)

# =========================
# READY
# =========================
@bot.event
async def on_ready():

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

try:
    asyncio.run(main())

except KeyboardInterrupt:
    print("\n🛑 Bot stopped.")