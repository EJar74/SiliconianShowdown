
class Player:
    
    def __init__(self, name, swarm:list):
        
        self._player_name = name
        
        # List of Nanovor (class objects), each nanovor has its set of attacks (also class objects)
        self._player_swarm = swarm
        
        #Selects nanovor after match begins
        self._current_nanovor = ''
        
        #The next nanovor in line if player chooses to swap
        self._next_nanovor = ''
        
        #Starts the match with 2 energy
        self._current_energy = 2
        
        #Starts match with no override
        self._current_override = {}
        
        #Starts match without being swap blocked (blocked for 0 turns)
        self._swap_block = 0
        
        #Updates each round depending on what each player chooses to do 
        self._selected_attack = ''
        
        # Who the player is going to attack in the coming round
        self._enemy_targets = ''
        
        #Keeps track of which hack to self was more recent: Stun or Swap-Block
        self._recent_hack = ''
        
    #Accessor Methods
    def get_name(self):
        return self._player_name
    def get_swarm(self):
        return self._player_swarm
    def get_current_nanovor(self):
        return self._current_nanovor
    def get_next_nanovor(self):
        return self._next_nanovor
    def get_energy(self):
        return self._current_energy
    def get_current_override(self):
        return self._current_override
    def get_swap_block(self):
        return self._swap_block
    def get_selected_attack(self):
        return self._selected_attack
    def get_targets(self):
        return self._enemy_targets
    def get_recent_hack(self):
        return self._recent_hack
        
    #Mutator Methods
    def set_current_nanovor(self, nanovor):
        self._current_nanovor = nanovor
    def set_next_nanovor(self, nanovor):
        self._next_nanovor = nanovor
    def add_energy(self, amount:int):
        self._current_energy += amount
    def remove_energy(self, amount:int):
        self._current_energy -= amount
        if self._current_energy < 0:
            self._current_energy = 0
    def set_override(self, override):
        self._current_override = override
    def remove_override(self):
        self._current_override = {}
    def add_swap_block(self, amount:int):
        self._swap_block += amount
    def remove_swap_block(self, amount:int):
        self._swap_block -= amount
        if self._swap_block < 0:
            self._swap_block = 0
    def set_selected_attack(self, attack):
        self._selected_attack = attack
    def set_targets(self, enemies):
        self._enemy_targets = enemies
    def add_nanovor(self,nanovor):
        self._player_swarm.append(nanovor)
    def remove_nanovor(self, nanovor):
        if nanovor in self._player_swarm:
            self._player_swarm.remove(nanovor)
    def set_recent_hack(self, hack):
        self._recent_hack = hack
    
    # Other
    def display_swarm(self):
        display = ''
        for nano in self._player_swarm:
            display += (nano.display_stats()+"\n")
        return display
