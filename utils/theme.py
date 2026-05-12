import discord
from utils.colors import *

# =========================
# DEFAULT EMBED
# =========================
def default_embed(title, description=None):

    embed = discord.Embed(
        title=f"💠 {title}",
        description=description,
        color=INFO
    )

    embed.set_footer(
        text="LeonBot • Dark Neon System ⚡"
    )

    embed.timestamp = discord.utils.utcnow()

    return embed

# =========================
# SUCCESS EMBED
# =========================
def success_embed(title, description=None):

    embed = discord.Embed(
        title=f"✅ {title}",
        description=description,
        color=SUCCESS
    )

    embed.set_footer(
        text="LeonBot Success System 🚀"
    )

    embed.timestamp = discord.utils.utcnow()

    return embed

# =========================
# ERROR EMBED
# =========================
def error_embed(title, description=None):

    embed = discord.Embed(
        title=f"❌ {title}",
        description=description,
        color=ERROR
    )

    embed.set_footer(
        text="LeonBot Error System ⚠️"
    )

    embed.timestamp = discord.utils.utcnow()

    return embed