import discord
from discord.ext import commands
import random

from utils.theme import (
    default_embed,
    success_embed,
    error_embed
)

from utils.economy_utils import (
    load_data,
    save_data,
    create_account,
    format_money
)


class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # COINFLIP
    # =========================
    @commands.command(
        aliases=["cf", "flip"]
    )
    async def coinflip(
        self,
        ctx,
        choice=None,
        amount: int = None
    ):

        if choice is None or amount is None:

            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID USAGE",
                    "Contoh: `?coinflip heads 500`"
                )
            )

        choice = choice.lower()

        if choice not in ["heads", "tails"]:

            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID CHOICE",
                    "Pilih `heads` atau `tails`"
                )
            )

        if amount <= 0:

            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID AMOUNT",
                    "Bet harus lebih dari 0."
                )
            )

        data = load_data()

        create_account(data, ctx.author.id)

        user = data[str(ctx.author.id)]

        if user["wallet"] < amount:

            return await ctx.send(
                embed=error_embed(
                    "❌ NOT ENOUGH MONEY",
                    "Wallet lu tidak cukup."
                )
            )

        result = random.choice([
            "heads",
            "tails"
        ])

        # WIN
        if result == choice:

            reward = amount

            user["wallet"] += reward

            save_data(data)

            embed = success_embed(
                "🪙 COINFLIP WIN",
                (
                    f"🎲 Result: `{result}`\n"
                    f"💰 Won: `+{format_money(reward)}`"
                )
            )

        # LOSE
        else:

            user["wallet"] -= amount

            save_data(data)

            embed = error_embed(
                "💀 COINFLIP LOSE",
                (
                    f"🎲 Result: `{result}`\n"
                    f"💸 Lost: `-{format_money(amount)}`"
                )
            )

        await ctx.send(embed=embed)

    # =========================
    # DICE
    # =========================
    @commands.command()
    async def dice(
        self,
        ctx,
        amount: int = None
    ):

        if amount is None:

            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID USAGE",
                    "Contoh: `?dice 500`"
                )
            )

        if amount <= 0:

            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID AMOUNT",
                    "Bet harus lebih dari 0."
                )
            )

        data = load_data()

        create_account(data, ctx.author.id)

        user = data[str(ctx.author.id)]

        if user["wallet"] < amount:

            return await ctx.send(
                embed=error_embed(
                    "❌ NOT ENOUGH MONEY",
                    "Wallet lu tidak cukup."
                )
            )

        player_roll = random.randint(1, 6)
        bot_roll = random.randint(1, 6)

        # WIN
        if player_roll > bot_roll:

            reward = amount

            user["wallet"] += reward

            result_text = (
                f"🎲 Your Roll: `{player_roll}`\n"
                f"🤖 Bot Roll: `{bot_roll}`\n\n"
                f"💰 Won: `+{format_money(reward)}`"
            )

            embed = success_embed(
                "🎲 DICE WIN",
                result_text
            )

        # LOSE
        elif player_roll < bot_roll:

            user["wallet"] -= amount

            result_text = (
                f"🎲 Your Roll: `{player_roll}`\n"
                f"🤖 Bot Roll: `{bot_roll}`\n\n"
                f"💸 Lost: `-{format_money(amount)}`"
            )

            embed = error_embed(
                "💀 DICE LOSE",
                result_text
            )

        # DRAW
        else:

            result_text = (
                f"🎲 Your Roll: `{player_roll}`\n"
                f"🤖 Bot Roll: `{bot_roll}`\n\n"
                f"🤝 Draw"
            )

            embed = default_embed(
                "⚖ DICE DRAW",
                result_text
            )

        save_data(data)

        await ctx.send(embed=embed)

    # =========================
    # GUESS NUMBER
    # =========================
    @commands.command(
        aliases=["guess"]
    )
    async def guessnumber(
        self,
        ctx,
        number: int = None,
        amount: int = None
    ):

        if number is None or amount is None:

            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID USAGE",
                    "Contoh: `?guessnumber 5 500`"
                )
            )

        if number < 1 or number > 10:

            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID NUMBER",
                    "Pilih angka 1 - 10."
                )
            )

        if amount <= 0:

            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID AMOUNT",
                    "Bet harus lebih dari 0."
                )
            )

        data = load_data()

        create_account(data, ctx.author.id)

        user = data[str(ctx.author.id)]

        if user["wallet"] < amount:

            return await ctx.send(
                embed=error_embed(
                    "❌ NOT ENOUGH MONEY",
                    "Wallet lu tidak cukup."
                )
            )

        generated = random.randint(1, 10)

        # WIN
        if generated == number:

            reward = amount * 5

            user["wallet"] += reward

            embed = success_embed(
                "🎯 GUESS WIN",
                (
                    f"🔢 Number: `{generated}`\n"
                    f"💰 Won: `+{format_money(reward)}`"
                )
            )

        # LOSE
        else:

            user["wallet"] -= amount

            embed = error_embed(
                "💀 GUESS FAILED",
                (
                    f"🔢 Correct Number: `{generated}`\n"
                    f"💸 Lost: `-{format_money(amount)}`"
                )
            )

        save_data(data)

        await ctx.send(embed=embed)


# =========================
# SETUP
# =========================
async def setup(bot):
    await bot.add_cog(Games(bot))