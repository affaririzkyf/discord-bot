import json
import os

INVENTORY_FILE = "data/inventory.json"


# =========================
# LOAD INVENTORY
# =========================
def load_inventory():

    if not os.path.exists(INVENTORY_FILE):

        with open(INVENTORY_FILE, "w") as f:

            json.dump({}, f)

    with open(INVENTORY_FILE, "r") as f:

        return json.load(f)


# =========================
# SAVE INVENTORY
# =========================
def save_inventory(data):

    with open(INVENTORY_FILE, "w") as f:

        json.dump(data, f, indent=4)


# =========================
# CREATE INVENTORY
# =========================
def create_inventory(data, user_id):

    user_id = str(user_id)

    if user_id not in data:

        data[user_id] = {}