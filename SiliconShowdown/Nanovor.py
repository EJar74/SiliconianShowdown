 
class Nanovor:
    
    def __init__(self, name, health, armor, speed, strength,  sv, family_class, attacks:list):
        #String defining the nanovor's name
        self._nano_name = name 
        
        #int, there are no decimals when it comes to dealing and taking damage
        self._nano_health = health
        
        #int, no decimals 
        self._nano_armor = armor
        
        #int, no decimals
        self._nano_speed = speed
        
        #int, no decimals
        self._nano_strength = strength
        
        #int, no decimals
        self._swarm_value = sv
        
        #String
        self._nano_class = family_class
        
        #a list of attack objects (attack has its own class)
        self._nano_attacks = attacks
        
        self._stun_length = 0
        
        self._is_buffed = False
        
        #Whether or not the Nanovor has been revealed
        self._revealed = False
        
        self._max_health = health
        
    #Accessor methods
    def get_name(self):
        return self._nano_name
    def get_health(self):
        return self._nano_health
    def get_armor(self):
        return self._nano_armor
    def get_speed(self):
        return self._nano_speed
    def get_strength(self):
        return self._nano_strength
    def get_sv(self):
        return self._swarm_value
    def get_class(self):
        return self._nano_class
    def get_attacks(self):
        return self._nano_attacks
    def check_stun_length(self):
        return self._stun_length
    def check_buffs(self):
        return self._is_buffed
    def check_reveal(self):
        return self._revealed
    def get_max_hp(self):
        return self._max_health
    
    #Mutator Methods
    
    #currently no nanovor in the game that can heal 
    def add_health(self):
        pass
    def remove_health(self, amount:int):
        # If the amount comes back negative, then that means the armor defended more than the actual attack did damage
        if amount >= 0:
            self._nano_health -=amount
    def add_armor(self, amount:int):
        self._nano_armor += amount
    def remove_armor(self, amount:int):
        self._nano_armor -= amount
        if self._nano_armor < 0:
            self._nano_armor = 0
    def add_speed(self, amount:int):
        self._nano_speed += amount
    def remove_speed(self, amount:int):
        self._nano_speed -= amount
        if self._nano_speed < 0:
            self._nano_speed = 0
    def add_strength(self, amount:int):
        self._nano_strength += amount
    def remove_strength(self, amount:int):
        self._nano_strength -= amount
        if self._nano_strength < 0:
            self._nano_strength = 0
    def change_length_stun(self, amount:int):
        self._stun_length += amount 
        if self._stun_length <= 0:
            self._stun_length = 0
    def change_buffed_status(self, new:bool):
        self._is_buffed = new
    def reveal(self):
        self._revealed = True
    # Display for information while in battle
    def display_stats(self):

        stats = f"\n{self._nano_name} ({self._nano_class})\nHP:  {self._nano_health}\nSTR:  {self._nano_strength}\nARM:  {self._nano_armor}\nSPD:  {self._nano_speed}\nSV:  {self._swarm_value}"
        if self._stun_length > 0:
            stats += f"\nStunned for: {self._stun_length} rounds."

        return stats 
