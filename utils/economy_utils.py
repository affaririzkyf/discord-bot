import json
import os

ECONOMY_FILE = "data/economy.json"


# =========================
# LOAD DATA
# =========================
def load_data():

    if not os.path.exists(ECONOMY_FILE):
        with open(ECONOMY_FILE, "w") as f:
            json.dump({}, f)

    with open(ECONOMY_FILE, "r") as f:
        return json.load(f)


# =========================
# SAVE DATA
# =========================
def save_data(data):

    with open(ECONOMY_FILE, "w") as f:
        json.dump(data, f, indent=4)


# =========================
# CREATE ACCOUNT
# =========================
def create_account(data, user_id):

    user_id = str(user_id)

    if user_id not in data:
        data[user_id] = {
            "wallet": 0,
            "bank": 0,
            "daily": 0,
            "work": 0,
            "beg": 0
        }

    return data


# =========================
# FORMAT MONEY
# =========================
def format_money(amount):
    return f"{amount:,}"