import random
import os


# CHANGES NEEDED: UPDATE random_mob(), count(), main(); CREATE use_usable(), player_name_query(), replay(),
# get_attack_story(); CONSIDER randomized_rooms() count effect, changing .counter attribute to .count, get_Alert
# ('RANDOM ATTACK', get_attack_story), removing location (center, northwest, etc.); POTENTIAL DEVELOPMENTS: UPDATE
# main() to be "main_menu" for additional game variations (western, school, lab); ADD player_health, player_attack,
# minion_health - could knock out minion and autowin item upon entering room. 



# Function to print break lines.
def print_break():
    print("----------------------------------------------------------------------------------------------------------")


# Function to display the game instructions.
def show_instructions():
    print("\nText Based Game: The Dark King\n")
    print("Objective: Collect 7 items before entering the Dark King Ashakusa's chambers.")
    print("Move Commands: 'go' 'cardinal direction' (e.g., go south, go north, go west, go east)")
    print("Collect Item: 'get' 'item name' (i.e., get Wand, get Ironshadow.)")
    print_break()


# Function to get stored initial values.
def get_initial_values():
    room_names = ['Chapel - Ventus Vayu', 'King\'s Chamber - Calig Crepundia', 'Kitchen - Tejas Ignis',
                  'Library - Akusha', 'Gallery - Levi\'s Luminx', 'Bathroom - Apaszer Stici', 'Cellar - Necro',
                  'Dungeon - Privithi Ager']
    room_items = ['Wand', 'Dark King Ashakusa', 'Athame', 'Heart', 'Bolt', 'Chalice', 'Ironshadow', 'Pentacle']
    minions = ['Sirocco, the Wind Elemental', 'Dark King Ashakusa', 'Rhys, the Fire Elemental', 'Drago, the Phantom',
               'Barak, the Lightning Elemental', 'Maya, the Water Elemental', 'Shoiynbai, the Metal Elemental',
               'Afra, the Earth Elemental']
    game_names = ['lower_number', 'higher_number', 'right_guess', 'roll_1', 'roll_2', 'roll_3', 'rock_paper_scissors']
    # usables = ['Emerald Shield', 'Ruby Shield', 'Sapphire Shield']
    inventory, u_inventory, usables_inventory = [], [], []
    return room_names, room_items, minions, game_names, inventory, u_inventory, usables_inventory


# Function to display an alert.
def show_alert(alert_type, alert):
    print(f"ALERT: {alert_type}\n")
    print(alert)


# Function to randomize rooms, room item, room minion, and mini games.
def randomize_rooms(times_rooms_randomized, room_names, room_items, minions, game_names):
    randomized_rooms = list(zip(room_names, room_items, minions))
    random.shuffle(randomized_rooms)
    room_names, room_items, minions = zip(*randomized_rooms)
    if times_rooms_randomized == 0:
        random.shuffle(game_names)
    else:
        show_alert('Room', 'Room has been randomized')
    times_rooms_randomized += 1
    return room_names, room_items, minions, game_names


# Function to set rooms.
def set_room(room_names, room_items, minions):
    rooms = {
        room_names[0]: {'East': room_names[1], 'South': room_names[3], 'Item': room_items[0], 'Minion': minions[0],
                        'Location': 'northwest'},
        room_names[1]: {'East': room_names[2], 'South': 'Great Hall of Fallen Lights', 'West': room_names[0],
                        'Item': room_items[1], 'Minion': minions[1], 'Location': 'north'},
        room_names[2]: {'South': room_names[4], 'West': room_names[1], 'Item': room_items[2], 'Minion': minions[2],
                        'Location': 'northeast'},
        room_names[3]: {'East': 'Great Hall of Fallen Lights', 'North': room_names[0], 'South': room_names[5],
                        'Item': room_items[3], 'Minion': minions[3], 'Location': 'west'},
        'Great Hall of Fallen Lights': {'East': room_names[4], 'North': room_names[1], 'South': room_names[6],
                                        'West': room_names[3], 'Location': 'center'},
        room_names[4]: {'North': room_names[2], 'South': room_names[7], 'West': 'Great Hall of Fallen Lights',
                        'Item': room_items[4], 'Minion': minions[4], 'Location': 'east'},
        room_names[5]: {'East': room_names[6], 'North': room_names[3], 'Item': room_items[5], 'Minion': minions[5],
                        'Location': 'southwest'},
        room_names[6]: {'East': room_names[7], 'North': 'Great Hall of Fallen Lights', 'West': room_names[5],
                        'Item': room_items[6], 'Minion': minions[6], 'Location': 'south'},
        room_names[7]: {'North': room_names[4], 'West': room_names[6], 'Item': room_items[7], 'Minion': minions[7],
                        'Location': 'southeast'}
    }
    return rooms


# Function to assign game names to rooms except the main and villain rooms.
def assign_room_games(times_rooms_randomized, rooms, game_names):
    if times_rooms_randomized == 0:
        i = 0
        for room in rooms:
            if room not in ('Great Hall of Fallen Lights', 'King\'s Chamber - Calig Crepundia'):
                rooms[room]['Game'] = game_names[i]
                i += 1


# Function to set initial values. 
# room_names, room_items, minions, game_names, inventory, u_inventory, usables_inventory
def set_up_game(times_rooms_randomized):
    room_names, room_items, minions, game_names, inventory, u_inventory, usables_inventory = get_initial_values()
    room_names, room_items, minions, game_names = randomize_rooms(times_rooms_randomized, room_names, room_items,
                                                                  minions, game_names)
    rooms = set_room(room_names, room_items, minions)
    assign_room_games(times_rooms_randomized, rooms, game_names)
    return rooms, inventory, u_inventory, usables_inventory


# Function to capture location status.
def get_location(rooms, current_room):
    location = rooms[current_room]['Location']
    room_no = [room for room in rooms].index(current_room) + 1
    return location, room_no


# Function to display location status. // CONSIDER removing location (center, northwest, etc.)
def show_location(rooms, current_room):
    location, room_no = get_location(rooms, current_room)
    print(f"Room {room_no} ({location.title()})")


# Function to display availability of item in a room.
def show_item(current_room, rooms, inventory):
    if current_room != 'Great Hall of Fallen Lights' and rooms[current_room].get('Item') not in inventory:
        print(f"\nYou see the {rooms[current_room]['Item']} in the distance.")
    elif current_room != 'Great Hall of Fallen Lights' and rooms[current_room].get('Item') in inventory:
        print(f"\nRoom cleared. {rooms[current_room]['Item']} has been obtained.")


# Function to display the current room status. 
def show_room_status(current_room, inventory, rooms, usables_inventory):
    show_location(rooms, current_room)
    print(f"{current_room}")
    print("Inventory:", '[%s]' % ', '.join(map(str, inventory)))
    print("Usables: ", '[%s]' % ', '.join(map(str, usables_inventory)))
    show_item(current_room, rooms, inventory)
    print_break()

# Function to display random mob attack. / FIX - Break up into pick_random_mob, move variables, return enemy_mob?  
# Need to add use of item first, item config - thwart. NEED to add notify_random_attack, look to search_for_usables
# CONSIDER get_Alert('RANDOM ATTACK', get_attack_story)
# def random_mob(minions, inventory, room_items):
#     mob_list = [minion for minion in minions if minion != 'Dark King Ashakusa']
#     mob_item_list = [item for item in room_items if item != 'Dark King Ashakusa']
#     random.shuffle(mob_item_list)
#     enemy_mob = random.choice(mob_list)
#     print("Alert: Random Attack\n")
#     if mob_item_list[mob_list.index(enemy_mob)] in inventory:
#         get_Alert('RANDOM ATTACK', 'You thwarted random attack from {enemy_mob} by using the\
#                   {mob_item_list[mob_list.index(enemy_mob)]}.')        
#     else:
#         get_Alert('RANDOM ATTACK', '{enemy_mob} randomly attacked. You lost \
#                   {inventory.pop(random.randint(0, len(inventory) - 1))}!') 


# Function to display game win message.
def show_game_win_message():
    print("You open the gateway with the Wand, Athame, Pentacle, and Chalice as you feel your energy begin to drain.")
    print("The Dark King launches an attack at you, but you parry his attack, and the next, and the next, but with")
    print("each strike you grow weaker. You must act now! You allow the Dark King's next strike to propel you back")
    print("through the gateway and chuck the Bolt at him. It's a hit! You land hard on the ground, weakened, but you")
    print("must finish the ritual. You hastily throw the Ironshadow into the gateway as the Dark King groans in pain")
    print("and then consume the heart. As you recite the last words of the prayer, you see the gateway shut before you")
    print("pass out from sheer exhaustion.\n\nCongratulations, you have defeated the Dark King Ashakusa!\n")
    os.system('pause')
    exit()


# Function to display game lose message.
def show_game_lose_message():
    print("You attempt to cast open the gateway without the required items to no avail. You feel your energy begin to")
    print("drain. The Dark King launches an attack at you, but you parry his attack, and the next, and the next, but")
    print("with each strike you grow weaker. After a long and hard fought battle, you feel the embrace of darkness as")
    print("you are struck by the Dark King's blade.\n\nYou lose! The Dark King Ashakusa has defeated you!\n")
    os.system('pause')
    exit()


# Function to exit game.
def exit_game(rooms, current_room, inventory):
    if rooms[current_room].get('Item') == 'Dark King Ashakusa' and len(inventory) > 6:
        show_game_win_message()
    elif rooms[current_room].get('Item') == 'Dark King Ashakusa' and len(inventory) < 7:
        show_game_lose_message()


# Function to capture user's command.
def get_user_cmd():
    return input("Type a command: ").title().split()


# Function for room story attached to item wand.
def wand():
    print("Flying high into the sky with child-like enthusiasm, you feel the air around you become thin. You")
    print("think it at first to be a matter of your altitude but in front of the Winterstorm Winds (Wand) you see")
    print("an air elemental sucking the air from the sky form before you. Battle it and obtain the Wand.\n")


# Function for room story attached to item athame.
def athame():
    print("A bead of sweat drops from your forehead as the cool, crisp room begins to heat. Suddenly, the room")
    print("is engulfed in flames as a fire elemental rises from the ground blocking your path to the Ferocious")
    print("Flame (Athame). Battle it and obtain the Athame.\n")


# Function for room story attached to item heart.
def heart():
    print("Ahead of the aimlessly walking spirits you see the Heart of Hope (Heart). A dark spirit turns.")
    print("Dark Spirit: \"Fresh Blood... A heart you seek, hmm? How about... giving me YOURS!\"")
    print("The dark spirit launches toward you. Battle it and obtain the Heart.\n")


# Function for room story attached to item bolt.
def bolt():
    print("The lights flicker before they become blinding. You feel a presence behind you. You turn and are")
    print("grazed by a lightning bolt. The lights flicker and you see the Lightning Lamp (Bolt) ahead. You make")
    print("out a disguised light elemental too before the lights brighten again. Battle it and obtain the Bolt.\n")


# Function for room story attached to item chalice.
def chalice():
    print("A bit weary, you splash your face with some water. A watery hand grabs out at you and you fall back.")
    print("Water begins to flood the room. You catch a glimpse of the Treacherous Tide (Chalice) as the water")
    print("elemental appears and devours it before going on the offensive. Battle it and obtain the Chalice.\n")


# Function for room story attached to item ironshadow.
def ironshadow():
    print("A few lights seep into the dark room. A light flickers and you move dodging what sounds to be a heavy")
    print("metal piece. Your eyes adjust a bit and you see the Shadow Metal (Ironshadow) nearby. Sound guided, you")
    print("block the physical attack of what feels like a metal elemental. Battle it and obtain the Ironshadow.\n")


# Function for room story attached to item pentacle.
def pentacle():
    print("The air smells horrible here. As you step in, the ground trembles. Several holes appear and an entity")
    print("springs up. You parry its attack but fall into a nearby hole. From the ledge, you hurl yourself up and")
    print("spot both the Sleeping Sands (Pentacle) and an earth elemental. Battle it and obtain the Pentacle.\n")


# Function to display room_story.
def show_room_story(rooms, current_room):
    globals()[rooms.get(current_room, {}).get('Item').lower()]()


# Function to capture mini game objective.
def get_game_objective(rooms, current_room):
    game = rooms[current_room]['Game'].replace('_', ' ').title()
    to_win = game + " while " + rooms[current_room]['Minion'] + " does not." if game in ('Roll 1', 'Roll 2', 'Roll 3')\
        else "Roll a number " + game.lower().split(' ').pop(0) + " than " + rooms[current_room]['Minion'] + "."
    if game not in ('Roll 1', 'Roll 2', 'Roll 3', 'Higher Number', 'Lower Number'):
        to_win = "Roll the same number as " + rooms[current_room]['Minion'] + "." if game == 'Right Guess' else \
            "Beat " + rooms[current_room]['Minion'] + "'s hand - rock beats scissors, scissors paper, and paper rock."
    return game, to_win


# Function to display mini game objective.
def show_game_objective(rooms, current_room):
    game, to_win = get_game_objective(rooms, current_room)
    print("Objective: Defeat " + rooms[current_room]['Minion'] + " in a game of " + game + ". ")
    print("Win: " + to_win + "\n")


# Function to append inventory with current room item.
def append_inventory(inventory, rooms, current_room):
    inventory.append(rooms[current_room].get('Item'))


# Function to display room win message.
def show_room_win_message(inventory, rooms, current_room):
    append_inventory(inventory, rooms, current_room)
    print(f"\nYou have defeated {rooms[current_room]['Minion']}.")
    print(f"You have obtained the {rooms[current_room]['Item']}.")


# Function to display room lose message.
def show_room_lose_message(rooms, current_room):
    print(f"\n{rooms[current_room]['Minion']} has defeated you.")


# Function .... / FIX - Determine viability.
def count():
    count.counter += 1
    main.counter = 0


# Function to capture action for mini game stats.
def get_mini_action(player_roll):
    return "hand" if player_roll in ('rock', 'paper', 'scissors') else "rolls"


# Function to display mini game stats.
def show_mini_stats(player_roll, enemy_roll, rooms, current_room):
    action = get_mini_action(player_roll)
    print(f"Mekias {action}: {player_roll}")
    print(f"{rooms[current_room]['Minion']} {action}: {enemy_roll}")


# Function to select random usable.
def random_usable(u_inventory):
    random_usable_list = []
    for item in ['Emerald Shield', 'Ruby Shield', 'Sapphire Shield']:
        if u_inventory.count(item) < 5:
            random_usable_list.append(item)
    return random.choice(random_usable_list)


# Function to append usable to usable inventories: u_inventory and usables_inventory.
def append_usable(usable, u_inventory, usables_inventory):
    u_inventory.append(usable)
    if u_inventory.count(usable) == 1:
        usables_inventory.append(usable + " (" + str(u_inventory.count(usable)) + "x)")
    elif u_inventory.count(usable) > 1:
        # MOVE to update_usables_inventory. Will need for usables being used. CHECK enumerate for other functions.
        index_list = []
        for item in ['Emerald Shield', 'Ruby Shield', 'Sapphire Shield']:
            index_list.append(item.startswith(usable))
        index_no_list = [i for i, boolean in enumerate(index_list) if boolean]
        usables_inventory[int(index_no_list[0])-1] = usable + f" (" + str(u_inventory.count(usable)) + "x)" 


# Function to capture usable.
def get_usable(u_inventory, usables_inventory):
    usable = random_usable(u_inventory)
    append_usable(usable, u_inventory, usables_inventory)


# Function to search for usable.
def search_for_usable(u_inventory, usables_inventory):
    i = random.randint(0, 10)
    if random.randint(4, 9) in range(i):
        get_usable(u_inventory, usables_inventory)


# Function to calculate player and enemy rolls in mini game Lower Number.
def lower_number_rolls():
    player_roll = random.randint(0, 6)
    return player_roll, random.randint(0, 6) + player_roll if lower_number.counter % 3 == 0 else random.randint(0, 6)


# Function to display evaluation of player and enemy rolls in mini game Lower Number.
def show_lower_number_evaluate(inventory, u_inventory, usables_inventory, rooms, current_room):
    player_roll, enemy_roll = lower_number_rolls()
    show_mini_stats(player_roll, enemy_roll, rooms, current_room)
    show_room_win_message(inventory, rooms, current_room) if player_roll < enemy_roll else\
        show_room_lose_message(rooms, current_room)
    search_for_usable(u_inventory, usables_inventory)


# Function to play mini game Lower Number.
def lower_number(inventory, u_inventory, usables_inventory, rooms, current_room):
    lower_number.counter += 1
    show_room_story(rooms, current_room)
    show_game_objective(rooms, current_room)
    show_lower_number_evaluate(inventory, u_inventory, usables_inventory, rooms, current_room)
    count()


# Function to calculate player and enemy rolls in mini game Higher Number.
def higher_number_rolls():
    enemy_roll = random.randint(0, 6)
    return enemy_roll, random.randint(0, 6) + enemy_roll if higher_number.counter % 3 == 0 else random.randint(0, 6)


# Function to display evaluation of player and enemy rolls in mini game Higher Number.
def show_higher_number_evaluate(inventory, u_inventory, usables_inventory, rooms, current_room):
    enemy_roll, player_roll = higher_number_rolls()
    show_mini_stats(player_roll, enemy_roll, rooms, current_room)
    show_room_win_message(inventory, rooms, current_room) if player_roll > enemy_roll else\
        show_room_lose_message(rooms, current_room)
    search_for_usable(u_inventory, usables_inventory)


# Function to play mini game High Number.
def higher_number(inventory, u_inventory, usables_inventory, rooms, current_room):
    higher_number.counter += 1
    show_room_story(rooms, current_room)
    show_game_objective(rooms, current_room)
    show_higher_number_evaluate(inventory, u_inventory, usables_inventory, rooms, current_room)
    count()


# Function to calculate player and enemy rolls in mini game Right Guess.
def right_guess_rolls():
    enemy_roll = random.randint(0, 10)
    return enemy_roll, enemy_roll if right_guess.counter % 3 == 0 else random.randint(0, 10)


# Function to display evaluation of player and enemy rolls in mini game Right Guess.
def show_right_guess_evaluate(inventory, u_inventory, usables_inventory, rooms, current_room):
    enemy_roll, player_roll = right_guess_rolls()
    show_mini_stats(player_roll, enemy_roll, rooms, current_room)
    show_room_win_message(inventory, rooms, current_room) if player_roll == enemy_roll else\
        show_room_lose_message(rooms, current_room)
    search_for_usable(u_inventory, usables_inventory)


# Function to play mini game Right Guess.
def right_guess(inventory, u_inventory, usables_inventory, rooms, current_room):
    right_guess.counter += 1
    show_room_story(rooms, current_room)
    show_game_objective(rooms, current_room)
    show_right_guess_evaluate(inventory, u_inventory, usables_inventory, rooms, current_room)
    count()


# Function to calculate player and enemy rolls in mini game Roll 1.
def roll_1_rolls():
    enemy_roll = list(range(0, 4))
    if roll_1.counter % 3 == 0:
        enemy_roll.remove(1)
    return 1 if roll_1.counter % 3 == 0 else random.randint(0, 4), random.choice(enemy_roll)


# Function to display evaluation of player and enemy rolls in mini game Roll 1.
def show_roll_1_evaluate(inventory, u_inventory, usables_inventory, rooms, current_room):
    player_roll, enemy_roll = roll_1_rolls()
    show_mini_stats(player_roll, enemy_roll, rooms, current_room)
    show_room_win_message(inventory, rooms, current_room) if player_roll == 1 and enemy_roll != 1 else\
        show_room_lose_message(rooms, current_room)
    search_for_usable(u_inventory, usables_inventory)


# Function to play mini game Roll 1.
def roll_1(inventory, u_inventory, usables_inventory, rooms, current_room):
    roll_1.counter += 1
    show_room_story(rooms, current_room)
    show_game_objective(rooms, current_room)
    show_roll_1_evaluate(inventory, u_inventory, usables_inventory, rooms, current_room)
    count()


# Function to calculate player and enemy rolls in mini game Roll 2.
def roll_2_rolls():
    enemy_roll = list(range(0, 4))
    if roll_2.counter % 3 == 0:
        enemy_roll.remove(2)
    return 2 if roll_2.counter % 3 == 0 else random.randint(0, 4), random.choice(enemy_roll)


# Function to display evaluation of player and enemy rolls in mini game Roll 2.
def show_roll_2_evaluate(inventory, u_inventory, usables_inventory, rooms, current_room):
    player_roll, enemy_roll = roll_2_rolls()
    show_mini_stats(player_roll, enemy_roll, rooms, current_room)
    show_room_win_message(inventory, rooms, current_room) if player_roll == 2 and enemy_roll != 2 else\
        show_room_lose_message(rooms, current_room)
    search_for_usable(u_inventory, usables_inventory)


# Function to play mini game Roll 2.
def roll_2(inventory, u_inventory, usables_inventory, rooms, current_room):
    roll_2.counter += 1
    show_room_story(rooms, current_room)
    show_game_objective(rooms, current_room)
    show_roll_2_evaluate(inventory, u_inventory, usables_inventory, rooms, current_room)
    count()


# Function to calculate player and enemy rolls in mini game Roll 3.
def roll_3_rolls():
    enemy_roll = list(range(0, 4))
    if roll_3.counter % 3 == 0:
        enemy_roll.remove(3)
    return 3 if roll_3.counter % 3 == 0 else random.randint(0, 4), random.choice(enemy_roll)


# Function to display evaluation of player and enemy rolls in mini game Roll 3.
def show_roll_3_evaluate(inventory, u_inventory, usables_inventory, rooms, current_room):
    player_roll, enemy_roll = roll_3_rolls()
    show_mini_stats(player_roll, enemy_roll, rooms, current_room)
    show_room_win_message(inventory, rooms, current_room) if player_roll == 3 and enemy_roll != 3 else\
        show_room_lose_message(rooms, current_room)
    search_for_usable(u_inventory, usables_inventory)


# Function to play mini game Roll 3.
def roll_3(inventory, u_inventory, usables_inventory, rooms, current_room):
    roll_3.counter += 1
    show_room_story(rooms, current_room)
    show_game_objective(rooms, current_room)
    show_roll_3_evaluate(inventory, u_inventory, usables_inventory, rooms, current_room)
    count()


# Function to calculate player and enemy rolls in mini game Rock Paper Scissors.
def rock_paper_scissors_rolls():
    player_roll = random.choice(['rock', 'paper', 'scissors'])
    enemy_roll = random.choice(['rock', 'paper', 'scissors'])
    if rock_paper_scissors.counter % 3 == 0:
        enemy_roll = 'rock' if player_roll == 'paper' else 'scissors'
        if player_roll == 'scissors':
            enemy_roll = 'paper'
    return player_roll, enemy_roll


# Function to display evaluation player and enemy hands in mini game Rock Paper Scissors. // CONSIDER hand = ["rock",
# "paper", "scissors"], hand_2 = hand, hand_2.append(hand_2.pop(0)), ... if hand_2.index(player_roll) =
# hand_1.index(enemy_roll)
def rock_paper_scissors_evaluate(inventory, u_inventory, usables_inventory, rooms, current_room):
    player_roll, enemy_roll = rock_paper_scissors_rolls()
    show_mini_stats(player_roll, enemy_roll, rooms, current_room)
    if player_roll == enemy_roll:
        print("\nIt's a draw")
    elif player_roll == 'rock' and enemy_roll == 'scissors' or player_roll == 'scissors' and enemy_roll == 'paper'\
            or player_roll == 'paper' and enemy_roll == 'rock':
        show_room_win_message(inventory, rooms, current_room) 
    else:     
        show_room_lose_message(rooms, current_room)
    search_for_usable(u_inventory, usables_inventory)


# Function to play mini game Rock Paper Scissors.
def rock_paper_scissors(inventory, u_inventory, usables_inventory, rooms, current_room):
    rock_paper_scissors.counter += 1
    show_room_story(rooms, current_room)
    show_game_objective(rooms, current_room)
    rock_paper_scissors_evaluate(inventory, u_inventory, usables_inventory, rooms, current_room)
    count()


# Function to capture directions.
def get_directions(rooms, current_room):
    return dict([(key, val) for key, val in rooms[current_room].items() if key not in ('Item', 'Game', 'Minion',
                                                                                       'Location')])


# Function to determine next room.
def determine_direction(rooms, current_room, user_cmd):
    return rooms[current_room][user_cmd[-1]]


# Function to determine alert.
def determine_alert(user_cmd, rooms, inventory):
    print_break()    
    if user_cmd[0] == 'Safe' and len(user_cmd) == 1:
        show_alert('Room', "The King\'s Chamber - Calig Crepundia is the {} room."
                  .format(rooms['King\'s Chamber - Calig Crepundia']['Location']))
    elif len(user_cmd) > 2:
        show_alert('Invalid Command', 'Command must not be longer than two words.')
    elif user_cmd[0] == 'Get' and user_cmd[-1] in inventory:
        show_alert('Inventory', f"{user_cmd[-1]} already in Inventory")  
    else:
        show_alert('Invalid Command',
                  f"Can't {user_cmd[0]}{' ' + user_cmd[-1] + '.' if user_cmd[-1] != user_cmd[0] else '.'}")


# Function to evaluate user commands.
def evaluate_user_cmd(user_cmd, rooms, current_room, inventory, u_inventory, usables_inventory):
    while len(user_cmd) == 0:
        show_room_status(current_room, inventory, rooms, usables_inventory)     
        user_cmd = get_user_cmd()       
        print_break()                
    if user_cmd[0] == 'Go' and user_cmd[-1] in get_directions(rooms, current_room) and len(user_cmd) == 2:
        current_room = determine_direction(rooms, current_room, user_cmd)
    elif current_room != 'Great Hall of Fallen Lights' and user_cmd[0] == 'Get' and user_cmd[-1] == \
            rooms[current_room]['Item'] and user_cmd[-1] not in inventory and len(user_cmd) == 2:
        globals()[rooms.get(current_room, {}).get('Game')](inventory, u_inventory, usables_inventory, rooms, current_room)  
    else:
        determine_alert(user_cmd, rooms, inventory)
    print_break()
    return current_room


# Function to run game // ADD while for RANDOM ROOM CHANGE,  room_randomize boolean or counter_list? -  see
# day_trip_generator.py, counters.
def main():
    times_rooms_randomized = 0
    show_instructions()

    while True:
        rooms, inventory, u_inventory, usables_inventory = set_up_game(times_rooms_randomized)
        current_room = 'Great Hall of Fallen Lights'

        while True:
            show_room_status(current_room, inventory, rooms, usables_inventory)
            exit_game(rooms, current_room, inventory)
            user_cmd = get_user_cmd()
            current_room = evaluate_user_cmd(user_cmd, rooms, current_room, inventory, u_inventory, usables_inventory)


count.counter, higher_number.counter, lower_number.counter, right_guess.counter = 0, 0, 0, 0
roll_1.counter, roll_2.counter, roll_3.counter, rock_paper_scissors.counter = 0, 0, 0, 0


# Execute program
if __name__ == "__main__":
    main()
