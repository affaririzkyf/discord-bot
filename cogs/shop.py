import discord
from discord.ext import commands
import json

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

from utils.inventory_utils import (
    load_inventory,
    save_inventory,
    create_inventory
)


class Shop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.items = {

            "booster": {
                "price": 5000,
                "description": "⚡ Double XP Booster"
            },

            "lucky": {
                "price": 3000,
                "description": "🍀 Lucky Charm"
            },

            "crate": {
                "price": 2500,
                "description": "🎁 Mystery Crate"
            },

            "vip": {
                "price": 10000,
                "description": "👑 VIP Role"
            }
        }

    # =========================
    # SHOP
    # =========================
    @commands.command()
    async def shop(self, ctx):

        embed = default_embed(
            "🛒 LEON SHOP",
            "⚡ Welcome to LeonBot Shop"
        )

        for item_name, item_data in self.items.items():

            embed.add_field(
                name=f"🧩 {item_name.upper()}",
                value=(
                    f"{item_data['description']}\n"
                    f"💰 Price: `{format_money(item_data['price'])}`"
                ),
                inline=True
            )

        embed.set_footer(
            text="Gunakan ?buy <item>"
        )

        await ctx.send(embed=embed)

    # =========================
    # BUY ITEM
    # =========================
    @commands.command()
    async def buy(self, ctx, item=None):

        if item is None:

            return await ctx.send(
                embed=error_embed(
                    "❌ INVALID USAGE",
                    "Contoh: `?buy booster`"
                )
            )

        item = item.lower()

        if item not in self.items:

            return await ctx.send(
                embed=error_embed(
                    "❌ ITEM NOT FOUND",
                    "Item tidak tersedia di shop."
                )
            )

        # LOAD ECONOMY
        data = load_data()

        create_account(data, ctx.author.id)

        user = data[str(ctx.author.id)]

        # LOAD INVENTORY
        inventory = load_inventory()

        create_inventory(
            inventory,
            ctx.author.id
        )

        item_data = self.items[item]

        price = item_data["price"]

        # CHECK MONEY
        if user["wallet"] < price:

            return await ctx.send(
                embed=error_embed(
                    "❌ NOT ENOUGH MONEY",
                    (
                        f"💰 Harga item: `{format_money(price)}`\n"
                        f"💵 Wallet lu tidak cukup."
                    )
                )
            )

        # REMOVE MONEY
        user["wallet"] -= price

        # =====================================
        # VIP ROLE + ACHIEVEMENT
        # =====================================
        if item == "vip":

            role = discord.utils.get(
                ctx.guild.roles,
                name="VIP"
            )

            if role:

                await ctx.author.add_roles(role)

                # ACHIEVEMENT
                achievement_cog = self.bot.get_cog(
                    "Achievements"
                )

                if achievement_cog:

                    await achievement_cog.give_achievement(
                        ctx,
                        ctx.author,
                        "vip",
                        "💎 VIP"
                    )

        # ADD ITEM INVENTORY
        user_inventory = inventory[str(ctx.author.id)]

        if item not in user_inventory:

            user_inventory[item] = 0

        user_inventory[item] += 1

        # SAVE
        save_data(data)
        save_inventory(inventory)

        embed = success_embed(
            "🛒 PURCHASE SUCCESS",
            (
                f"🧩 Item: `{item.upper()}`\n"
                f"💸 Price: `{format_money(price)}`\n"
                f"🎒 Masuk ke inventory."
            )
        )

        await ctx.send(embed=embed)

    # =========================
    # INVENTORY
    # =========================
    @commands.command(
        aliases=["inv"]
    )
    async def inventory(self, ctx):

        inventory = load_inventory()

        create_inventory(
            inventory,
            ctx.author.id
        )

        user_inventory = inventory[
            str(ctx.author.id)
        ]

        embed = default_embed(
            "🎒 LEON INVENTORY",
            f"👤 {ctx.author.mention}"
        )

        if len(user_inventory) == 0:

            embed.description = (
                "📦 Inventory masih kosong."
            )

            return await ctx.send(embed=embed)

        for item, amount in user_inventory.items():

            embed.add_field(
                name=f"🧩 {item.upper()}",
                value=f"📦 Amount: `{amount}`",
                inline=True
            )

        await ctx.send(embed=embed)


# =========================
# SETUP
# =========================
async def setup(bot):

    await bot.add_cog(Shop(bot))