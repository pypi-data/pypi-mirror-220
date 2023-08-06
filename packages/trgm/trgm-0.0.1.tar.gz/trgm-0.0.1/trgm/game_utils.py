import time
import sys
import random
import pickle

def write(text, speed):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)

    print("")

# Saving Data    
def saveData(data):
    with open('data.pickle', 'wb') as f:
        pickle.dump(data, f)

def loadData():
    with open('data.pickle', 'rb') as f:
        return pickle.load(f)

# Inventory Functions

def create_item(name, description):
    return {"name": name, "description": description}

def show_inventory(inventory):
    print("Inventory:")
    if not inventory:
        print("Inventory is Empty.")
    else:
        for item in inventory:
            print(f"{item['name']}: {item['description']}")

def add_item_to_inventory(inventory, item):
    inventory.append(item)

def discard_item(inventory, item_name):
    for item in inventory:
        if item["name"] == item_name:
            inventory.remove(item)
            print(f"{item_name} has been discarded.")
            break
    else:
        print(f"{item_name} not found in inventory.")

# Enemy Functions

def calculate_damage(attacker):
    return random.randint(attacker["damage"] - 3, attacker["damage"] + 3)

def player_attack(player):
    if player["equipped_weapon"]:
        return calculate_damage(player) + player["equipped_weapon"]["damage"]
    else:
        return calculate_damage(player)

def enemy_attack(enemy):
    return calculate_damage(enemy)

def update_health(entity, damage):
    entity["current_hp"] -= damage
    if entity["current_hp"] < 0:
        entity["current_hp"] = 0

def is_battle_over(player, enemy):
    return player["current_hp"] <= 0 or enemy["current_hp"] <= 0

def battle(player, enemy):
    print(f"An enemy {enemy['name']} appears!")

    while not is_battle_over(player, enemy):
        player_damage = player_attack(player)
        enemy_damage = enemy_attack(enemy)

        update_health(player, enemy_damage)
        update_health(enemy, player_damage)

        print(f"Player HP: {player['current_hp']} | Enemy HP: {enemy['current_hp']}")

        if player["current_hp"] <= 0:
            print("Game Over! You were defeated.")
            return False
        else:
            print(f"You defeated the {enemy['name']}! You gain some loot and experience points.")
            # Implement rewards or other logic here.
            return True

def create_enemy(name, health, damage):
    enemy = {
        "name": name,
        "max_hp": health,
        "current_hp": health,
        "damage": damage
    }
    return enemy