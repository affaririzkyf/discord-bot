import discord
from discord.ext import commands
import random
import time

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


class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # BALANCE
    # =========================
    @commands.command(aliases=["bal"])
    async def balance(self, ctx, member: discord.Member = None):

        if member is None:
            member = ctx.author

        data = load_data()
        create_account(data, member.id)
        save_data(data)

        user = data[str(member.id)]

        wallet = format_money(user["wallet"])
        bank = format_money(user["bank"])

        embed = default_embed(
            "💰 LEON BANK",
            (
                f"━━━━━━━━━━━━━━\n"
                f"👤 User: {member.mention}\n"
                f"💵 Wallet: `{wallet}`\n"
                f"🏦 Bank: `{bank}`"
            )
        )

        await ctx.send(embed=embed)
        
        
    # =========================
    # PAY MONEY
    # =========================
    @commands.command(aliases=["give"])
    async def pay(
        self,
        ctx,
        member: discord.Member = None,
        amount: int = None
    ):

        if member is None or amount is None:
            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID USAGE",
                    "Contoh: `$pay @user 500`"
                )
            )

        if member.bot:
            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID USER",
                    "Tidak bisa transfer ke bot."
                )
            )

        if member.id == ctx.author.id:
            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID ACTION",
                    "Lu tidak bisa transfer ke diri sendiri."
                )
            )

        if amount <= 0:
            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID AMOUNT",
                    "Jumlah harus lebih dari 0."
                )
            )

        data = load_data()

        create_account(data, ctx.author.id)
        create_account(data, member.id)

        sender = data[str(ctx.author.id)]
        receiver = data[str(member.id)]

        if sender["wallet"] < amount:
            return await ctx.send(
                embed=error_embed(
                    "❌ NOT ENOUGH MONEY",
                    "Uang wallet lu tidak cukup."
                )
            )

        # TRANSFER
        sender["wallet"] -= amount
        receiver["wallet"] += amount

        save_data(data)

        embed = success_embed(
            "💸 TRANSFER SUCCESS",
            (
                f"👤 Sender: {ctx.author.mention}\n"
                f"📥 Receiver: {member.mention}\n"
                f"💰 Amount: `{format_money(amount)}`"
            )
        )

        await ctx.send(embed=embed)
        
    
        
    # =========================
    # SLOTS
    # =========================
    @commands.command()
    async def slot(self, ctx, amount: int = None):

        if amount is None:
            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID USAGE",
                    "Contoh: `$slots 500`"
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
                    "Uang wallet lu tidak cukup."
                )
            )

        symbols = [
            "🍒",
            "🍋",
            "🍉",
            "💎",
            "⭐"
        ]

        slot1 = random.choice(symbols)
        slot2 = random.choice(symbols)
        slot3 = random.choice(symbols)

        result = f"{slot1} │ {slot2} │ {slot3}"

        # =========================
        # JACKPOT
        # =========================
        if slot1 == slot2 == slot3:

            reward = amount * 5

            user["wallet"] += reward

            message = (
                f"🎉 JACKPOT!\n\n"
                f"{result}\n\n"
                f"💰 Won: `+{format_money(reward)}`"
            )

            embed = success_embed(
                "🎰 LEON SLOTS",
                message
            )

            # =====================================
            # JACKPOT ACHIEVEMENT
            # =====================================
            achievement_cog = self.bot.get_cog(
                "Achievements"
            )

            if achievement_cog:

                await achievement_cog.give_achievement(
                    ctx,
                    ctx.author,
                    "jackpot",
                    "🎰 Jackpot"
                )

        # =========================
        # 2 MATCH
        # =========================
        elif slot1 == slot2 or slot2 == slot3 or slot1 == slot3:

            reward = amount * 2

            user["wallet"] += reward

            message = (
                f"✨ NICE!\n\n"
                f"{result}\n\n"
                f"💰 Won: `+{format_money(reward)}`"
            )

            embed = success_embed(
                "🎰 LEON SLOTS",
                message
            )

        # =========================
        # LOSE
        # =========================
        else:

            user["wallet"] -= amount

            message = (
                f"💀 YOU LOST\n\n"
                f"{result}\n\n"
                f"💸 Lost: `-{format_money(amount)}`"
            )

            embed = error_embed(
                "🎰 LEON SLOTS",
                message
            )

        save_data(data)

        # =====================================
        # GAMBLER ACHIEVEMENT
        # =====================================
        achievement_cog = self.bot.get_cog(
            "Achievements"
        )

        if achievement_cog:

            await achievement_cog.give_achievement(
                ctx,
                ctx.author,
                "gambler",
                "🎲 Gambler"
            )

        await ctx.send(embed=embed)
        
    # =========================
    # TOP BALANCE
    # =========================
    @commands.command(aliases=["topbal", "rich"])
    async def leaderboard(self, ctx):

        data = load_data()

        leaderboard_data = []

        for user_id, user_data in data.items():

            total_money = (
                user_data["wallet"] +
                user_data["bank"]
            )

            leaderboard_data.append(
                (int(user_id), total_money)
            )

        # SORT DESC
        leaderboard_data = sorted(
            leaderboard_data,
            key=lambda x: x[1],
            reverse=True
        )

        embed = default_embed(
            "🏆 LEONBOT LEADERBOARD",
            "💰 Top richest users"
        )

        rank = 1

        for user_id, money in leaderboard_data[:10]:

            member = ctx.guild.get_member(user_id)

            if member is None:
                continue

            embed.add_field(
                name=f"#{rank} • {member.name}",
                value=f"💰 `{format_money(money)}`",
                inline=False
            )

            rank += 1

        await ctx.send(embed=embed)
        
    # =========================
    # DEPOSIT
    # =========================
    @commands.command(aliases=["dep"])
    async def deposit(self, ctx, amount=None):

        if amount is None:
            return await ctx.send(
            embed=error_embed(
                "❌ INVALID AMOUNT",
                "Contoh: `$deposit 500`"
            )
        )

        data = load_data()
        create_account(data, ctx.author.id)

        user = data[str(ctx.author.id)]

        if amount.lower() == "all":
            amount = user["wallet"]

        else:

            if not amount.isdigit():
                return await ctx.send(
                embed=error_embed(
                    "❌ INVALID NUMBER",
                    "Masukkan angka yang valid."
                )
            )

        amount = int(amount)

        if amount <= 0:
            return await ctx.send(
            embed=error_embed(
                "❌ INVALID AMOUNT",
                "Amount harus lebih dari 0."
            )
        )

        if user["wallet"] < amount:
            return await ctx.send(
            embed=error_embed(
                "❌ NOT ENOUGH MONEY",
                "Wallet lu tidak cukup."
            )
        )

        user["wallet"] -= amount
        user["bank"] += amount

        save_data(data)

        embed = success_embed(
            "🏦 DEPOSIT SUCCESS",
            (
            f"💰 Deposited: `{format_money(amount)}`\n\n"
            f"🏦 Bank: `{format_money(user['bank'])}`"
        )
    )

        await ctx.send(embed=embed)


    # =========================
    # WITHDRAW
    # =========================
    @commands.command(aliases=["with"])
    async def withdraw(self, ctx, amount=None):

        if amount is None:
            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID AMOUNT",
                    "Contoh: `$withdraw 500`"
                )
            )

        data = load_data()
        create_account(data, ctx.author.id)

        user = data[str(ctx.author.id)]

        if amount.lower() == "all":
            amount = user["bank"]

        else:

            if not amount.isdigit():
                return await ctx.send(
                    embed=error_embed(
                        "❌ INVALID NUMBER",
                        "Masukkan angka yang valid."
                    )
                )

            amount = int(amount)

        if amount <= 0:
            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID AMOUNT",
                    "Amount harus lebih dari 0."
                )
            )

        if user["bank"] < amount:
            return await ctx.send(
                embed=error_embed(
                    "❌ NOT ENOUGH MONEY",
                    "Uang bank lu tidak cukup."
                )
            )

        user["bank"] -= amount
        user["wallet"] += amount

        save_data(data)

        embed = success_embed(
            "🏦 WITHDRAW SUCCESS",
            (
                f"💰 Withdrawn: `{format_money(amount)}`\n\n"
                f"💵 Wallet: `{format_money(user['wallet'])}`"
            )
        )

        await ctx.send(embed=embed) 

    # =========================
    # DAILY
    # =========================
    @commands.command()
    async def daily(self, ctx):

        data = load_data()
        create_account(data, ctx.author.id)

        user = data[str(ctx.author.id)]

        now = time.time()

        cooldown = 86400

        if now - user["daily"] < cooldown:

            remaining = int(cooldown - (now - user["daily"]))

            hours = remaining // 3600
            minutes = (remaining % 3600) // 60

            embed = error_embed(
                "⏳ DAILY COOLDOWN",
                f"Coba lagi dalam `{hours} jam {minutes} menit`"
            )

            return await ctx.send(embed=embed)

        reward = 500
        # VIP BONUS
        vip_role = discord.utils.get(
            ctx.author.roles,
            name="VIP"
        )

        if vip_role:

            amount *= 2

        user["wallet"] += reward
        user["daily"] = now

        save_data(data)

        embed = success_embed(
            "🎁 DAILY REWARD",
            (
                f"Lu claim daily reward!\n\n"
                f"💰 Coins: `+{format_money(reward)}`"
            )
        )

        await ctx.send(embed=embed)

    # =========================
    # WORK
    # =========================
    @commands.command()
    async def work(self, ctx):

        data = load_data()
        create_account(data, ctx.author.id)

        user = data[str(ctx.author.id)]

        now = time.time()

        cooldown = 1800

        if now - user["work"] < cooldown:

            remaining = int(cooldown - (now - user["work"]))

            minutes = remaining // 60
            seconds = remaining % 60

            embed = error_embed(
                "💼 WORK COOLDOWN",
                f"Coba lagi dalam `{minutes} menit {seconds} detik`"
            )

            return await ctx.send(embed=embed)

        jobs = [
            "💻 Coding website",
            "🎨 Design logo",
            "🍔 Jadi kasir",
            "📦 Jadi kurir",
            "🧹 Bersih-bersih server",
            "🎬 Edit video"
        ]

        job = random.choice(jobs)

        reward = random.randint(100, 500)
        # VIP BONUS
        vip_role = discord.utils.get(
            ctx.author.roles,
            name="VIP"
        )

        if vip_role:

            amount *= 2

        user["wallet"] += reward
        user["work"] = now

        save_data(data)

        embed = success_embed(
            "💼 WORK COMPLETE",
            (
                f"{job}\n\n"
                f"💰 Earned: `+{format_money(reward)}`"
            )
        )

        await ctx.send(embed=embed)

    # =========================
    # BEG
    # =========================
    @commands.command()
    async def beg(self, ctx):

        data = load_data()
        create_account(data, ctx.author.id)

        user = data[str(ctx.author.id)]

        now = time.time()

        cooldown = 60

        if now - user["beg"] < cooldown:

            remaining = int(cooldown - (now - user["beg"]))

            embed = error_embed(
                "🥺 BEG COOLDOWN",
                f"Tunggu `{remaining} detik` lagi"
            )

            return await ctx.send(embed=embed)

        success = random.randint(1, 100)

        user["beg"] = now

        if success <= 70:

            reward = random.randint(10, 100)

            messages = [
                "Orang asing memberi lu uang.",
                "Kakek baik hati membantu lu.",
                "Lu dikasih receh di jalan.",
                "Streamer terkenal ngasih donasi."
            ]

            message = random.choice(messages)

            user["wallet"] += reward

            save_data(data)

            embed = success_embed(
                "🥺 BEGGING SUCCESS",
                (
                    f"{message}\n\n"
                    f"💰 Coins: `+{format_money(reward)}`"
                )
            )

        else:

            failed_messages = [
                "Lu diabaikan semua orang.",
                "Satpam mengusir lu.",
                "Ga ada yang peduli.",
                "Lu malah diketawain."
            ]

            message = random.choice(failed_messages)

            save_data(data)

            embed = error_embed(
                "❌ BEGGING FAILED",
                message
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Economy(bot))