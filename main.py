from classes.game import Person, bcolors  # The person and preset color classes
from classes.magic import Spell  # The spell class
from classes.inventory import Item
import random

# Create Black Magic
fire = Spell("Fire", 10, 700, "black")
thunder = Spell("Thunder", 10, 800, "black")
blizzard = Spell("Blizzard", 10, 900, "black")
meteor = Spell("Meteor", 20, 1000, "black")
quake = Spell("Quake", 14, 1100, "black")

# Create White Magic
cure = Spell("Cure", 12, 1000, "white")
cura = Spell("Cura", 18, 2000, "white")

# Create some Items
potion = Item("Potion", "potion", "Heals 800 HP", 800)
hipotion = Item("Hi-Potion", "potion", "Heals 1250 HP", 1250)
superpotion = Item("Super-Potion", "potion", "Heals 1700 HP", 1700)
elixer = Item("Elixer", "elixer", "Fully restores the HP & MP of a party member", 9999)
megaelixer = Item("Mega-Elixer", "elixer", "Fully restores the HP & MP of all party members", 9999)
grenade = Item("Grenade", "weapon", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": megaelixer, "quantity": 2}, {"item": grenade, "quantity": 2}]

# (You)The player and the enemy; 2 instances of 'Person'
player1 = Person('Hori', 3200, 132, 60, 34, player_spells, player_items)
player2 = Person('Volo', 4200, 122, 60, 34, player_spells, player_items)
player3 = Person('Roxy', 3600, 111, 60, 34, player_spells, player_items)
players = [player1, player2, player3]

enemy_spells = [fire, meteor, cure]

enemy1 = Person('Imp  ', 7000, 500, 1000, 50, enemy_spells, [])
enemy2 = Person('Magus', 12000, 700, 800, 25, enemy_spells, [])
enemy3 = Person('Imp  ', 7000, 500, 1000, 50, enemy_spells, [])
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!\n" + bcolors.ENDC + "This is normal text!")

while running:
    print("=============================")
    if not running:
        continue

    for player in players:
        player.get_stats()
        # print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        print("\n<" + bcolors.BOLD + player.name + bcolors.ENDC + ">")
        player.choose_action()
        choice = input("Choose action: ")
        index = int(choice) - 1  # This is the index in the 'action' list

        if index == 0:  # Attack
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name + " for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]

        elif index == 1:  # Magic
            player.choose_magic()
            magic_choice = int(input("Choose a spell: ")) - 1  # This is the index in the 'action' list

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]  # The chosen spell
            magic_dmg = spell.generate_spell_damage()  # The generated spell damage

            current_mp = player.get_mp()

            if spell.cost > current_mp:  # Insufficient mana => we cannot cast the spell
                print(bcolors.FAIL + "Not enough MP!" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)

            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to "
                      + enemies[enemy].name + "." + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

        elif index == 2:  # Items
            player.choose_item()
            item_choice = int(input("Choose an item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]
            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue
            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP." + bcolors.ENDC)

            elif item.type == "elixer":
                player.hp = player.maxhp
                player.mp = player.maxmp

                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP." + bcolors.ENDC)

            elif item.type == "weapon":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to " +
                      enemies[enemy].name + "." + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

    # Check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # Check if player won
    if defeated_enemies == 2:  # The enemy player dies
        print(bcolors.OKGREEN + bcolors.BOLD + "You win!" + bcolors.ENDC)
        running = False
    # Check if enemy won
    elif defeated_players == 2:  # You die
        print(bcolors.FAIL + "You have been defeated by the enemy team!" + bcolors.ENDC)
        running = False

    # Enemy's turn
    for enemy in enemies:
        if len(enemies) > 1:
            enemy_choice = random.randrange(0, len(enemies) - 1)  # We make the enemy attack us
        elif len(enemies) == 1:
            enemy_choice = 0
        else:
            running = False
            continue

        # Enemy chooses to attack
        if enemy_choice == 0:
            if len(players) > 1:
                target = random.randrange(0, len(players) - 1)
            elif len(players) == 1:
                target = 0
            else:
                running = False
                continue

            enemy_dmg = enemies[enemy_choice].generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", ""), "attacks", players[target].name.replace(" ", ""), "for", enemy_dmg,
                  "points of damage.")

        # Enemy chooses to cast a spell
        if enemy_choice == 1:
            spell = enemy.choose_enemy_spell()
            magic_dmg = spell.generate_spell_damage()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals " + enemy.name + " for", str(magic_dmg), "HP." +
                      bcolors.ENDC)

            elif spell.type == "black":
                if len(players) > 1:
                    target = random.randrange(0, len(players) - 1)
                elif len(players) == 1:
                    target = 0
                else:
                    running = False
                    continue

                print(players[target].name)

                players[target].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + enemy.name + "'s " + spell.name + " deals", str(magic_dmg),
                      "points of damage to " + players[target].name + "." + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " has died.")
                    del players[target]
