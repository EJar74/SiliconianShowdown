from Player import Player
import random
import math
import copy
import threading
from collections import OrderedDict, defaultdict
from AI import *


class OnlineGame:

    def __init__(self, maxPlayers, complete_list):
        #If lobby fills up, game closes, so no one else can join midway
        self.game_closed = False

        self.complete_list = complete_list

        self.rounds = 0

        self.max_players = maxPlayers
        # Dict, key is the client's connection, value is the clients username
        self.players = {}
        #Dicts containing each player's conn as keys, and the value is the Player object, containing the player's Swarm, player's name, etc.
        self.player_swarms = OrderedDict()
        #Player conn as keys, value is True or False depending on whether or not the players are connected.
        self.connected = {}

        self.game_over = False

        self.key_lock = threading.Lock()

        #Dict, one key will be a string with the entire round summary, and the other key will be a dict of the stats of all Nanovor on the field after the round
        #That inner dict will have a key that is the name of each player, and the value being the string with their nanovor's updated stats after the round
        #Names as keys might not actually work, in the event that multiple users have the same name. Maybe have index positions as keys? How would I get indexes though
        #Or maybe have a key called "Players", which holds list of 2-tuples, first element player's name, second their nanovors updated stats
        self.round_summary = {}

        #Counts how many players sent in their decisions for the round. Must be equal to the number of players in game. Increments by 1, resets to 0 when all info is received.
        self.player_info_received = 0

        self.round_over = False

    def add_player(self, player):
        with self.key_lock:
            self.players[player[0]] = player[1]
            self.connected[player[0]] = True

    def remove_player(self, player):
        #with self.key_lock:
        if player in self.players.keys():
            del self.players[player]
        if player in self.player_swarms.keys():
            del self.player_swarms[player]
        if player in self.connected.keys():
            del self.connected[player]

    def get_players(self):
        with self.key_lock:
            #Returning only the players' sockets
            return self.players

    def game_size(self):
        with self.key_lock:
            return self.max_players

    def full(self):
        with self.key_lock:
            if len(self.players) == self.max_players or self.game_closed:
                return True

    def set_swarm(self, player, swarm):
        with self.key_lock:
            swarm_tracker = []
            name_list = [nano.get_name() for nano in self.complete_list]
            for nano in swarm:
                i = name_list.index(nano)
                swarm_tracker.append(copy.deepcopy(self.complete_list[i]))
            self.player_swarms[player] = Player(self.players[player],swarm_tracker)

            #TODO Here we handle the case that the player chose to play single-player. If that's the case, assign a swarm to the AI.
            if self.max_players == 1:
                swarm_tracker = []
                chosen_swarm = pick_swarm()
                for vor in chosen_swarm:
                    j = name_list.index(vor)
                    swarm_tracker.append(copy.deepcopy(self.complete_list[j]))
                self.players["AI"] = "Spydran Agent"
                self.player_swarms["AI"] = Player("Spydran Agent", swarm_tracker)
                self.connected["AI"] = True

    def ready(self):
        #with self.key_lock:
        #Players are not added to the dict until after their swarm is set, if not all players have been added, game cannot start

        #TODO, creating another exception here for single-player matches
        if len(self.player_swarms) != self.max_players and self.max_players > 1:
            return False
        self.game_closed = True
        return True

    def gameOver(self,conn):
        if self.game_over:
            #TODO: added this to account for single-player
            if self.max_players == 1 and "AI" in self.players.keys():
                del self.players["AI"]
            if len(self.player_swarms_copy) == 0:
                return f"Game Over: DRAW!\n\nMatch Round Total: {self.rounds}"
            else:
                winner = list(self.player_swarms_copy.keys())[0]
                result = {"Results":"you Won! Congrats!" if conn == winner else f"you Lost! Better luck next time!\n\nWinner: {self.players_copy[winner]}"}
                result["Results"] += f"\n\nMatch Round Total: {self.rounds}"
                result.update({self.player_swarms_copy[winner].get_swarm().index(nanovor): nanovor.display_stats() for nanovor in self.player_swarms_copy[winner].get_swarm()})
                return result
        #If game isn't over, check if the client is even still in the game (they won't be if they aren't in the swarm dict, because they would've
        #been deleted during the round wrap up method execution)
        elif conn not in self.player_swarms.keys():
            del self.players[conn]
            return "You were eliminated!"
        #If not over, it'll return False (conditional branch didn't execute)
        return self.game_over

    #This function will return all data necessary for the players to make their roundly decisions. Data will be sent in form of strings,
    #Not class objects, because nothing will change while the players are deciding their next move (data changes in the server side every round,
    #and the updated data is sent back to each client at the end of each round).
    #What to return to each client: Their swarm, their current Nanovor, their override/EN, and the same for every other opponent
    def gameInformation(self, client):
        #Ensures only one client at a time can access this function, that way a data race doesn't occur and break the system
        with self.key_lock:
            #Accesses the player object to reduce the wording below
            player = self.player_swarms[client]

            #Player will not have a current nanovor if it is the first round or if their current Nanovor was splatted
            if player.get_current_nanovor() != '':
                active_nanovor = {"Stats": player.get_current_nanovor().display_stats() + (f"\nSwap Blocked for: {player.get_swap_block()} turn(s)." if player.get_swap_block() else ''),
                                "ActiveIDX":player.get_swarm().index(player.get_current_nanovor())}
            else:
                active_nanovor = {"Stats":'', "ActiveIDX":None}

            #Players swarm keys will be each Nanovors index position inside of the player's swarm list, and the values will be a string of that nanovor's current stats. Entire dict has info for entire swarm.
            #Key is always ordered; the client can just return the index of the nanovor that they chose to swap into, as their next active, etc
            #{Index:String, ...}
            player_swarm = {player.get_swarm().index(nanovor): nanovor.display_stats() for nanovor in player.get_swarm()}
            #Opponents is a list of Player objects
            opponents = [competitor for conn,competitor in self.player_swarms.items() if conn != client]
            #Dict containing the index of the opponent in the list of opponents as keys, then list with a string saying their name, and their active nano stats as elements
            #{Index: [String Username, String Active Nano Stats]}
            #Making the index key +1 because each individual client will be the 0 index, this will make iterating through the dict to make the interface much easier on the client side.
            opponent_active = {opponents.index(opponent) + 1: [opponent.get_name(), opponent.get_current_nanovor().display_stats() + (f"\nSwap Blocked for: {opponent.get_swap_block()} turn(s)." if opponent.get_swap_block() else '') if opponent.get_current_nanovor() != '' else "\n\n\nUnknown\n\n\n"] for opponent in opponents}

            #Contains strings of every attack possessed by every Nanovor in the clients Swarm, so they can access this info on their side easier with back buttons
            #Key is the Nanovors index position inside of the player's swarm, value is another dict, where the key there is the attack name with EN cost and damage, and value the attack description
            #{Index:{String AttackName: String AttackDesc}}
            player_attacks = defaultdict(list)
            for nano in player.get_swarm():
                for attack in nano.get_attacks():
                    player_attacks[player.get_swarm().index(nano)].append((f"{attack.get_name()}        {attack.get_cost()} EN{self.display_damage(nano, attack)}",attack.get_attack_summary()))

            #OP nested dict comprehension with values as a dict comprehension
            #player_attacks = {player.get_swarm().index(nano): [f"{attack.get_name()}       {attack.get_cost()} EN{self.display_damage(nano,attack)}", attack.get_attack_summary() for attack in nano.get_attacks()] for nano in player.get_swarm()}

            #{IDX:[Str AttackName..], stores index position of every nanovor in the player's swarm, and the names of the attacks that are pure overrides (empty if none).
            pure_overrides = {player.get_swarm().index(nano): [attack.get_name() for attack in nano.get_attacks() if attack.pure_override()] for nano in player.get_swarm()}
            #Dict of the EN and Overrides for each player, including the client. Client will be the first index, 0. All others will follow
            energy_override_info = {0: {"EN": player.get_energy(), "Override": self.decode_override(player.get_current_override()), "Pure": pure_overrides}}
            energy_override_info.update({opponents.index(opponent) + 1: {"EN": opponent.get_energy(), "Override": self.decode_override(opponent.get_current_override())} for opponent in opponents})

            #HP and name of every Nanovor in that opponent's swarm if the Nanovor has been revealed, else it is unknown. Player can always see their own swarm HP/names
            #The first element, 0, is actually the client requesting the information
            #The client can be grouped here into the same dictionary as the opponents rather than being added on the client side, because the client does not need to access
            #the HP summary and Name of the nanovor in their header beyond just having them displayed for viewing (they do however, access their own attacks and EN/Overrides)
            all_swarm_info = {0:[f"{nano.get_name()}\nHP: {nano.get_health()}/{nano.get_max_hp()}" for nano in player.get_swarm()]}

            #Again, making the index +1 here so that the client on their side can be index 0 and this dict is just added on to the end of that
            #Sorted here should send all the unknown Nanovor (so, all the "?") to the front, so that in the client side when they hover over, all the ? will be left-most.
            #This is for better visibility when the information pops out. Ex. If a ? is between two revealed Nanovor, it might be hard to hover over it since it would not expand much.
            all_swarm_info.update({opponents.index(opponent) + 1: sorted([f"{nano.get_name()}\nHP: {nano.get_health()}/{nano.get_max_hp()}" if nano.check_reveal() else "?" for nano in opponent.get_swarm()]) for opponent in opponents})

            #Dict with the keys being the index of the opponent in the opponent list and the value being a list of tuples with first element being the attack name and
            #the second element being the attack description for each attack their ACTIVE nanovor has. Plus 1 for keys for same reasons as above
            opponent_attack_info = defaultdict(list)
            for i,opponent in enumerate(opponents):
                if opponent.get_current_nanovor() != '':
                    for attack in opponent.get_current_nanovor().get_attacks():
                        if opponent.get_current_nanovor().check_reveal():
                            opponent_attack_info[i + 1].append((f"{attack.get_name()}        {attack.get_cost()} EN{self.display_damage(opponent.get_current_nanovor(), attack)}", attack.get_description()))
                        else:
                            opponent_attack_info[i + 1].append(("?", "?"))
                #If there is no active Nanovor (such as in the first round), give 3 artificial attacks to fill in the space.
                else:
                    opponent_attack_info[i + 1].extend([("?", "?"), ("?", "?"), ("?","?")])

            return {"Active Nanovor":active_nanovor, "Player Swarm":player_swarm, "Player Attacks":player_attacks, "Opponent Active":opponent_active,
                    "Energy & Overrides":energy_override_info, "All Swarms":all_swarm_info, "Opponent Attacks":opponent_attack_info}

    def decode_override(self, override):
        translation = []
        for type,info in override.items():
            if type == "SPIKE":
                if info == "Spike":
                    translation.append("Omni Spike")
                else:
                    translation.append(f"{info} Spike")
            elif type in "STR SPD ARM":
                translation.append(f"+{info} {type}")
            elif type == "DODGE":
                translation.append(f"Dodge: {info}% Chance")
            elif "EN" in type:
                if "HEX" in type:
                    translation.append(f"+{info} EN (Hexites)")
                elif "MAG" in type:
                    translation.append(f"+{info} EN (Magnamods)")
                else:
                    translation.append(f"+{info} EN (All Nanovor)")
        return ", ".join(translation)

    def display_damage(self, nanovor, attack):
        separator = "    |    "
        calculations = []
        STR_MULTIPLIER = nanovor.get_strength()/100

        if attack.get_damage():
            calculations.append("{} HP".format(self.round(attack.get_damage()[0] * STR_MULTIPLIER)))
            if len(attack.get_damage()) > 1:
                calculations.append("-{} HP".format(attack.get_damage()[1]))

        if attack.get_spike_combo():
            combos = attack.get_spike_combo().keys()
            if "DMGSET" in combos:
                calculations.append("{} HP*".format(self.round(attack.get_spike_combo()["DMGSET"] * STR_MULTIPLIER)))
            elif "DMGDOUBLE" in combos:
                calculations.append("{} HP*".format(self.round(attack.get_damage()[0] * 2 * STR_MULTIPLIER)))
            elif "PIERCE" in combos:
                if type(attack.get_spike_combo()["PIERCE"]) == dict:
                    if "PART" in attack.get_spike_combo()["PIERCE"]:
                        calculations.append("{} HP*".format(self.round(attack.get_damage()[0] * STR_MULTIPLIER) + self.round(attack.get_spike_combo()["PIERCE"]["PART"] * STR_MULTIPLIER)))

        if attack.get_special_condition():
            conditions = attack.get_special_condition().keys()
            if "DMG-CLASS" in conditions:
                if "Magnamod" in attack.get_special_condition()["DMG-CLASS"]:
                    calculations.append("{} HP*".format(self.round(attack.get_special_condition()["DMG-CLASS"]["Magnamod"] * STR_MULTIPLIER)))
            elif ">STR" in conditions:
                if "120" in attack.get_special_condition()[">STR"]:
                    if "DMGSET" in attack.get_special_condition()[">STR"]["120"]:
                        calculations.append("{} HP*".format(self.round(attack.get_special_condition()[">STR"]["120"]["DMGSET"] * STR_MULTIPLIER)))
            elif "CHANCE-DMG-50" in conditions:
                if "XTRANONPIERCE" in attack.get_special_condition()["CHANCE-DMG-50"]:
                    calculations.append("{} HP*".format(self.round(attack.get_special_condition()["CHANCE-DMG-50"]["XTRANONPIERCE"] * STR_MULTIPLIER)))
                elif "XTRAPIERCE" in attack.get_special_condition()["CHANCE-DMG-50"]:
                    calculations.append("{} HP*".format(self.round(attack.get_special_condition()["CHANCE-DMG-50"]["XTRAPIERCE"] * STR_MULTIPLIER)))

        return f"\n{separator.join(calculations)}" if calculations else ''

    def control_center(self, conn, decisions):
        #Prevents counter and other stuff from getting wonky if users send info at the same time
        with self.key_lock:
            #The first person continued from previous round summary, and sent in new info, so it's now a new round. Reset to false
            self.round_over = False
            #decisions = {"Active":self.active, "Next":self.next, "Attack":self.attack, "Target":self.target}
            #where active is the index of the active nano, next is the index of the next nano, attack is a string of the attack name, target is index of target in opponent list
            #player is a Player class object
            player = self.player_swarms[conn]
            player.set_current_nanovor(player.get_swarm()[decisions["Active"]])
            player.set_next_nanovor(player.get_swarm()[decisions["Next"]])

            #If opponent PASSED, set their attack to empty string, start_round will handle passing. Else, find the attack object and set that as active.
            for attack in player.get_current_nanovor().get_attacks():
                if attack.get_name() == decisions["Attack"]:
                    player.set_selected_attack(attack)
                    break
            else:
                player.set_selected_attack('')

            opponents = [competitor for sock,competitor in self.player_swarms.items() if sock != conn]
            # Subtract 1 because the curr_list contains the client at the beginning, whereas onlineBattle checks the opponents which excludes the client
            # So, opponents will always be 1 element shorter. So we subtract 1 to adjust for that.
            # Also check to see if there are even any opponents left (in the event all but 1 players quit), and that the target is not None (Pass or pure override).
            # If not, set the target to an empty string (won't be checked anyways).
            player.set_targets(opponents[decisions["Target"] - 1] if len(opponents) > 0 and decisions["Target"] is not None else '')
            self.player_info_received += 1

            #TODO this section is in the case of single-player matches. Once the player sends in their decision, simply make the decisions for the AI as well.
            if self.max_players == 1:
                computer = self.player_swarms["AI"]
                if computer.get_current_nanovor() == '' or computer.get_current_nanovor().get_health() <= 0:
                    computer.remove_swap_block(computer.get_swap_block())
                    computer.set_current_nanovor(computer.get_swarm()[0])

                computer.set_next_nanovor(computer.get_current_nanovor())
                computer.set_targets(player)
                matrix = fill_matrix(player, computer)
                move = [attack for attack in computer.get_current_nanovor().get_attacks()][decide(matrix)]
                computer.set_selected_attack(move)

            #TODO: added the OR exception so the round can get started in single-player. This is why I didn't want to make the AI here intiailly, so many small nuances.
            # Later on I'll have to optimize the code so that this isn't so annoying to deal with.
            if self.player_info_received == len(self.player_swarms) or self.max_players == 1:
                #Start the round, all info received, and reset the counter for next round. Also reset the summary from previous round
                self.round_summary = ''
                self.player_info_received = 0
                self.start_round()
                self.round_carnage_report()
            return

    def handle_quitters(self, conn=False):
        if conn and conn in self.connected.keys():
            self.connected[conn] = False
            self.control_center(conn, {"Active":0, "Next":0, "Attack":"PASS", "Target":1})
        else:
            for conn,on in self.connected.copy().items():
                if not on:
                    self.round_summary["Round Summary"] += f"\n{self.players[conn]} quit the game!"
                    self.remove_player(conn)

    def get_round_summary(self):
        if self.round_over:
            return self.round_summary
        return "Waiting"

    # BRING IN ALL THE FUNCTIONS THAT DO THE BEHIND-THE-SCENES WORK (LIKELY POST THEM AT THE VERY BOTTOM?)
    def start_round(self):
        # NOTE: THIS FUNCTION IS A COMBINATION OF START_ROUND AND SIMULATE_MOVE FROM THE COMBATRULES

        # Keep an eye on this, trying to figure out the issue of override buffs stacking multiple times
        # If the active nanovor has been buffed already, remove the buff so that it can be reapplied before the speed raffle and
        # Attack, that way buffs don't stack and a nanovor that hasn't received the buff won't get its stats depleted
        for homie in self.player_swarms.values():
            self.remove_override_buffs(homie)

        # Removed buffs from previous turn, Applying all buffs to all current nanovor before we even get to attack
        for plyr in self.player_swarms.values():
            self.apply_override_buffs(plyr)

        # After all players select their attacks, we determine who gets to go first, and if they can even attack, based on speed
        # and how much energy each player has
        pecking_order = self.determine_order(list(self.player_swarms.values()))

        # Round summary title, before the speed ranking is added
        self.round_summary += ("***** ROUND {} CARNAGE REPORT *****\n\n".format(self.rounds + 1))
        self.round_summary += "ORDER OF ATTACK\n"

        for i,homie in enumerate(pecking_order):
            # Set all the currently active nanovor to revealed, opponents can now see their stats
            homie.get_current_nanovor().reveal()

            # Instead of printing to the console, add to the self string variable to paste a text box message at the end of the round
            self.round_summary += (
                "({}) {}\'s {} ==> Speed: {} \n".format(i+1,homie.get_name(), homie.get_current_nanovor().get_name(),
                                               homie.get_current_nanovor().get_speed()))
        self.round_summary += "\nMOVES MADE\n"

        for player in pecking_order:
            # Check to see if player chose to attack or pass
            if player.get_selected_attack() != '':
                # Check if the player's current nanovor is even alive for the attack
                if player.get_current_nanovor().get_health() <= 0:
                    continue
                # Check if nanovor is stunned before attacking
                elif player.get_current_nanovor().check_stun_length() > 0:

                    self.round_summary += ("{}\'s {} is Stunned!\n".format(player.get_name(), player.get_current_nanovor().get_name()))

                    player.get_current_nanovor().change_length_stun(-1)

                    self.round_summary += ("Turns until stun wears off: {}\n".format(player.get_current_nanovor().check_stun_length()))
                # If player is missing energy for the attack, nanovor fizzled
                elif player.get_energy() < player.get_selected_attack().get_cost():
                    self.round_summary += ("{}\'s {} Fizzled!\n".format(player.get_name(), player.get_current_nanovor().get_name()))
                # If the player's nanovor is alive, isn't stunned, and player has enough energy for the attack, execute it.
                else:
                    self.play(player, player.get_targets())
                    # Remove energy for a successful attack
                    player.remove_energy(player.get_selected_attack().get_cost())
            # If their selected attack is empty, they chose to pass!
            else:
                if player.get_current_nanovor().get_health() > 0:
                    self.round_summary += ("{}\'s {} passed.\n".format(player.get_name(), player.get_current_nanovor().get_name()))
                    player.get_current_nanovor().change_length_stun(-1)

    # This function called for each players attack. Apply buffs to those involved, then remove them. When its the next player's turn,
    # those buffs, if active, will be applied again. This is to prevent buffs adding additional stats every round they are active.
    def play(self, attacker, defenders):
        # Call it once in the beginning to save us the heartache of calling it multiple times over and also to save a lot of space.
        attack = attacker.get_selected_attack()
        # If the attack is simply an override, then Dodge, target being splatted, and anything else does not matter! Set the override and skip the rest.
        if attack.pure_override():
            self.round_summary += f"{attacker.get_name()}\'s {attacker.get_current_nanovor().get_name()} used {attack.get_name()}!    ({self.decode_override(attack.get_override())} Override)\n"
            self.remove_override_buffs(attacker)
            attacker.set_override(attack.get_override())
            return

        # Check to see if the defender is already dead (in a  3+ player match, someone might've beat you to the punch)
        # If you were beaten to the punch, you are returned the energy that you would have spent
        # I returned the energy here because in the other function call in start_round, the function removes energy
        # regardless of whether or not the attack was successful. By adding it here, it offsets that reduction.
        if defenders.get_current_nanovor().get_health() <= 0:
            self.round_summary += ("{}\'s {} fizzled! It\'s target was already splatted!\n".format(attacker.get_name(),
                                                                                                    attacker.get_current_nanovor().get_name()))
            attacker.add_energy(attack.get_cost())
            return

        #Replace placeholder with the actual damage dealt later on.
        self.round_summary += (
            "{}\'s {} used {} on {}\'s {}! (DMGPLACEHOLDER)\n".format(attacker.get_name(), attacker.get_current_nanovor().get_name(),
                                                     attack.get_name(), defenders.get_name(),
                                                     defenders.get_current_nanovor().get_name()))

        # Check to see if the opponent has a dodge override active. If so, run it to see if the nanovor dodged.
        # If the nanovor successfully dodged, the opponent still loses the energy and override for the attack, but
        # The function will exit before any hacks or damage or spike combos are put in play against the defender
        if self.determine_dodge(defenders):
            # No damage was dealt, so replace the placeholder with empty string.
            self.round_summary = self.round_summary.replace("(DMGPLACEHOLDER)", '')
            self.round_summary += "{}\'s {} dodged the attack!\n".format(defenders.get_name(),defenders.get_current_nanovor().get_name())

            # Apply any overrides that come with the attack regardless of whether or not the defender dodged
            if attack.get_override():
                self.remove_override_buffs(attacker)
                attacker.set_override(attack.get_override())

            # effects to self still happen regardless if the attack landed on the defender
            self.apply_self_hacks(attacker)
            self.apply_self_spike_combos(attacker)

            if attack.get_consumes():
                if "SPIKE" in attacker.get_current_override().keys():
                    if attacker.get_current_override()["SPIKE"] in attack.get_description():
                        attacker.remove_override()

            # Applying recoil damage, even if defender dodged.
            if attack.get_damage():
                if len(attack.get_damage()) > 1:
                    attacker.get_current_nanovor().remove_health(attack.get_damage()[1])
                    if attacker.get_current_nanovor().get_health() <= 0:

                        self.round_summary += ("{}\'s {} splatted itself!\n".format(attacker.get_name(),
                                                                                     attacker.get_current_nanovor().get_name()))

                        attacker.remove_nanovor(attacker.get_current_nanovor())

            return

        attack_damage = 0
        recoil_damage = 0
        final_piercing = False
        extra_pierce_damage = 0
        STR_MULTIPLIER = attacker.get_current_nanovor().get_strength() / 100

        # Returns true if the attack does damage, returns False if nothing is returned. So, if this statement goes off, we know it does damage
        if attack.get_damage():
            attack_damage = attack.get_damage()[0]
            if len(attack.get_damage()) > 1:
                recoil_damage = attack.get_damage()[1]

        # Check special conditions, if any. If there are, apply them.
        special_conds = self.handle_special_conditions(attacker, defenders)
        if len(special_conds.keys()) > 0:
            for condition in special_conds.keys():
                if condition == "DMGSET":
                    attack_damage = special_conds[condition]
                elif condition == "PIERCE":
                    if special_conds[condition] == "ALL":
                        final_piercing = True
                #STRMULT will be False if it is a key, so set the multiplier to 1 (will have no effect on damage output).
                elif condition == "STRMULT":
                    STR_MULTIPLIER = 1

        set_up = self.apply_self_spike_combos(attacker)
        if len(set_up) > 0:
            for effect in set_up:
                # Checking for armor piercing effects
                if effect == "ALL":
                    final_piercing = True
                elif effect == "PART":
                    # Watch out for attacks that are armor piercing and have additional pierce damage
                    # NOTE: additional pierce damage is BASE DAMAGE, so you apply STR
                    extra_pierce_damage += attack.get_spike_combo()["PIERCE"]["PART"]
                    extra_pierce_damage = self.round(extra_pierce_damage * STR_MULTIPLIER)
                # Doubling damage if that is the effect
                elif effect == "DMGDOUBLE":
                    attack_damage *= 2
                # DmgSET, an int element lets me know that the effect is setting the damage
                elif type(effect) == int:
                    attack_damage = effect

        # Applying strength to the attack damage to get the total damage
        attack_damage = self.round(attack_damage * STR_MULTIPLIER)

        # Would have to apply armor piercing last. Damage would vary depending on the opponent's armor
        if attack.get_armorpiercing() or final_piercing:
            attack_damage += defenders.get_current_nanovor().get_armor()

        # Applying damage to the defender, while taking into account the armor of the defender, if any. Apply extra pierce damage afterwards, since it ignores armor
        defenders.get_current_nanovor().remove_health(attack_damage - defenders.get_current_nanovor().get_armor() + extra_pierce_damage)
        # Applying recoil damage
        attacker.get_current_nanovor().remove_health(recoil_damage)
        if recoil_damage > 0:
            self.round_summary += f"{attacker.get_name()}\'s {attacker.get_current_nanovor().get_name()} dealt {recoil_damage} damage to itself!\n"
        #Replacing placeholder with actual damage done.
        self.round_summary = self.round_summary.replace("(DMGPLACEHOLDER)", f"   (-{attack_damage - defenders.get_current_nanovor().get_armor() + extra_pierce_damage} HP)" if attack_damage > 0 else '')

        # Mostly applying battle kraken's hack zap
        self.handle_aoe_effects(attacker, list(self.player_swarms.values()))

        # Apply the hacks after dealing any damage
        self.apply_hacks(attacker, defenders)
        self.apply_self_hacks(attacker)

        # Apply effects from the combos onto enemy nanovor after dealing any damage
        self.apply_spike_combos(attacker, defenders)

        # Remove the override if it was consumes, after applying damage/effects/hacks
        if attack.get_consumes():
            if "SPIKE" in attacker.get_current_override().keys():
                if attacker.get_current_override()["SPIKE"] in attack.get_description():
                    attacker.remove_override()

        # Keep eye on this, may have to move it to after the attack damage is applied
        # This depends on if there are any attacks that set an override while ALSO dealing damage,
        # Without the need of a spike combo. This would only give issues if the current override is also a buff.
        if attack.get_override():
            # remove buffs so that the stats do not remain inflated if you place a different override.
            # apply override buffs so that newly placed overrides are taken into account when a player gets attacked on the same turn
            self.remove_override_buffs(attacker)
            attacker.set_override(attack.get_override())
            self.apply_override_buffs(attacker)

        # Checking if defender nanovor dies from the attack
        if defenders.get_current_nanovor().get_health() <= 0:
            self.round_summary += (
                "{}\'s {} splatted {}\'s {}!\n".format(attacker.get_name(), attacker.get_current_nanovor().get_name(),
                                                       defenders.get_name(),
                                                       defenders.get_current_nanovor().get_name()))

            defenders.remove_nanovor(defenders.get_current_nanovor())

        # Checking if attacking nanovor dies from recoil
        if attacker.get_current_nanovor().get_health() <= 0:

            self.round_summary += (
                "{}\'s {} splatted itself!\n".format(attacker.get_name(), attacker.get_current_nanovor().get_name()))

            attacker.remove_nanovor(attacker.get_current_nanovor())


    '''
    
    
       MAIN ENGINE FUNCTIONS THAT SUPPORT THE START_ROUND & PLAY FUNCTIONS, THESE FUNCTIONS DO ALL THE BEHIND-THE-SCENES WORK!
    
    
    '''


    # Made my own adaptation of the round function to solve rounding issues
    def round(self, num):
        if type(num) == float:
            if int("{:.2f}".format(num).split(".")[1]) >= 50:
                return math.ceil(num)
            else:
                return round(num)
        else:
            return num

    def apply_override_buffs(self, player):
        current = player.get_current_override()
        for nano in player.get_swarm():
            if not (nano.check_buffs()):
                if "STR" in current.keys():
                    nano.add_strength(current["STR"])
                    nano.change_buffed_status(True)
                if "ARM" in current.keys():
                    nano.add_armor(current["ARM"])
                    nano.change_buffed_status(True)
                if "SPD" in current.keys():
                    nano.add_speed(current["SPD"])
                    nano.change_buffed_status(True)

    def remove_override_buffs(self, player):
        current = player.get_current_override()
        for nano in player.get_swarm():
            if nano.check_buffs():
                if "STR" in current.keys():
                    nano.remove_strength(current["STR"])
                if "ARM" in current.keys():
                    nano.remove_armor(current["ARM"])
                if "SPD" in current.keys():
                    nano.remove_speed(current["SPD"])
                nano.change_buffed_status(False)

    def apply_energy_override(self, player):
        current = player.get_current_override()
        if "EN-ALL" in current.keys():
            player.add_energy(current["EN-ALL"])
        elif "EN-MAG" in current.keys():
            if player.get_current_nanovor().get_class() == "Magnamod":
                player.add_energy(current["EN-MAG"])
        elif "EN-VEL" in current.keys():
            if player.get_current_nanovor().get_class() == "Velocitron":
                player.add_energy(current["EN-VEL"])
        elif "EN-HEX" in current.keys():
            if player.get_current_nanovor().get_class() == "Hexite":
                player.add_energy(current["EN-HEX"])

    def determine_dodge(self, player):
        current = player.get_current_override()
        if "DODGE" in current.keys():
            luck = random.randint(1, 100)
            if luck % (100 // current["DODGE"]) == 0:
                return True
            return False

    def determine_order(self, player_list):
        order = []
        copy_list = player_list[:]

        # This loop removes the next player in line from the copy list until there is a single player left: the one who goes last.
        # As a result, total_speed decreases each time, because a player was removed.
        while len(order) != len(player_list):
            total_speed = sum([player.get_current_nanovor().get_speed() for player in copy_list])

            # Handles scenario where all active nanovor combined have 0 speed, randomly chooses which one goes next
            if total_speed == 0:
                next_in_line = random.randint(0, len(copy_list) - 1)
                order.append(copy_list[next_in_line])
                copy_list.pop(next_in_line)
                continue

            player_odds = {}
            odds_range = {}

            for player in copy_list:
                player_odds[player] = player.get_current_nanovor().get_speed() / total_speed * 100

            current = 1
            for player, odds in player_odds.items():

                # new way I'm testing, just simply using the odds themselves. Hesitated at first because rounding could result in total odds > 100
                odds_range[player] = [current, current + odds]
                current += odds

            # Note: Used to be 1 to total_speed. Changed to 100 bc it's standardized.
            # Idea: change it to current, to account for the 101's
            # determine = random.randint(1,current)
            determine = random.uniform(1, 100)

            for player, odds in odds_range.items():

                if odds[0] <= determine < odds[1]:
                    order.append(player)
                    copy_list.remove(player)

        return order

    # Apply hack effects to the defender(s)
    def apply_hacks(self, attacker, defenders):
        attack = attacker.get_selected_attack()

        # All Hacks: Stun, Swap Block, Obliterate
        if attack.get_hack():
            for hack in attack.get_hack().keys():
                if hack == "SWAP":
                    defenders.add_swap_block(attack.get_hack()[hack])
                    # Don't need to set defenders next Nanovor to the current one, command center simply doesn't swap, skips to attack selection.
                    # Sets the defenders most recent hack to Swap
                    defenders.set_recent_hack("SWAP")
                    self.round_summary += f"{defenders.get_name()} is swap-blocked! Blocked for the next {defenders.get_swap_block()} turn(s)!\n"
                elif hack == "OBLIT":
                    self.remove_override_buffs(defenders)
                    defenders.remove_override()
                    self.round_summary += f"{defenders.get_name()}\'s Override was erased!\n"
                elif hack == "STUN":
                    defenders.get_current_nanovor().change_length_stun(attack.get_hack()[hack])
                    defenders.set_recent_hack("STUN")
                    self.round_summary += f"{defenders.get_name()}\'s {defenders.get_current_nanovor().get_name()} got stunned!\n"
                elif hack == "ENSAP":
                    defenders.remove_energy(attack.get_hack()[hack])
                    self.round_summary += f"{defenders.get_name()} lost {attack.get_hack()[hack]} EN!\n"
                elif hack == "STR":
                    defenders.get_current_nanovor().remove_strength(attack.get_hack()[hack])
                    self.round_summary += f"-{attack.get_hack()[hack]} STR for {defenders.get_name()}\'s {defenders.get_current_nanovor().get_name()}!\n"
                elif hack == "SPD":
                    defenders.get_current_nanovor().remove_speed(attack.get_hack()[hack])
                    self.round_summary += f"-{attack.get_hack()[hack]} SPD for {defenders.get_name()}\'s {defenders.get_current_nanovor().get_name()}!\n"
                elif hack == "ARM":
                    defenders.get_current_nanovor().remove_armor(attack.get_hack()[hack])
                    self.round_summary += f"-{attack.get_hack()[hack]} ARM for {defenders.get_name()}\'s {defenders.get_current_nanovor().get_name()}!\n"

    # Apply hack effects to the attacker, if any.
    def apply_self_hacks(self, attacker):
        attack = attacker.get_selected_attack()

        if attack.get_hack():
            for hack in attack.get_hack().keys():
                if hack == "SELFSTUN":
                    attacker.get_current_nanovor().change_length_stun(attack.get_hack()[hack])
                    attacker.set_recent_hack("STUN")
                    self.round_summary += f"{attacker.get_name()}\'s {attacker.get_current_nanovor().get_name()} stunned itself!\n"
                elif hack == "DECSELFSTR":
                    attacker.get_current_nanovor().remove_strength(attack.get_hack()[hack])
                    self.round_summary += f"-{attack.get_hack()[hack]} STR for {attacker.get_name()}\'s {attacker.get_current_nanovor().get_name()}!\n"
                elif hack == "DECSELFSPD":
                    attacker.get_current_nanovor().remove_speed(attack.get_hack()[hack])
                    self.round_summary += f"-{attack.get_hack()[hack]} SPD for {attacker.get_name()}\'s {attacker.get_current_nanovor().get_name()}!\n"
                elif hack == "DECSELFARM":
                    attacker.get_current_nanovor().remove_armor(attack.get_hack()[hack])
                    self.round_summary += f"-{attack.get_hack()[hack]} ARM for {attacker.get_name()}\'s {attacker.get_current_nanovor().get_name()}!\n"
                elif hack == "INCSELFSTR":
                    attacker.get_current_nanovor().add_strength(attack.get_hack()[hack])
                    self.round_summary += f"+{attack.get_hack()[hack]} STR for {attacker.get_name()}\'s {attacker.get_current_nanovor().get_name()}!\n"
                elif hack == "INCSELFSPD":
                    attacker.get_current_nanovor().add_speed(attack.get_hack()[hack])
                    self.round_summary += f"+{attack.get_hack()[hack]} SPD for {attacker.get_name()}\'s {attacker.get_current_nanovor().get_name()}!\n"
                elif hack == "INCSELFARM":
                    attacker.get_current_nanovor().add_armor(attack.get_hack()[hack])
                    self.round_summary += f"+{attack.get_hack()[hack]} ARM for {attacker.get_name()}\'s {attacker.get_current_nanovor().get_name()}!\n"

    # Apply Spike Combo effects to the defender(s)
    def apply_spike_combos(self, attacker, defenders):
        attack = attacker.get_selected_attack()

        # So many different spike combos, this is going to look terrible if done with nothing but if statements, but that may be the only way
        # So Far: DMGDOUBLE, DMGSET, PIERCE (either all or part), SETNEW
        if attack.get_spike_combo():
            if "SPIKE" in attacker.get_current_override().keys():
                if attacker.get_current_override()["SPIKE"] in attack.get_description():
                    for effect in attack.get_spike_combo().keys():
                        if effect == "SWAP":
                            # change this later to include all defenders (though currently only 1 AOE attack exists) Need for loop. Maybe add above
                            defenders.add_swap_block(attack.get_spike_combo()[effect])
                            # Don't need to set defenders next Nanovor to the current one, command center simply doesn't swap, skips to attack selection.
                            # Set the defenders recent hack to Swap
                            defenders.set_recent_hack("SWAP")
                            self.round_summary += "{} is swap-blocked! Blocked for the next {} turn(s)!\n".format(
                                defenders.get_name(), defenders.get_swap_block())

                        elif effect == "OBLIT":
                            self.remove_override_buffs(defenders)
                            defenders.remove_override()
                            self.round_summary += f"{defenders.get_name()}\'s Override was erased!\n"
                        elif effect == "STUN":
                            defenders.get_current_nanovor().change_length_stun(attack.get_spike_combo()[effect])
                            defenders.set_recent_hack("STUN")
                            self.round_summary += f"{defenders.get_name()}\'s {defenders.get_current_nanovor().get_name()} got stunned!\n"
                        elif effect == "ENSAP":
                            defenders.remove_energy(attack.get_spike_combo()[effect])
                            self.round_summary += f"{defenders.get_name()} lost {attack.get_spike_combo()[effect]} EN!\n"
                        elif effect == "STR":
                            defenders.get_current_nanovor().remove_strength(attack.get_spike_combo()[effect])
                            self.round_summary += f"-{attack.get_spike_combo()[effect]} STR for {defenders.get_name()}\'s {defenders.get_current_nanovor().get_name()}!\n"
                        elif effect == "SPD":
                            defenders.get_current_nanovor().remove_speed(attack.get_spike_combo()[effect])
                            self.round_summary += f"-{attack.get_spike_combo()[effect]} SPD for {defenders.get_name()}\'s {defenders.get_current_nanovor().get_name()}!\n"
                        elif effect == "ARM":
                            defenders.get_current_nanovor().remove_armor(attack.get_spike_combo()[effect])
                            self.round_summary += f"-{attack.get_spike_combo()[effect]} ARM for {defenders.get_name()}\'s {defenders.get_current_nanovor().get_name()}!\n"

                        # Maybe should be in self_spike_combos, but the order of functions in play would make
                        # it so that a STR increase or decrease is applied BEFORE the attack damage is calculated.
                        # Leaving these here for now to prevent errors. If I rearrange the play function later,
                        # Which I certainly will, I will move these where they should be.
                        elif effect == "DECSELFSTR":
                            attacker.get_current_nanovor().remove_strength(attack.get_spike_combo()[effect])
                            self.round_summary += f"-{attack.get_spike_combo()[effect]} STR for {attacker.get_name()}\'s {attacker.get_current_nanovor().get_name()}!\n"
                        elif effect == "DECSELFSPD":
                            attacker.get_current_nanovor().remove_speed(attack.get_spike_combo()[effect])
                            self.round_summary += f"-{attack.get_spike_combo()[effect]} SPD for {attacker.get_name()}\'s {attacker.get_current_nanovor().get_name()}!\n"
                        elif effect == "DECSELFARM":
                            attacker.get_current_nanovor().remove_armor(attack.get_spike_combo()[effect])
                            self.round_summary += f"-{attack.get_spike_combo()[effect]} ARM for {attacker.get_name()}\'s {attacker.get_current_nanovor().get_name()}!\n"
                        elif effect == "INCSELFSTR":
                            attacker.get_current_nanovor().add_strength(attack.get_spike_combo()[effect])
                            self.round_summary += f"+{attack.get_spike_combo()[effect]} STR for {attacker.get_name()}\'s {attacker.get_current_nanovor().get_name()}!\n"
                        elif effect == "INCSELFSPD":
                            attacker.get_current_nanovor().add_speed(attack.get_spike_combo()[effect])
                            self.round_summary += f"+{attack.get_spike_combo()[effect]} SPD for {attacker.get_name()}\'s {attacker.get_current_nanovor().get_name()}!\n"
                        elif effect == "INCSELFARM":
                            attacker.get_current_nanovor().add_armor(attack.get_spike_combo()[effect])
                            self.round_summary += f"+{attack.get_spike_combo()[effect]} ARM for {attacker.get_name()}\'s {attacker.get_current_nanovor().get_name()}!\n"

    # Apply spike combo effects to the attacker, if any.
    def apply_self_spike_combos(self, attacker):

        attack = attacker.get_selected_attack()

        deliverable = []

        if attack.get_spike_combo():
            if "SPIKE" in attacker.get_current_override().keys():
                if attacker.get_current_override()["SPIKE"] in attack.get_description():
                    for effect in attack.get_spike_combo().keys():
                        if effect == "SELFSTUN":
                            attacker.get_current_nanovor().change_length_stun(attack.get_spike_combo()[effect])
                            attacker.set_recent_hack("STUN")
                            self.round_summary += f"{attacker.get_name()}\'s {attacker.get_current_nanovor().get_name()} stunned itself!\n"
                        elif effect == "SETNEW":
                            self.remove_override_buffs(attacker)
                            attacker.remove_override()
                            attacker.set_override(attack.get_spike_combo()[effect])
                        elif effect == "ENADD":
                            attacker.add_energy(attack.get_spike_combo()[effect])
                            self.round_summary += f"{attacker.get_name()} gained {attack.get_spike_combo()[effect]} EN!\n"
                        elif effect == "PIERCE":
                            if type(attack.get_spike_combo()[effect]) == dict:
                                deliverable.append("PART")
                            else:
                                # If its not Partial Pierce, it's fully piercing
                                deliverable.append(attack.get_spike_combo()[effect])
                        elif effect == "DMGDOUBLE":
                            deliverable.append("DMGDOUBLE")
                        elif effect == "DMGSET":
                            deliverable.append(attack.get_spike_combo()[effect])

        return deliverable

    def handle_special_conditions(self, attacker, defenders):
        attack = attacker.get_selected_attack()

        if attack.get_special_condition():
            for condition in attack.get_special_condition().keys():
                for details in attack.get_special_condition()[condition].keys():
                    if condition == "DMG-CLASS":
                        if details == defenders.get_current_nanovor().get_class():
                            return {"DMGSET": attack.get_special_condition()[condition][details]}

                    elif condition == "PIERCE-CLASS":
                        if details == defenders.get_current_nanovor().get_class():
                            return {"PIERCE": attack.get_special_condition()[condition][details]}

                    # Experimental, this is for attacks that do damage based on enemy energy
                    # The condition would look like this: {{"EN-DMG":{"PIERCE":10}} with 10 being the multiplier per energy
                    # Send in the STRMULT key to let the play function know NOT to apply the STR multiplier to this damage (it is straight-damage).
                    elif condition == "EN-DMG":
                        if details == "PIERCE":
                            return {"DMGSET":attack.get_special_condition()[condition][details] * defenders.get_energy(), "PIERCE":"ALL", "STRMULT":False}
                    # Experimental, if the defenders speed is below a certain threshold,
                    # apply the effect. If it's pierce all, return it as a dict to play function.
                    # Used only for Giga Siren's Incinerate Attack
                    elif condition == "<SPD":
                        if defenders.get_current_nanovor().get_speed() < int(details):
                            if attack.get_special_condition()[condition][details] == "PIERCEALL":
                                return {"PIERCE": "ALL"}
                    # Experimental, used for Phase Spiker's Flying Fang
                    elif condition == ">STR":
                        if defenders.get_current_nanovor().get_strength() > int(details):
                            if "DMGSET" in attack.get_special_condition()[condition][details].keys():
                                return {"DMGSET": attack.get_special_condition()[condition][details]["DMGSET"]}

                    # Experimental, tackles the attacks that have 50% chance of doing x amount of damage, or more x amount.
                    # Looks like: {"CHANCE-DMG-50": {"PIERCE":100}} with 100 being the damage it can do.
                    elif condition == "CHANCE-DMG-50":
                        risk = random.randint(1, 100)
                        self.round_summary = self.round_summary.replace("(DMGPLACEHOLDER)", '')
                        if risk > 50:
                            self.round_summary += "{} was successful!   (DMGPLACEHOLDER)\n".format(attack.get_name())
                            if details == "PIERCE":
                                # If piercing,remove health w/out taking into account enemy armor. This is for fixed damage. (Ie, Plasma Lash 3.0 Solid Strike).
                                return {"DMGSET": attack.get_special_condition()[condition][details], "PIERCE":"ALL", "STRMULT":False}
                            elif details == "XTRANONPIERCE":
                                # Thunderpoid 3.0, chance of doing double damage, or regular damage. Also used for Spike Hornet's Wisecrack
                                return {"DMGSET": attack.get_special_condition()[condition][details]}
                            elif details == "XTRAPIERCE":
                                # Cyber Slicer 1.0, chance of doing 30 base damage, or 50 BASE damage that IGNORES armor
                                return {"DMGSET": attack.get_special_condition()[condition][details], "PIERCE": "ALL"}
                            '''
                            elif details == "NONPIERCE":
                                # If non-piercing, subtract opponent armor from damage output. This is for fixed damage, though there isn't an attack like this yet
                                defenders.get_current_nanovor().remove_health(attack.get_special_condition()[condition][details] - defenders.get_current_nanovor().get_armor())
                            '''
                        else:
                            self.round_summary += "{} failed!   (DMGPLACEHOLDER)\n".format(attack.get_name())
        return {}

    def handle_aoe_effects(self, attacker, player_list):
        # Keep an eye here, it is applying aoe effects to all players before attacking.
        # Does not include any damage or stat decrease which is handled later
        if attacker.get_selected_attack().get_aoe_effect():
            # If clearhacks isn't even in the aoe effect, the second part doesn't even go off because of python's and rule, where if the left statement is false,
            # the right side of the statement isn't even checked. Short-circuit eval.
            if "CLEARHACKS" in attacker.get_selected_attack().get_aoe_effect().keys() and (
                    attacker.get_selected_attack().get_aoe_effect()["CLEARHACKS"] == "RECENT"):
                for homie in player_list:
                    for nanovor in homie.get_swarm():
                        if nanovor != homie.get_current_nanovor():
                            nanovor.change_length_stun(nanovor.check_stun_length() * -1)
                        else:
                            if homie.get_recent_hack() == "SWAP":
                                homie.remove_swap_block(homie.get_swap_block())
                            elif homie.get_recent_hack() == "STUN":
                                homie.get_current_nanovor().change_length_stun(
                                    homie.get_current_nanovor().check_stun_length() * -1)
                self.round_summary += "Most recent Stun or Swap condition removed from all Nanovor in all Swarms!\n"


    '''
    
    
     MAIN ENGINE FUNCTIONS END HERE
    
    
    '''


    # Displays a summary of everything that happened the previous round on the screen so users can keep track of the events.
    def round_carnage_report(self):

        self.round_summary += "\nSWAPS MADE\n"

        for plyr in list(self.player_swarms.values()):
            # Present the Nanovor that were switched in on the Carnage Report, if any switched in. Also note if someone tried to switch but was swap blocked
            if plyr.get_swap_block() == 0 and plyr.get_current_nanovor().get_health() > 0:
                if plyr.get_next_nanovor() != plyr.get_current_nanovor():
                    self.round_summary += "{} swapped out their {} & swapped in their {}!\n".format(plyr.get_name(),
                                                                                                     plyr.get_current_nanovor().get_name(),
                                                                                                     plyr.get_next_nanovor().get_name())
            else:
                if plyr.get_current_nanovor().get_health() > 0 and (
                        plyr.get_next_nanovor() != plyr.get_current_nanovor()):
                    self.round_summary += "{} tried to swap out their {}, but was swap-blocked!\n".format(plyr.get_name(), plyr.get_current_nanovor().get_name())

        # Apply Buffs as soon as turn is over so the players can notice the immediate effects and not be confused as to why buffs weren't applied
        # These buffs are later removed before the round starts. Then, they are added back again (prevents buffs from stacking when they shouldn't)
        # apply buffs is called twice in a row, BUT, the function checks to see if the nanos are already buffed, which also prevents multiple stacking
        for plyr in list(self.player_swarms.values()):
            self.apply_override_buffs(plyr)

        #Turn the entire string into a value in a dict, so that you can add the player's resulting active nanovor stats in another key
        self.round_summary = {"Round Summary":self.round_summary, "Players":[]}

        for conn, plyr in self.player_swarms.items():
            curr_vor = plyr.get_current_nanovor().display_stats()
            if plyr.get_swap_block() > 0:
                curr_vor += "\nSwap Blocked for: {} turn(s).".format(plyr.get_swap_block())

            #Adds 2-tuple to list, 1st elemnt being the username, 2nd the stats
            self.round_summary["Players"].append((f"{self.players[conn]}\'s Nanovor", curr_vor))

        self.round_wrapup()


    def round_wrapup(self):
        self.rounds += 1

        players_alive = self.player_swarms.copy()

        for conn,player in players_alive.items():
            # If a player is eliminated (ie, no remaining nanovor)
            if len(player.get_swarm()) == 0:
                if player in self.player_swarms.values():
                    del self.player_swarms[conn]
                    self.round_summary["Round Summary"] += f"\n{player.get_name()} was eliminated!"

        #Remove players who left the game, the consequent if statement then checks to see if that leaves the game with 1 player
        #If so, game will be over. Otherwise, game will continue, just without that additional player. Think this also erases the
        #need for an after-screen message telling the remaining player that their opponent quit (instead, it will be in the Caranage Report)
        self.handle_quitters()

        if len(self.player_swarms) <= 1:
            #Make a copy so that players can access the final screen at their own pace and game can be erased from games w/out worry
            self.players_copy = self.players.copy()
            self.player_swarms_copy = self.player_swarms.copy()

            #Set to True to deliver the final Carnage Report
            self.round_over = True
            self.game_over = True

        else:
            # Before anyone gets to swap or choose their next nanovor, the energy and energy overrides must be applied.
            for conn,player in players_alive.items():
                player.add_energy(2)
                self.apply_energy_override(player)

                # If the player isn't swap blocked and if their nanovor isn't dead (meaning they wont be redirected to a new nanovor selection), then swap their nanovor.
                # If either of these is False, the following loop will handle both of those cases.
                if player.get_swap_block() == 0 and player.get_current_nanovor().get_health() > 0:
                    player.set_current_nanovor(player.get_next_nanovor())
                    # Reveal the new active nanovor so the opponents can see its attacks and stats
                    player.get_current_nanovor().reveal()

                # Remove a swap block turn from everyone AFTER checking to see if they had any blocks. If they didn't, the function is set so that negative blocks don't exist
                player.remove_swap_block(1)

                # If a player's nanovor died, allow them to choose a new one
                if player.get_current_nanovor().get_health() <= 0:

                    # If the active nanovor died, remove any swap block hacks active on the player so that they do not carry over.
                    player.remove_swap_block(player.get_swap_block())

                    #If the active nanovor died, set the player's nanovor to an empty string, so that the client side knows
                    #whether or not it needs to prompt the user to select a new active nanovor
                    player.set_current_nanovor('')

            self.round_over = True
