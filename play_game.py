#Project 7 Andrej Hromic
import json, time, os, random

start = time.time()
def main():
    # Returns a list containing the names of the entries in the directory given by path
    games_to_play = []
    for names in os.listdir():
        if names.endswith('.json'):
            games_to_play.append(names)
    
    print("JSON Games")
    for i in range(len(games_to_play)):
        print(i+1, "-", games_to_play[i][:-5])
    print("")
        
    game_choice = int(input("Select your game: ")) 
    
    if game_choice <= 0 or game_choice > len(games_to_play):
        print("Sorry, that game is not available")
        print("")
        print("")
        main()
   
    x = str(games_to_play[game_choice - 1])
    
    with open(x) as fp:
        game = json.load(fp)
    print("")
    print_instructions()
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    play(game)

def play(rooms):
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start'] 
    # The things the player has collected.
    stuff = ["Cell Phone; no signal or battery..."]
    # The rooms the player has visited
    visited = {}

    while True:
        print("")
        print("")
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        # Print the description.
        print(here["description"]) 
        # Prints any available items in the room...
        if len(here["items"]) >= 1:
            print("Items in room: ", *here["items"])
            
        # Black cat
        current_cat_room = random.choice(find_non_win_rooms(rooms))
        if current_cat_room == current_place:
            print("---There is a black cat in here---")
            
        # If you've visited a room before
        if current_place in visited:
            print("...You've been in this room before...")
        visited[current_place] = True
        
        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        usable_exits = find_usable_exits(here)
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()

        # If they type give, give the cat a treat when the user is in the same room with the cat
        if action == "give":
            if "Raw Fish..." not in stuff:
                if current_place != current_cat_room:
                    print("You have nothing to give.")
                    continue
                elif current_place == current_cat_room:
                    print("Poor kitty... you don't have a treat to give")
                    continue
            elif "Raw Fish..." in stuff:
                if current_place == current_cat_room:
                    print("Prrr...The cat loves the treat!")
                    stuff.remove("Raw Fish...")
                    continue
                else:
                    print("You have a treat...but there's no cat to give it to")
                    continue
       
        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit. Better luck next time!")
            break
     
        # If the user wants to see the instructions again
        if action == "help":
            print_instructions()
            continue

        # If they type "stuff", print any items they have (check the stuff list!)
        if action == "stuff":
            if len(stuff) == 0:
                print("You have nothing.")
            else: 
                print("Inventory:", *stuff)
            continue
        
        # If they type "take", grab any items in the room.
        if action == "take":
            if here["items"] == []:
                print("There is nothing here for you to take...")
            else:
                print("You picked up:", *here["items"])
                stuff.extend(here["items"])
                here["items"].clear()
            continue

        # If they type "drop", drop specifc item and attach it to current location
        if action == "drop":
            #if you don't have any items
            if len(stuff) == 0:
                print("You don't have any items...")
                continue
            
            #if you have items 
            print("Which item do you want to drop?")
            for i, item in enumerate(stuff): 
                print("  {}. {}".format(i+1, item))
                
            action = input("> ").lower().strip()
            
            try:
                index = int(action) - 1
                item = stuff.pop(index)
                print("You dropped:", item)
                here["items"].append(item)
            except:
                print("I don't understand '{}'...".format(action))
            continue
        
        # If they type "search" look through any exits in the room that might be hidden, and make them not hidden anymore!
        if action == "search":
            if here == rooms["basement"]:
                print("---You've discovered a hidden exit!---")
            else:
                print("Nothing here for you to search...")
            
            for exit in here['exits']:
                if exit.get("hidden", True):
                    exit["hidden"] = False
            continue      
        
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = usable_exits[num]
            if "Mansion Key..." not in stuff:
                if current_place == "crypt":
                    break
                if selected['destination'] == "outside":
                    print("You try to open the door, but it's locked!")
                    continue      
            current_place = selected['destination']
            print("...")
        except:
            print("I don't understand '{}'...".format(action))
        
    print("")
    print("")
    print("=== GAME OVER ===")
    end = time.time() - start
    print("Time:", time.strftime("%M:%S", time.gmtime(end)))

def find_usable_exits(room):
    usable = []
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue
        usable.append(exit)
    return usable

def find_non_win_rooms(game):
    keep = []
    for room_name in game.keys():
    # skip if it is the "fake" metadata room that has title & start
        if room_name == '__metadata__':
            continue
        # skip if it ends the game
        if game[room_name].get('ends_game', False):
            continue
        # keep everything else:
        keep.append(room_name)
    return keep
# output:
# ['entranceHall', 'basement', 'attic', 'attic2', 'balcony', 'kitchen',
# 'dumbwaiter', 'secretRoom', 'crypt', 'hallway0', 'hallway1', 'hallway2']
    
def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'help' to see the instructions again.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print(" - Type 'give' to give the cat a special treat if you have it.")
    print("=== Instructions ===")
    print("")
    

if __name__ == '__main__':
    main()
