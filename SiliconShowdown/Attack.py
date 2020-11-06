
class Attack:
    def __init__(self, name, cost:int, description, damage=[False], hack=[False], override=[False], combo=[False], consumes=False, armorpiercing=False, special_condition = [False], aoe_effect = [False]):
        #String with the attack name
        self._attack_name = name
        
        #int with the energy cost
        self._energy_cost = cost
        
        #Describes the attack and all its possibilities 
        self._attack_description = description
        
        #list with either 1 or 2 elements. 1 = [false] if not a damage attack; 2 elements = [true, [damage to enemy, damage to self]]
        self._damage = damage
        
        #list w either 1 or 2 elements. 1 = [false]; 2 = [true, {HackName:duration->int, ...}]
        self._creates_hack = hack
        
        #list w either 1 or 2 elements. 1 = [false]; 2 = [true, {OverrideType:amount->int}]
        self._creates_override = override
        
        #list w either 1 or 2 elements. 1 = [false]; 2 = [true, {EffectName:amount ->int, ...}]
        self._spike_combo = combo
        
        #boolean, either true or false
        self._consumes_spike = consumes
        
        #Whether or not the attack ignores armor
        self._armor_piercing = armorpiercing
        
        #Whether or not the attack holds a special condition, [True, {"CONDITION":{"CONDITIONTYPE":int}}]
        self._special_condition = special_condition
        
        #Check if the attack has anything effects that affect all players
        #Made because of Battle Kraken's Hack Zap, smh.
        self._aoe_effect = aoe_effect

        #Checks if the attack only sets an override, and does not have any additional effects (ex. Spikes, ARM boost, SPD boost, Dodge).
        self._pure_override = True if (not self._damage[0] and not self._creates_hack[0] and not self._spike_combo[0] and not self._consumes_spike and not self._special_condition[0] and not self._aoe_effect[0]) else False
    
    # Accessor Methods
    def get_name(self):
        return self._attack_name
    def get_cost(self):
        return self._energy_cost
    def get_description(self):
        return self._attack_description
    def get_damage(self):
        if self._damage[0]:
            return self._damage[1]
    def get_hack(self):
        if self._creates_hack[0]:
            return self._creates_hack[1]
    def get_override(self):
        if self._creates_override[0]:
            return self._creates_override[1]
    def get_spike_combo(self):
        if self._spike_combo[0]:
            return self._spike_combo[1]
    def get_consumes(self):
        return self._consumes_spike
    def get_armorpiercing(self):
        return self._armor_piercing
    def get_special_condition(self):
        if self._special_condition[0]:
            return self._special_condition[1]
    def get_aoe_effect(self):
        if self._aoe_effect[0]:
            return self._aoe_effect[1]
    def pure_override(self):
        return self._pure_override
        
    # Prints out Attack Details
    def get_attack_summary(self):

        return self._attack_description
