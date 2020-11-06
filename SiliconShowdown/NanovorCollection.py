from NanovorClass import Nanovor
from AttackClass import Attack
from PlayerClass import Player

#Nanovor: (self, name, health, armor, speed, strength,  sv, family_class, attacks:list)
#Attacks: (self, name, cost:int, description, damage=[False], hack=[False], override=[False], combo=[False], consumes=False, armorpiercing=False)

#ATTACKS
electro_shock = Attack("Electroshock", 1, "A ranged electric damage attack", damage=[True, [30]])
armor_up = Attack("Armor Up", 3, "This Nanovor places a +5 Armor Override", override = [True, {"ARM":5}])
red_spike = Attack("Red Spike", 1, "This Nanovor places an Override that allows your swarm to make a Red Spiked attack.", override = [True, {"SPIKE":"Red"}])

powerball = Attack("Powerball", 2, "A damage attack; with a Red Spike override, the attack deals double damage.", damage = [True, [35]], combo = [True, {"DMGDOUBLE":2}], consumes = True)
obliterate = Attack("Obliterate", 2, "A ranged energy attack that erases the enemy's override.", hack=[True, {"OBLIT":0}])
get_tough = Attack("Get Tough", 5, "This Nanovor places a +10 Armor Override.", override = [True, {"ARM":10}])

energy_blast = Attack("Energyblast", 2, "A ranged energy damage attack; with a Red Spike, more damage that ignores Armor.", damage = [True, [40]], combo = [True, {"DMGSET":50, "PIERCE": "ALL"}], consumes = True)
pod_power = Attack("Pod Power", 4, "This Nanovor places a +15 Strength Override", override = [True, {"STR":15}])
spin_slash = Attack("Spin Slash", 3, "A damage attack", damage = [True, [50]])

gore = Attack("Gore", 1, "A damage attack", damage = [True, [30]])
dig_in = Attack("Dig In", 3,"This Nanovor places a +10 Strength Override", override = [True, {"STR": 10}])
bull_zap = Attack("Bull Zap", 3, "A ranged electric damage attack", damage = [True, [50]])

arcing_gore = Attack("Arcing Gore", 2, "An electric damage attack.", damage = [True, [40]])
bulk_up = Attack("Bulk Up", 4, "This Nanovor places a +15 Strength Override", override = [True, {"STR":15}])
bull_blast = Attack("Bull Blast", 3, "A ranged electric damage attack.", damage = [True, [50]])

crushing_wall = Attack("Crushing Wall", 1, "A damage attack; with a Red Spike, it swap-blocks the opponent for this and the next 2 rounds.", damage = [True, [30]], combo = [True, {"SWAP": 3}], consumes = True)
firewall = Attack("Firewall", 5, "This Nanovor places a +10 Armor Override", override = [True, {"ARM":10}])
hackslash = Attack("Hackslash", 3, "A damage attack", damage = [True, [60]])

tremor = Attack("Tremor", 1, "Ranged energy attack in which the target loses 25 Speed.", hack = [True, {"SPD": 25}])
tank_gore = Attack("Tank Gore", 3, "A headbutt charge that deals 53 Damage" , damage = [True, [50]])

headbutt = Attack("Headbutt", 1, "A damage attack.", damage = [True, [30]])
tank_smash = Attack("Tank Smash", 3, "An attack that causes the target to lose 40 Speed.", hack = [True, {"SPD": 40}])
ion_gore = Attack("Ion Gore", 4, "An electric damage attack.", damage = [True, [60]])

ion_gouge = Attack("Ion Gouge", 2, "An electric attack; with a Red Spike override, there is a second electric attack that ignores Armor.", damage = [True,[40]], combo = [True, {"PIERCE": {"PART":20}}], consumes = True)
atom_smasher = Attack("Atom Smasher", 5, "An electric damage attack that swap-blocks the target for this and the next round.", damage = [True, [60]], hack = [True, {"SWAP": 2}])

slam = Attack("Slam", 2, "A damage attack; with a Red Spike override, the damage ignores Armor.", damage = [True, [40]], combo = [True, {"PIERCE":"ALL"}], consumes = True)
defense = Attack("Defense", 5, "This Nanovor places a +10 Armor Override", override = [True, {"ARM": 10}])
agony = Attack("Agony", 4, "A ranged psychic damage attack.", damage = [True, [60]])

maim = Attack("Maim", 3, "A damage attack.", damage = [True, [50]])
shield = Attack("Shield", 6, "This Nanovor places a +15 Armor Override.", override = [True, {"ARM": 15}])
scorch = Attack("Scorch", 7, "A ranged energy damage attack", damage = [True, [90]])

hit_and_run = Attack("Hit and Run", 2, "A damage attack.", damage = [True, [40]])
zip_zap = Attack("Zip Zap", 3, "A ranged energy attack that also causes Gamma Stalker 1.0 to lose 10 Strength.", damage = [True, [50]], hack = [True, {"DECSELFSTR":10}])

jump_jab = Attack("Jump Jab", 2, "A damage attack.", damage = [True, [40]])
speed_boost = Attack("Speed Boost", 2, "This Nanovor places a +25 Speed Override", override = [True, {"SPD": 25}])
phase_fang = Attack("Phase Fang", 3, "A damage attack; with the Red Spike override, it swap-blocks the target Nanovor for this and the next 2 rounds.", damage = [True, [50]], combo = [True, {"SWAP": 3}], consumes = True)

gamma_zap = Attack("Gamma Zap", 3, "A damage attack that also causes the target to lose 30 Speed", damage = [True, [30]], hack = [True, {"SPD":30}])
spitfire = Attack("Spitfire", 2, "A damage attack; with a Red Spike override, gain a +25 Speed Override.", damage = [True, [35]], combo = [True, {"SETNEW": {"SPD":25}}])
spin_up = Attack("Spin Up", 3, "A damage attack and your Nanovor gains 10 Speed", damage = [True, [45]], hack = [True, {"INCSELFSPD":10}])

battering_ram = Attack("Battering Ram", 2, "A damage attack.", damage = [True, [40]])
thunder_flash = Attack("Thunder Flash", 3, "A ranged energy damage attack that also causes your current Nanovor to lose 10 Speed.", damage = [True, [60]], hack = [True, {"DECSELFSPD":10}])
power_amp = Attack("Power Amp", 4, "This Nanovor places a +15 STR Override", override = [True, {"STR":15}])

two_fist_hit = Attack("Two-Fist Hit", 2, "A damage attack; with a Red Spike override, the target takes double damage.", damage = [True, [40]], combo = [True, {"DMGDOUBLE": 2}], consumes = True)
mentallica = Attack("Mentallica", 4, "A ranged psychic attack in which the target Nanovor loses 50 Speed.", hack = [True, {"SPD": 50}])
gamma_power = Attack("Gamma Power", 5, "This Nanovor places a +20 Strength Override", override = [True, {"STR":20}])

killer_loogie = Attack("Killer Loogie", 2, "Ranged acid attack", damage = [True, [40]])
poison_pinch = Attack("Poison Pinch", 2, "Poison attack that swap-blocks the target for this and the next 2 rounds.", hack = [True, {"SWAP":3}])

mega_blast = Attack("Mega Blast", 3, " ranged energy damage attack; with the Red Spike override, it swap-blocks the target Nanovor for this and the next 3 rounds.", damage = [True, [50]], combo = [True, {"SWAP":4}], consumes = True)
dazzle = Attack("Dazzle", 2, "A ranged antimatter attack that ignores Armor.", damage = [True, [30]], armorpiercing = True)
acid_sting = Attack("Acid Sting", 4, "A ranged acid damage attack.", damage = [True, [60]])

atomic_spit = Attack("Atomic Spit", 3, "A ranged acid damage attack that also causes the target to lose 5 Armor.", damage = [True, [30]], hack = [True, {"ARM":5}])
psychic_sight = Attack("Psychic Sight", 3, "This Nanovor places a Dodge Override", override = [True, {"DODGE":20}])
cosmic_crush = Attack("Cosmic Crush", 4, "A ranged energy damage attack; your Nanovor gains 25 Speed and loses 10 Strength.", damage = [True, [70]], hack = [True, {"INCSELFSPD":25, "DECSELFSTR":10}])

jumpshot = Attack("Jumpshot", 3, "A damage attack that ignores Armor; your Nanovor gains 10 Strength and 20 Speed.", damage = [True, [30]], hack = [True, {"INCSELFSTR":10, "INCSELFSPD":20}], armorpiercing=True)
big_power_up = Attack("Big Power-Up", 4, "This Nanovor places an Override for Magnamods that allow them +1 Energy", override = [True, {"EN-MAG":1}])
flamethrower = Attack("Flamethrower", 5, "A ranged fire damage attack.", damage = [True, [70]])

head_whip = Attack("Head Whip", 1, "A damage attack.", [True,[30]])
electro_lite = Attack("Electro-lite", 2, "A ranged electric attack in which the target loses 10 Strength.", hack=[True, {"STR":10}])
yellow_spike = Attack("Yellow Spike", 1, "This Nanovor places an Override that allows your swarm to make a Yellow Spiked attack.", override = [True, {"SPIKE":"Yellow"}])

zeus_zap = Attack("Zeus Zap", 3, "A ranged electric damage attack that also swap-blocks the target swarm for this and the next round.", damage = [True, [50]], hack = [True, {"SWAP":2}])

plasma_slam = Attack("Plasma Slam", 2, "A damage attack; with a Yellow Spike override, the damage ignores Armor.", damage = [True, [40]], combo = [True, {"PIERCE":"ALL"}], consumes = True)
solid_strike = Attack("Solid Strike", 4, "A ranged electric attack that either inflicts 100 damage that ignores Armor, or no damage", special_condition = [True, {"CHANCE-DMG-50": {"PIERCE":100}}])

plasma_blast = Attack("Plasma Blast", 3, "A ranged electric attack that takes away 15 Strength; with a Yellow Spike override, the target Nanovor takes damage.", hack = [True, {"STR":15}], combo = [True, {"DMGSET":50}], consumes = True)
arc_blast = Attack("Arc Blast", 4, "A ranged electric damage attack.", damage = [True, [60]])

blaster = Attack("Blaster", 3, "A ranged electric damage attack.", damage = [True, [50]])

locust_whip = Attack("Locust Whip", 2, "A damage attack that also causes the attacker to lose 15 Strength.", damage = [True, [60]], hack = [True, {"DECSELFSTR":15}])
plasma_zap = Attack("Plasma Zap", 3, "A damage attack; with a Yellow Spike, the target also loses 20 Strength.", damage = [True, [40]], combo = [True, {"STR":20}], consumes = True)

tusk_slash = Attack("Tusk Slash", 2, "A damage attack.", damage = [True, [35]])
meltdown = Attack("Meltdown", 3, "A damage attack that also causes the target to lose 10 Strength.", damage = [True, [40]], hack = [True, {"STR": 10}])

blade_strike = Attack("Blade Strike", 3, "A damage attack.", damage = [True, [50]])
berserk = Attack("Berserk", 1, "A damage attack that also causes the attacker to lose 10 Health.", damage = [True, [40, 10]])
blunt_trauma = Attack("Blunt Trauma", 4, "An energy attack in which the target Nanovor loses 20 Strength.", hack = [True, {"STR":20}])

doomserk = Attack("Doomserk", 2, "A damage attack; with a Yellow Spike, the target takes extra damage.", damage = [True, [40]], combo = [True, {"DMGSET":60}], consumes = True)
guillotine = Attack("Guillotine", 3, "An energy damage attack that also causes your Nanovor to lose 50 Health.", damage = [True, [80, 50]])

rapier_jab = Attack("Rapier Jab", 2, "A damage attack.", damage = [True, [40]])
flay = Attack("Flay", 2, "A damage attack that ignores Armor; with a Yellow Spike override, the target loses 10 Armor.", damage = [True, [30]], combo = [True, {"ARM":10}], consumes = True)
plasma_pound = Attack("Plasma Pound", 3, "A ranged energy damage attack that ignores Armor and also causes the target to lose 10 Strength.", damage = [True, [30]], hack = [True, {"STR":10}], armorpiercing = True)

power_punt = Attack("Power Punt", 2, "A ranged energy damage attack that ignores Armor.", damage = [True, [30]], armorpiercing = True)
fearsome_flay = Attack("Fearsome Flay", 3, "A damage attack; the target loses 10 Strength and 5 Armor.", damage = [True, [40]], hack = [True, {"STR": 10, "ARM":5}])
splatter = Attack("Splatter", 4, "A damage attack where the target swarm also loses 1 Energy; with a Yellow Spike override, the target takes damage that ignores Armor.", damage = [True, [50]], hack = [True, {"ENSAP":1}], combo = [True, {"PIERCE":{"PART":30}}], consumes = True)

gorgon_gaze = Attack("Gorgon Gaze", 2, "A ranged energy attack that ignores Armor; with a Yellow Spike override, it swap-blocks the target for this and the next 3 rounds.", damage = [True, [30]], combo = [True, {"SWAP":4}], consumes = True, armorpiercing=True)
poison_spit = Attack("Poison Spit", 3, "A ranged poison damage attack that also causes the target to lose 15 Strength.", damage = [True, [30]], hack = [True, {"STR":15}])
mag_hunter = Attack("Mag Hunter", 3, "A damage attack that does more damage if the target is a Magnamod.", damage = [True, [40]], special_condition = [True, {"DMG-CLASS":{"Magnamod":60}}])

whammy = Attack("Whammy", 1, "An attack in which the target loses 25 Speed.", hack = [True, {"SPD":25}])
icy_sigh = Attack("Icy Sigh", 2, "A ranged cold damage attack", damage = [True, [40]])

slip_slash = Attack("Slip Slash", 2, "A ranged cold attack that causes the target to lose 35 Speed.", hack = [True, {"SPD":35}])
ice_storm = Attack("Ice Storm", 3, "A ranged cold damage attack", damage = [True, [50]])
windchill = Attack("Windchill", 3, "A ranged cold attack that swap-blocks the target for this and the next round; with a Yellow Spike override, the target loses 10 Armor.", hack = [True, {"SWAP":2}], combo = [True, {"ARM":10}], consumes = True)

psychic_fade = Attack("Psychic Fade", 2, "A ranged psychic damage attack; with a Yellow Spike override, the target also loses 50 Speed.", damage = [True, [40]], combo = [True, {"SPD":50}], consumes = True)
disk_of_death = Attack("Disk of Death", 3, "A ranged psychic damage attack that ignores Armor.", damage = [True, [35]], armorpiercing = True)
acid_bubble = Attack("Acid Bubble", 4, "A ranged acid attack; the target loses 15 Strength and the opponent is swap-blocked for this and the next 2 rounds.", hack = [True, {"STR":15, "SWAP":3}])

crystal_trap = Attack("Crystal Trap", 1, "An attack that swap-blocks the target for this and the next round.", hack = [True, {"SWAP":2}])
spin_strike = Attack("Spin Strike", 2, "A fire damage attack that ignores Armor.", damage = [True, [30]], armorpiercing=True)

reflex_zap = Attack("Reflex Zap", 2, "An attack that swap-blocks the opponent for this and the next 2 rounds.", hack = [True, {"SWAP":3}])
speed_demon = Attack("Speed Demon", 3, "A ranged fire damage attack that also causes your Nanovor to gain 25 Speed.", damage = [True, [40]], hack = [True, {"INCSELFSPD":25}])

slowdown = Attack("Slowdown", 2, "A damage attack that causes the target to lose 25 Speed.", damage = [True, [30]], hack = [True, {"SPD":25}])
storm_strike = Attack("Storm Strike", 3, "A ranged fire damage attack that also swap-blocks the target for this and the next round.", damage = [True, [40]], hack = [True, {"SWAP":2}])
stormfire = Attack("Stormfire", 4, "A ranged fire attack that ignores Armor and also causes the target to lose 5 Armor.", damage = [True, [40]], hack = [True, {"ARM":5}], armorpiercing=True)

lotus_cut = Attack("Lotus Cut", 2, "A damage attack.", damage = [True, [40]])
stare_down = Attack("Stare Down", 3, "A ranged energy attack that swap-blocks the target for this and the next round and causes it to lose 5 Armor.", hack = [True, {"SWAP":2, "ARM":5}])
chained_fist = Attack("Chained Fist", 3, "A ranged energy damage attack; with a Yellow Spike, the target also loses 50 Speed.", damage = [True, [50]], combo = [True, {"SPD":50}], consumes = True)

slash = Attack("Slash", 1, "An attack that causes the target to lose 25 Speed; with a Yellow Spike override, the target also takes damage.", hack = [True, {"SPD":25}], combo = [True, {"DMGSET":35}], consumes = True)
mega_boom = Attack("Mega Boom", 3, "A ranged energy damage attack that also causes the target to lose 25 Speed", damage = [True, [40]], hack = [True, {"SPD":25}])
taser = Attack("Taser", 4, "A ranged energy damage attack that also swap-blocks the opponent for this and the next 3 rounds", damage = [True, [50]], hack = [True, {"SWAP":4}])

serpent_whip = Attack("Serpent Whip", 4, "A damage attack that also causes the target to lose 25 Speed.", damage = [True, [60]], hack = [True, {"SPD":25}])
fearful_hiss = Attack("Fearful Hiss", 2, "A psychic ranged attack; the target loses 5 Armor and is swap-blocked for this and the next 2 rounds.", hack = [True, {"ARM":5, "SWAP":3}])
phase_strike = Attack("Phase Strike", 3, "A ranged energy damage attack that ignores Armor; with a Yellow Spike override, the target also loses 10 Armor.", damage = [True, [35]], combo = [True, {"ARM":10}], consumes = True, armorpiercing=True)

charge = Attack("Charge", 1, "An electric damage attack.", damage = [True, [30]])
power_rush = Attack("Power Rush", 2, "This Nanovor places a +5 Strength Override", override = [True, {"STR":5}])
blue_spike = Attack("Blue Spike", 1, "This Nanovor places an Override allowing your swarm to make a Blue Spiked attack.", override = [True, {"SPIKE":"Blue"}])

pump_it_up = Attack("Pump it Up", 4, "This Nanovor places an Override for Hexites that allow them +1 Energy", override = [True, {"EN-HEX":1}])
power_sink = Attack("Power Sink", 3, "A ranged electric attack that causes the target to lose 40 Speed.", hack = [True, {"SPD":40}])

slayer_sting = Attack("Slayer Sting", 2, "An electric damage attack that ignores Armor.", damage = [True, [30]], armorpiercing=True)
stormfield = Attack("Stormfield", 5, "This Nanovor places a +1 Energy Override", override = [True, {"EN-ALL":1}])
spine_sting = Attack("Spine Sting", 2, "A ranged electric damage attack; with the Blue Spike override, the target swarm loses 2 Energy.", damage = [True, [50]], combo = [True, {"ENSAP":2}], consumes = True)

slapstick = Attack("Slapstick", 2, "A damage attack.", damage = [True, [40]])
gutbuster = Attack("Gutbuster", 3, "A ranged poison damage attack in which the damage equals the target's Energy x10; your Nanovor loses 10 Speed.", hack = [True, {"DECSELFSPD":10}], special_condition = [True, {"EN-DMG":{"PIERCE":10}}])
heckle = Attack("Heckle", 3, "A ranged antimatter attack in which the target takes damage and the target swarm loses 1 Energy.", damage = [True, [30]], hack = [True, {"ENSAP":1}])

stinger = Attack("Stinger", 1, "A ranged antimatter damage attack; with a Blue Spike override, the attack does higher damage that ignores Armor.", damage = [True, [25]], combo = [True, {"DMGSET":40, "PIERCE": "ALL"}], consumes = True)
punchline = Attack("Punchline", 3, "A damage attack and if target is a Velocitron, damage ignores ARM", damage = [True, [40]], special_condition = [True, {"PIERCE-CLASS":{"Velocitron":"ALL"}}])
wisecrack = Attack("Wisecrack", 3, "A ranged antimatter attack that inflicts massive damage or 0 damage.", special_condition = [True, {"CHANCE-DMG-50": {"XTRANONPIERCE":80}}])

knock_knock = Attack("Knock Knock", 1, "An attack; the target loses 20 Speed and is swap-blocked for this and the next 2 rounds.", hack = [True, {"SWAP":3, "SPD":20}])
ventriloquist = Attack("Ventriloquist", 2, "A damage attack; with a Blue Spike, your Nanovor has a Good chance of Dodging an attack.", damage = [True, [40]], combo = [True, {"SETNEW":{"DODGE":20}}], consumes = True)
pun_ish = Attack("Pun-ish", 3, "A damage attack that also causes the target swarm to lose 2 Energy.", damage = [True, [30]], hack = [True, {"ENSAP":2}])
riddle = Attack("Riddle", 3, "An attack that ignores armor", damage = [True, [35]], armorpiercing=True)

gigazap = Attack("Gigazap", 2, "A ranged electric damage attack that ignores armor", damage = [True, [30]], armorpiercing=True)
meltdownv2 = Attack("Meltdown", 2, "Ranged psychic damage attack that also causes the enemy to lose 1 energy.", damage = [True, [20]], hack = [True, {"ENSAP":1}])

psychic_drain = Attack("Psychic Drain", 3, "A ranged psychic attack in which the target loses 15 Strength.", hack = [True, {"STR":15}])
psi_strike = Attack("Psi-Strike", 4, "A ranged psychic damage attack that also causes the target swarm to lose 1 Energy.", damage = [True, [50]], hack = [True, {"ENSAP":1}])

psi_burst = Attack("Psi-Burst", 3, "A ranged psychic damage attack; with a Blue Spike override, your swarm gains 6 Energy.", damage = [True, [30]], combo = [True, {"ENADD":6}], consumes = True)
mind_strike = Attack("Mind Strike", 3, "A ranged psychic damage attack that ignores Armor.", damage = [True, [35]], armorpiercing=True)

gob_smack = Attack("Gob Smack", 1, "A ranged damage attack; with a Blue Spike override, the target takes double damage.", damage = [True, [30]], combo = [True, {"DMGDOUBLE":2}], consumes = True)
smackdown = Attack("Smackdown", 4, "An electric damage attack that does damage equal to the target's EN x15; your current Nanovor loses 25 Speed.", hack = [True, {"DECSELFSPD":25}], special_condition = [True, {"EN-DMG":{"PIERCE":15}}])

face_plant = Attack("Face Plant", 3, "A damage attack that ignores Armor and swap-blocks the target for this and the next round.", damage = [True, [30]], hack = [True, {"SWAP":2}], armorpiercing=True)
rust = Attack("Rust", 2, "A ranged poison damage attack where the target loses 5 Armor; with a Blue Spike override, damage that ignores Armor.", hack = [True, {"ARM":5}], combo = [True, {"DMGSET":30, "PIERCE":"ALL"}], consumes = True)
whirlwind = Attack("Whirlwind", 4, "An electric damage attack that also causes the target swarm to lose 1 Energy.", damage = [True, [50]], hack = [True, {"ENSAP":1}])

dash_smash = Attack("Dash Smash", 2, "A damage attack that ignores Armor.", damage = [True, [30]], armorpiercing=True)
corrode = Attack("Corrode", 2, "An attack that causes the target Nanovor to lose 5 Armor; with a Blue Spike Override, the target loses 15 Armor.", hack = [True, {"ARM":5}], combo = [True, {"ARM":10}], consumes = True)
blendo = Attack("Blendo", 3, "A damage attack where the target loses 20 Speed.", damage = [True, [35]], hack = [True, {"SPD":20}])
gigadrain = Attack("Gigadrain", 4, "A damage attack in which the target also loses 3 Energy.", damage = [True, [40]], hack = [True, {"ENSAP":3}])

incinerate = Attack("Incinerate", 3, "A ranged fire damage attack; if the target's Speed is less than 50, the damage ignores Armor.", damage = [True, [40]], special_condition = [True, {"<SPD":{"50":"PIERCEALL"}}])
siren_sphere = Attack("Siren Sphere", 4, "A ranged psychic attack in which the target loses 15 Strength and the target swarm loses 3 Energy.", hack = [True, {"STR":15, "ENSAP":3}])
sonic_strike = Attack("Sonic Strike", 3, "A damage attack that ignores Armor in which the target also loses 10 Strength.", damage = [True, [30]], hack = [True, {"STR":10}], armorpiercing=True)

pierce = Attack("Pierce", 1, "A damage attack that ignores Armor and also causes your nanovor to lose 10 Speed.", damage = [True, [25]], hack = [True, {"DECSELFSPD":10}], armorpiercing=True)
power_surge = Attack("Power Surge", 3, "This Nanovor places a +40 Speed Override", override = [True, {"SPD":40}])

dodge = Attack("Dodge", 3, "Your Nanovor places a Dodge Override that gives your Nanovor a Good Chance of Dodging an attack.", override = [True, {"DODGE":25}])

short_circuit = Attack("Short Circuit", 3, "A ranged antimatter damage attack; with a Blue Spike override, the target swarm loses 4 Energy without taking damage.", damage = [True, [40]], combo = [True, {"ENSAP":4, "DMGSET":0}], consumes = True)

crunch = Attack("Crunch", 2, "A damage attack.", damage = [True, [40]])
tangler = Attack("Tangler", 1, "An attack that swap-blocks the opponent for this and the next round.", hack = [True,{"SWAP":2}])

kraken_smack = Attack("Kraken Smack", 2, "A damage attack that ignores Armor.", damage = [True, [30]], armorpiercing=True)
tentacle_zap = Attack("Tentacle Zap", 2, "A poison attack that swap-blocks the target for this and the next 2 rounds.", hack = [True, {"SWAP":3}])
fathom_blast = Attack("Fathom Blast", 4, "A ranged energy attack in which the target loses 10 Armor.", hack = [True, {"ARM":10}])

poison_darts = Attack("Poison Darts", 2, "A ranged poison damage attack that ignores Armor; your Nanovor is stunned and can only choose to Pass for 2 rounds.", damage = [True, [45]], hack = [True, {"SELFSTUN":2}], armorpiercing=True)
hack_zap = Attack("Hack Zap", 3, "A ranged poison damage attack that erases the most recent hack from all Nanovor in all swarms.", damage = [True, [30]], aoe_effect = [True, {"CLEARHACKS":"RECENT"}])
blue_blast = Attack("Blue Blast", 3, "A ranged electric damage attack; with a Blue Spike override, the target swarm loses 2 Energy.", damage = [True, [50]], combo = [True, {"ENSAP":2}], consumes = True)

zapper = Attack("Zapper", 2, "An electric damage attack that ignores Armor", damage = [True, [30]], armorpiercing = True)
zoomer = Attack("Zoomer", 2, "An attack that gives your Nanovor 25 Speed taken from the target Nanovor.", hack = [True, {"INCSELFSPD":25, "SPD":25}])
zinger = Attack("Zinger", 3, "A ranged electric damage attack that also causes the target swarm to lose 1 Energy.", damage = [True, [40]], hack = [True, {"ENSAP":1}])

asp_kiss = Attack("Asp Kiss", 2, "A damage attack.", damage = [True, [40]])
energy_drain = Attack("Energy Drain", 3, "A ranged antimatter attack; it takes 1 Energy from the target swarm, ignores Armor, and gives your Nanovor 10 Strength.", damage = [True, [15]], hack = [True, {"ENSAP":1, "INCSELFSTR":10}], armorpiercing=True)
flying_fang = Attack("Flying Fang", 5, "A ranged electric damage attack which does more damage if the target Nanovor has more than 120 Strength.", damage = [True, [40]], special_condition = [True, {">STR":{"120":{"DMGSET":75}}}])

##### WAVE 2 #####

fireplow = Attack("Fireplow", 2, "A fire damage attack", damage = [True, [40]])
hardshell = Attack("Hardshell", 3, "This Nanovor places a +5 Armor Override", override = [True, {"ARM":5}])

lockdown = Attack("Lockdown", 2, "An attack that swap-blocks the target for this and the next 3 rounds.", hack = [True, {"SWAP":4}])

torch = Attack("Torch", 3, "A fire damage attack that swap-blocks the target for this and the next three rounds.", damage = [True, [40]], hack = [True, {"SWAP":4}])
energy_bite = Attack("Energy Bite", 4, "An energy damage attack", damage = [True, [60]])
hyperburrow = Attack("Hyperburrow", 3, "A damage attack; with a Red Spike override, the same damage ignores Armor.", damage = [True, [45]], combo = [True, {"PIERCE":"ALL"}], consumes = True)

infection = Attack("Infection", 2, "A poison damage attack", damage = [True, [40]])
hyperspeed = Attack("Hyperspeed", 2,"This Nanovor places a +20 Speed Override", override = [True, {"SPD":20}])
belch = Attack("Belch", 3, "A ranged poison damage attack that ignores Armor.", damage = [True, [35]], armorpiercing=True)

hyperbelch = Attack("Hyperbelch", 2, "A poison damage attack; with a Red Spike override, the attack does more damage", damage = [True, [40]], combo = [True, {"DMGSET":70}], consumes = True)
poison_stench = Attack("Poison Stench", 3, "A ranged poison attack that causes the target to lose 40 Speed", hack = [True, {"SPD":40}])
tusk_tunnel = Attack("Tusk Tunnel", 4, "A damage attack that also causes your Nanovor to gain 20 Speed", damage = [True, [50]], hack = [True, {"INCSELFSPD":20}])

frost = Attack("Frost", 2, "A cold damage attack; with a Red Spike override, the attack deals double damage.", damage = [True, [30]], combo = [True, {"DMGDOUBLE":2}], consumes = True)
hyperslash = Attack("Hyperslash", 3, "A cold damage attack that ignores Armor; your Nanovor is stunned and can only Pass or Swap for 2 rounds.", damage = [True, [70]], hack = [True, {"SELFSTUN":2}], armorpiercing=True)

swipe = Attack("Swipe", 2, "A damage attack", damage = [True, [40]])
growl = Attack("Growl", 2, "This Nanovor places a +5 Strength Override", override = [True, {"STR":5}])

breakthrough = Attack("Breakthrough", 1, "A damage attack; with a Red Spike override, the target also loses 10 Armor", damage = [True, [30]], combo = [True, {"ARM":10}], consumes = True)
howl = Attack("Howl", 3, "An electric damage attack", damage = [True, [50]])

rumbler = Attack("Rumbler", 1, "A damage attack; with a Red Spike override, the target Nanovor loses 10 Armor", damage = [True, [30]], combo = [True, {"ARM":10}], consumes = True)
blocker = Attack("Blocker", 2, "An attack that swap-blocks the target for this and the next 3 rounds.", hack = [True, {"SWAP":4}])
eraser = Attack("Eraser", 3, "An energy damage attack; with a Red Spike, the opponent's last override is deleted, and the Red Spike remains in play", damage = [True, [40]], combo = [True, {"OBLIT":0}])
stronger = Attack("Stronger", 5, "This Nanovor places a +20 Strength Override", override = [True, {"STR":20}])

swat = Attack("Swat", 1, "An electrical damage attack", damage = [True, [30]])

entangle = Attack("Entangle", 2, "An electrical damage attack", damage = [True, [40]])
thunderpower = Attack("Thunderpower", 2, "This Nanovor places a +10 Strength Override", override = [True, {"STR":10}])
swarm_shot = Attack("Swarm Shot", 3, "An electrical damage attack that swap-blocks the target swarm for this and the next 3 rounds.", damage = [True, [40]], hack = [True, {"SWAP":4}])

grab = Attack("Grab", 2, "An attack that erases the target's override, and swap-blocks the opponent for this and the next 2 rounds.", hack = [True, {"OBLIT":0, "SWAP":3}])
fireswarm = Attack("Fireswarm", 2, "A fire damage attack that deals random damage", damage = [True, [30]], special_condition = [True, {"CHANCE-DMG-50": {"XTRANONPIERCE":60}}])

pinch = Attack("Pinch", 1, "A damage attack", damage = [True, [30]])
clamp = Attack("Clamp", 3, "A damage attack; with a Red Spike override, the target swarm is also swap-blocked for this and the next 4 rounds.", damage = [True, [50]], combo = [True, {"SWAP":5}], consumes = True)

whip = Attack("Whip", 4, "A damage attack", damage = [True, [60]])
pincer = Attack("Pincer", 3, "An acid damage attack that ignores Armor", damage = [True, [35]], armorpiercing=True)
power_play = Attack("Power Play", 6, "This Nanovor places an (sic) +20 Strength and +20 Speed override", override = [True, {"STR":20, "SPD":20}])
stunner = Attack("Stunner", 3, "A damage attack that also swap-blocks the opponent for this and the next 2 rounds and deletes the opponent's most recent override.", damage = [True, [30]], hack = [True, {"SWAP":3, "OBLIT":0}])

psi_zap = Attack("Psi-Zap", 2, "An energy damage attack", damage = [True, [40]])
think_fast = Attack("Think Fast!", 3, "This Nanovor places a +40 Speed Override", override = [True, {"SPD":40}])

brain_freeze = Attack("Brain Freeze", 3, "An energy damage attack; with a Red Spike override, the target also loses 40 Speed", damage = [True, [50]], combo = [True, {"SPD":40}], consumes = True)
brain_storm = Attack("Brain Storm", 2, "A damage attack that also swap-blocks the opponent for this and the next 3 rounds.", damage = [True, [30]], hack = [True, {"SWAP":4}])

kickoff = Attack("Kickoff", 1, "A damage attack; with a Red Spike override, your current Nanovor gains 30 Speed", damage = [True, [30]], combo = [True, {"INCSELFSPD":30}], consumes = True)
shocker = Attack("Shocker", 3, "A damage attack that also swap-blocks the opponent for this and the next 2 rounds", damage = [True, [40]], hack = [True, {"SWAP":3}])
rumble_pulse = Attack("Rumble Pulse", 2, "An attack that causes the target Nanovor to lose 10 Strength; with a Yellow Spike override, the attack also does damage.", hack = [True, {"STR":10}], combo = [True, {"DMGSET":35}], consumes = True)
static_boom = Attack("Static Boom", 5, "A damage attack that also causes the target Nanovor to lose 10 Armor", damage = [True, [50]], hack = [True, {"ARM":10}])

thunder = Attack("Thunder", 2, "A damage attack, with a Blue Spike Override the opponent loses 3 Energy", damage = [True, [30]], combo = [True, {"ENSAP":3}], consumes=True)
lightning = Attack("Lightning", 3, "A damage attack; with a Red Spike override, gain a 15 Strength Override", damage = [True, [50]], combo = [True, {"SETNEW": {"STR":15}}])
wardog = Attack("Wardog", 4, "An energy damage attack and the target Nanovor loses 5 Armor", damage = [True, [50]], hack = [True, {"ARM":5}])
flash = Attack("Flash", 4, "An attack that swap-blocks the target for this and the next 2 rounds and takes away 15 Strength", hack = [True, {"SWAP":3, "STR":15}])

run_down = Attack("Run Down", 2, "A damage attack", damage = [True, [40]])
exhaust = Attack("Exhaust", 2, "An energy attack that causes the target Nanovor to lose 10 Strength", hack = [True, {"STR":10}])

backspin = Attack("Backspin", 2, "An energy attack that causes the target Nanovor to lose 5 Armor", hack = [True, {"ARM":5}])
spin_out = Attack("Spin Out", 3, "A damage attack that also causes the target Nanovor to lose 10 Strength", damage = [True, [40]], hack = [True, {"STR":10}])

run_over = Attack("Run Over", 2, "A damage attack that ignores armor", damage = [True, [30]], armorpiercing=True)
eat_my_dust = Attack("Eat My Dust!", 2, "An attack that causes the target to lose 5 Armor; with a Yellow Spike override, the target loses 15 Armor", hack = [True, {"ARM":5}], combo = [True, {"ARM":10}], consumes = True)
ready_set_go = Attack("Ready Set Go!", 4, "An energy damage attack", damage = [True, [60]])

spear = Attack("Spear", 2, "A damage attack that also causes the target Nanovor to lose 10 Speed", damage = [True, [30]], hack = [True, {"SPD":10}])
fireball = Attack("Fireball", 3, "A damage attack that also causes your current Nanovor to gain 20 Speed", damage = [True, [40]], hack = [True, {"INCSELFSPD":20}])
wise_up = Attack("Wise Up", 4, "This Nanovor places a +20 Speed and +10 Strength Override", override = [True, {"SPD":20, "STR":10}])

spazzle = Attack("Spazzle", 4, "An electrical damage attack", damage = [True, [60]])
electrospear = Attack("Electrospear", 2, "A damage attack that also causes the target Nanovor to lose 15 Speed", damage = [True, [30]], hack = [True, {"SPD":15}])
power_pulse = Attack("Power Pulse", 3, "An attack that causes the target Nanovor to lose 15 Strength", hack = [True, {"STR":15}])
distract = Attack("Distract", 3, "An attack that causes the target Nanovor to lose 40 Speed", hack = [True, {"SPD":40}])

dragonfire = Attack("Dragonfire", 2, "A fire damage attack", damage = [True, [40]])

scorchv2 = Attack("Scorch", 2, "A fire damage attack; with a Yellow Spike override, the target Nanovor loses 10 Armor", damage = [True, [40]], combo = [True, {"ARM":10}], consumes = True)
flame_up = Attack("Flame Up", 3, "This Nanovor places a +10 Strength Override", hack = [True, {"STR":10}])
inferno = Attack("Inferno", 5, "A fire damage attack", damage = [True, [70]])

frostbite = Attack("Frostbite", 2, "An ice damage attack that also swap-blocks the target for this and the next 2 rounds", damage = [True, [30]], hack = [True, {"SWAP":3}])
blazeburn = Attack("Blazeburn", 2, "A fire damage attack", damage = [True, [40]])
meditate = Attack("Meditate", 2, "An attack that causes the target to lose 5 Armor", hack = [True, {"ARM":5}])

fireclap = Attack("Fireclap", 1, "A fire damage attack", damage = [True, [30]])
hypnotize = Attack("Hypnotize", 3, "The target Nanovor loses 25 Speed and 15 Strength", hack = [True, {"SPD":25, "STR":15}])
tantrum = Attack("Tantrum", 3, "A damage attack", damage = [True, [50]])
hydra_slap = Attack("Hydra Slap", 4, "A damage attack that also causes the target to lose 10 Armor", damage = [True, [40]], hack = [True, {"ARM":10}])

avalanche = Attack("Avalanche", 1, "An ice damage attack that also causes the target Nanovor to lose 10 Speed", damage = [True, [20]], hack = [True, {"SPD":10}])
icicle_storm = Attack("Icicle Storm", 3, "An ice damage attack", damage = [True, [50]])

poison_spray = Attack("Poison Spray", 3, "A poison damage attack", damage = [True, [50]])
stinkbomb = Attack("Stinkbomb", 2, "A poison damage attack; with a Yellow Spike Override, the target Nanovor loses 25 Strength", damage = [True, [40]], combo = [True, {"STR":25}], consumes = True)
faster = Attack("Faster!", 2, "An energy damage attack that also causes your Nanovor to gain 10 Speed", damage = [True, [30]], hack = [True, {"INCSELFSPD":10}])

burn_down = Attack("Burn Down", 4, "A fire damage attack that also swap-blocks the opponent for this and the next 4 rounds", damage = [True, [50]], hack = [True, {"SWAP":5}])
hot_air = Attack("Hot Air", 3, "An attack that causes the target to lose 5 Armor and 30 Speed", hack = [True, {"ARM":5, "SPD":30}])
heat_wave = Attack("Heat Wave", 2, "A fire damage attack", damage = [True, [40]])

bound = Attack("Bound", 2, "A damage attack; with a Yellow Spike override, the target also loses 15 Strength", damage = [True, [30]], combo = [True, {"STR":15}], consumes = True)
snapshot = Attack("Snapshot", 3, "A damage attack that also swap-blocks the opponent for this and the next 2 rounds", damage = [True, [40]], hack = [True, {"SWAP":3}])
crystal_maul = Attack("Crystal Maul", 3, "A damage attack that also causes the target Nanovor to lose 10 Strength", damage = [True, [40]], hack = [True, {"STR":10}])

turbo_kick = Attack("Turbo Kick", 2, "A damage attack", damage = [True, [40]])
speed_trade = Attack("Speed Trade", 2, "An attack that causes the target Nanovor to lose 20 Speed, and your current Nanovor gains 20 Speed", hack = [True, {"INCSELFSPD":20, "SPD":20}])
fightspeed = Attack("Fightspeed", 3, "A damage attack that ignores Armor; with a Yellow Spike this Nanovor places a +40 Speed Override", damage = [True, [35]], combo = [True, {"SETNEW":{"SPD":40}}], armorpiercing = True)

slow_down = Attack("Slow Down", 1, "An energy attack that causes the target Nanovor to lose 15 Speed", hack = [True, {"SPD":15}])
shock_sting = Attack("Shock Sting", 2, "An electric damage attack", damage = [True, [40]])

poison_sting = Attack("Poison Sting", 2, "A poison damage attack that ignores armor", damage = [True, [30]], armorpiercing = True)
poison_mist = Attack("Poison Mist", 2, "A poison damage attack; with a Yellow Spike override, the target Nanovor also loses 10 Armor", damage = [True, [40]], combo = [True, {"ARM":10}], consumes = True)
shock_and_awe = Attack("Shock and Awe", 2, "An attack that causes the target Nanovor to lose 30 Speed", hack = [True, {"SPD":30}])

scarab_slash = Attack("Scarab Slash", 3, "A fire damage attack", damage = [True, [50]])
tonguestrike = Attack("Tonguestrike", 2, "A damage attack; with a Red Spike override, the opponent is also swap-blocked for this and the next 3 rounds.", damage = [True, [40]], combo = [True, {"SWAP":4}], consumes = True)
psi_cannon = Attack("Psi Cannon", 3, "An attack that causes the target Nanovor to lose 15 Strength; with a Yellow Spike override, it also loses 10 Armor", hack = [True, {"STR":15}], combo = [True, {"ARM":10}], consumes = True)

claw_smash = Attack("Claw Smash", 1, "A damage attack; with a Yellow Spike override, you also gain a +10 Strength override", damage = [True, [30]], combo = [True, {"SETNEW":{"STR":10}}])
whiplash = Attack("Whiplash", 2, "A damage attack that ignores Armor; with a Blue Spike override, the opponent also loses 2 Energy", damage = [True, [30]], combo = [True, {"ENSAP":2}], consumes = True, armorpiercing=True)
crystal_flash = Attack("Crystal Flash", 3, "A ranged attack that also causes the target Nanovor to lose 5 Armor", damage = [True, [40]], hack = [True, {"ARM":5}])
fire_splash = Attack("Fire Splash", 3, "A fire attack", damage = [True, [60]])

triton_chomp = Attack("Triton Chomp", 2, "A damage attack that ignores Armor", damage = [True, [30]], armorpiercing=True)
spitball = Attack("Spitball", 1, "The target Nanovor loses 20 Speed", hack = [True, {"SPD":20}])

sting = Attack("Sting", 2, "A damage attack", damage = [True, [40]])
spark_siphon = Attack("Spark Siphon", 2, "A damage attack, with a Blue Spike override, the target loses 2 Energy", damage = [True, [40]], combo = [True, {"ENSAP":2}], consumes = True)
paralyze = Attack("Paralyze", 3, "An attack that swap-blocks the opponent for this and the next 2 rounds, and causes the target to lose 40 Speed", hack = [True, {"SWAP":3, "SPD":40}])

shockback = Attack("Shockback", 2, "An attack that causes the opponent to lose 3 Energy, and stuns your current Nanovor for this round and next", hack = [True, {"ENSAP":3, "SELFSTUN":1}])
triton_strike = Attack("Triton Strike", 4, "An electric damage attack", damage = [True, [60]])

fang_blast = Attack("Fang Blast", 2, "An energy damage attack that ignores armor", damage = [True, [30]], armorpiercing = True)
snare = Attack("Snare", 3, "An attack that swap-blocks the opponent for this and the next 4 rounds.", hack = [True, {"SWAP":5}])

spiderbite = Attack("Spiderbite", 3, "An electric damage attack; with a Blue Spike override, the opponent also loses 2 Energy", damage = [True, [50]], combo = [True, {"ENSAP":2}], consumes = True)
triton_tumble = Attack("Triton Tumble", 3, "The target Nanovor loses 30 Strength, and your current Nanovor loses 30 Speed", hack = [True, {"STR":30, "DECSELFSPD":30}])

shard_slice = Attack("Shard Slice", 2, "A damage attack that ignores armor", damage = [True, [30]], armorpiercing=True)
jumpstart = Attack("Jumpstart", 2, "This Nanovor places a +25 SPD Override", override = [True, {"SPD":25}])

slider = Attack("Slider", 3, "A damage attack", damage = [True, [50]])
burn = Attack("Burn", 2, "A damage attack that ignores armor", damage = [True, [30]], armorpiercing=True)
weaken = Attack("Weaken", 1, "An attack that causes the target Nanovor to lose 5 Strength", hack = [True, {"STR":5}])

blue_thunder = Attack("Blue Thunder", 3, "A damage attack; with a Blue Spike override, this damage ignores armor", damage = [True, [50]], combo = [True, {"PIERCE":"ALL"}], consumes = True)
slide_by = Attack("Slide-By", 3, "A damage attack that also causes the opponent to lose 1 Energy", damage = [True, [40]], hack = [True, {"ENSAP":1}])
shutdown = Attack("Shutdown", 5, "A ranged attack that causes the target Nanovor to lose 10 Armor and 10 Strength.", hack = [True, {"ARM":10, "STR":10}])

shard_smash = Attack("Shard Smash", 3, "A damage attack that also deletes the opponent's override", damage = [True, [30]], hack = [True, {"OBLIT":0}])
pummel = Attack("Pummel", 2, "A damage attack that ignores armor; with a Blue Spike override, the attack does heavier damage that also ignores armor", damage = [True, [30]], combo = [True, {"DMGSET":50, "PIERCE":"ALL"}], consumes = True, armorpiercing=True)
shard_blast = Attack("Shard Blast", 3, "A ranged damage attack that also causes the target to lose 10 Strength", damage = [True, [30]], hack = [True, {"STR":10}])

fire_smash = Attack("Fire Smash", 2, "A fire damage attack", damage = [True, [40]])
shard_shatter = Attack("Shard Shatter", 4, "A damage attack that ignores armor; with a Blue Spike override, the attack does more damage that also ignores armor", damage = [True, [40]], combo = [True, {"DMGDOUBLE":2, "PIERCE":"ALL"}], consumes = True, armorpiercing=True)

crunchv2 = Attack("Crunch", 2, "A damage attack that ignores armor", damage = [True, [30]], armorpiercing=True)
random_jack = Attack("Random Jack", 3, "An energy attack that either does moderate damage or heavy damage that ignores armor", damage = [True, [30]], special_condition=[True, {"CHANCE-DMG-50": {"XTRAPIERCE":50}}])

acid_burn = Attack("Acid Burn", 3, "An acid damage attack that ignores armor", damage = [True, [35]], armorpiercing=True)
crashoverride = Attack("CrashOverride", 2, "An attack that removes the target Swarms Override; with a Blue Spike override, it also swap-blocks the opponent for this and the next 3 rounds", hack = [True, {"OBLIT":0}], combo = [True, {"SWAP":4}], consumes = True)
phreak = Attack("Phreak", 3, "An energy damage attack that also causes the opponent to lose 5 armor", damage = [True, [20]], hack = [True, {"ARM":5}])

rip = Attack("Rip", 2, "A damage attack that ignores armor", damage = [True, [30]], armorpiercing=True)
whopper = Attack("Whopper", 3, "A ranged attack that drains 5 Energy from the target swarm, and your Nanovor is stunned for two rounds", hack = [True, {"ENSAP":5, "SELFSTUN":2}])

thrash = Attack("Thrash", 2, "A damage attack; with a Blue Spike override, your Nanovor also gains 10 Strength", damage = [True, [40]], combo = [True, {"INCSELFSTR":10}], consumes = True)
cyber_shock = Attack("Cyber Shock", 3, "A ranged electric damage attack that ignores armor", damage = [True, [35]], armorpiercing=True)
depth_charge = Attack("Depth Charge", 5, "A damage attack", damage = [True, [70]])

battle_rush = Attack("Battle Rush", 1, "A damage attack", damage = [True, [30]])
war_dance = Attack("War Dance", 4, "A damage attack that ignores Armor and also causes the target Nanovor to lose 2 Energy", damage = [True, [35]], hack = [True, {"ENSAP":2}], armorpiercing=True)

pounce = Attack("Pounce", 1, "A damage attack; with a Blue Spike override, the attack does more damage that ignores armor", damage = [True, [30]], combo = [True, {"DMGSET":45, "PIERCE":"ALL"}], consumes = True)
chop_drop = Attack("Chop Drop", 3, "An energy attack that also causes the target Nanovor to lose 10 Speed", damage = [True, [50]], hack = [True, {"SPD":10}])
battle_dance = Attack("Battle Dance", 4, "An attack that causes the target swarm to lose 1 Energy and your Nanovor gains 20 Speed", hack = [True, {"ENSAP":1, "INCSELFSPD":20}])

psi_drain = Attack("Psi Drain", 4, "An energy attack that causes the opponent to lose 25 Speed and 3 Energy", hack = [True, {"ENSAP":3, "SPD":25}])
driller = Attack("Driller", 2, "An electric damage attack that ignores armor; with a Blue Spike override, it does more damage", damage = [True, [30]], combo = [True, {"DMGSET":50, "PIERCE":"ALL"}], consumes = True, armorpiercing=True)

collider = Attack("Collider", 4, "A damage attack", damage = [True, [60]])
whirlpool = Attack("Whirlpool", 2, "An attack that causes the opponent to lose 1 Energy and 5 Strength; with a Blue Spike override, the attack also does damage", hack = [True, {"ENSAP":1, "STR":5}], combo = [True, {"DMGSET":40}], consumes = True)
triton_blast = Attack("Triton Blast", 2, "An electric damage attack; with a Yellow Spike, the target Nanovor loses 20 Strength", damage = [True, [40]], combo = [True, {"STR":40}], consumes = True)
shock_drain = Attack("Shock Drain", 3, "An attack that causes the target Nanovor to lose 20 Speed and 10 Strength", hack = [True, {"SPD":20, "STR":10}])

##### WAVE 1 #####

# MAGNAMODS
electropod1 = Nanovor("Electropod 1.0", 100, 5, 10, 120, 175, "Magnamod", [electro_shock, armor_up, red_spike])
electropod2 = Nanovor("Electropod 2.0", 130, 10, 15, 140, 255, "Magnamod", [powerball, obliterate, get_tough])
electropod3 = Nanovor("Electropod 3.0", 150, 15, 25, 150, 380, "Magnamod", [electro_shock, energy_blast, pod_power, spin_slash])

electrobull1 = Nanovor("Electrobull 1.0", 100, 10, 25, 130, 260, "Magnamod", [gore, dig_in, bull_zap])
electrobull2 = Nanovor("Electrobull 2.0", 105, 10, 30, 140, 285, "Magnamod", [arcing_gore, bulk_up, bull_blast])

electro_shield1 = Nanovor("Electroshield 1.0", 130, 10, 35, 120, 280, "Magnamod", [crushing_wall, firewall, hackslash])

tank_walker1 = Nanovor("Tank Walker 1.0", 105, 5, 10, 105, 165, "Magnamod", [tremor, tank_gore, red_spike])
tank_walker2 = Nanovor("Tank Walker 2.0", 120, 10, 15, 120, 240, "Magnamod", [headbutt, tank_smash, ion_gore])
tank_walker3 = Nanovor("Tank Walker 3.0", 130, 10, 25, 140, 270, "Magnamod", [headbutt, ion_gouge, atom_smasher])

tank_strider1 = Nanovor("Tank Strider 1.0", 110, 10, 5, 115, 255, "Magnamod", [slam, defense, agony])
tank_strider2 = Nanovor("Tank Strider 2.0", 130, 15, 15, 130, 240, "Magnamod", [maim, shield, scorch])

gamma_stalker1 = Nanovor("Gamma Stalker 1.0", 100, 5, 10, 120, 175, "Magnamod", [hit_and_run, zip_zap, red_spike])
gamma_stalker2 = Nanovor("Gamma Stalker 2.0", 115, 10, 15, 135, 275, "Magnamod", [jump_jab, speed_boost, phase_fang])
gamma_stalker3 = Nanovor("Gamma Stalker 3.0", 135, 10, 20, 140, 275, "Magnamod", [gamma_zap, spitfire, spin_up])

gamma_fury1 = Nanovor("Gamma Fury 1.0", 105, 10, 25, 115, 270, "Magnamod", [battering_ram, thunder_flash, power_amp])
gamma_fury2 = Nanovor("Gamma Fury 2.0", 125, 10, 35, 130, 285, "Magnamod", [two_fist_hit, mentallica, gamma_power])

mega_scorpion1 = Nanovor("Mega Scorpion 1.0", 100, 10, 20, 105, 175, "Magnamod", [killer_loogie, poison_pinch, red_spike])
mega_scorpion2 = Nanovor("Mega Scorpion 2.0", 120, 10, 25, 120, 270, "Magnamod", [mega_blast, dazzle, acid_sting])

phase_tank1 = Nanovor("Phase Tank 1.0", 125, 10, 35, 140, 285, "Magnamod", [atomic_spit, psychic_sight, cosmic_crush])

circuit_tank1 = Nanovor("Circuit Tank 1.0", 115, 10, 30, 100, 240, "Magnamod", [jumpshot, big_power_up, flamethrower])

# VELOCITRONS
plasma_lash1 = Nanovor("Plasma Lash 1.0", 110, 0, 25, 85, 155, "Velocitron", [head_whip, electro_lite, yellow_spike])
plasma_lash2 = Nanovor("Plasma Lash 2.0", 115, 0, 30, 100, 230, "Velocitron", [head_whip, electro_lite, zeus_zap])
plasma_lash3 = Nanovor("Plasma Lash 3.0", 130, 0, 35, 115, 245, "Velocitron", [plasma_slam, zeus_zap, solid_strike])

plasma_locust1 = Nanovor("Plasma Locust 1.0", 110, 0, 30, 95, 235, "Velocitron", [headbutt, plasma_blast, arc_blast])
plasma_locust2 = Nanovor("Plasma Locust 2.0", 130, 0, 50, 105, 240, "Velocitron", [headbutt, obliterate, blaster])
plasma_locust3 = Nanovor("Plasma Locust 3.0", 140, 0, 55, 115, 280, "Velocitron", [headbutt, locust_whip, plasma_zap, yellow_spike])

plasma_lancer1 = Nanovor("Plasma Lancer 1.0", 125, 5, 60, 115, 260, "Velocitron", [tusk_slash, meltdown, bulk_up])

doom_blade1 = Nanovor("Doom Blade 1.0", 100, 0, 25, 85, 160, "Velocitron", [blade_strike, berserk, yellow_spike])
doom_blade2 = Nanovor("Doom Blade 2.0", 110, 0, 30, 100, 220, "Velocitron", [blade_strike, berserk, blunt_trauma])
doom_blade3 = Nanovor("Doom Blade 3.0", 130, 0, 40, 115, 255, "Velocitron", [doomserk, guillotine, blunt_trauma])

doom_mantis1 = Nanovor("Doom Mantis 1.0", 140, 0, 45, 105, 260, "Velocitron", [rapier_jab, flay, plasma_pound])
doom_mantis2 = Nanovor("Doom Mantis 2.0", 150, 0, 55, 120, 285, "Velocitron", [power_punt, fearsome_flay, splatter, yellow_spike])

doom_bringer1 = Nanovor("Doom Bringer 1.0", 145,  0, 45, 120, 270, "Velocitron", [gorgon_gaze, poison_spit, mag_hunter])

phase_stormer1 = Nanovor("Phase Stormer 1.0", 110, 0, 25, 95, 165, "Velocitron", [whammy, icy_sigh, yellow_spike])
phase_stormer2 = Nanovor("Phase Stormer 2.0", 120, 0, 35, 110, 235, "Velocitron", [slip_slash, ice_storm, windchill])
phase_stormer3 = Nanovor("Phase Stormer 3.0", 130, 0, 45, 120, 250, "Velocitron", [psychic_fade, disk_of_death, acid_bubble])

storm_spinner1 = Nanovor("Storm Spinner 1.0", 110, 5, 30, 100, 175, "Velocitron", [crystal_trap, spin_strike, yellow_spike])
storm_spinner2 = Nanovor("Storm Spinner 2.0", 125, 5, 40, 110, 245, "Velocitron", [reflex_zap, spin_strike, speed_demon])
storm_spinner3 = Nanovor("Storm Spinner 3.0", 135, 5, 50, 115, 280, "Velocitron", [slowdown, storm_strike, stormfire])

storm_hunter1 = Nanovor("Storm Hunter 1.0", 120, 0, 55, 120, 255, "Velocitron", [lotus_cut, stare_down, chained_fist])

megadoom1 = Nanovor("Megadoom 1.0", 150, 5, 55, 115, 270, "Velocitron", [slash, mega_boom, taser])

battle_phaser1 = Nanovor("Battle Phaser 1.0", 140, 0, 60, 115, 270, "Velocitron", [serpent_whip, fearful_hiss, phase_strike])

#HEXITES
spike_spine1 = Nanovor("Spike Spine 1.0", 90, 0, 45, 95, 170, "Hexite", [charge, power_rush, blue_spike])
spike_spine2 = Nanovor("Spike Spine 2.0", 105, 5, 60, 115, 235, "Hexite", [arcing_gore, pump_it_up, power_sink])
spike_spine3 = Nanovor("Spike Spine 3.0", 120, 10, 75, 130, 305, "Hexite", [slayer_sting, stormfield, spine_sting])

spike_hornet1 = Nanovor("Spike Hornet 1.0", 100, 0, 55, 100, 250, "Hexite", [slapstick, gutbuster, heckle])
spike_hornet2 = Nanovor("Spike Hornet 2.0", 110, 5, 65, 115, 295, "Hexite", [stinger, punchline, wisecrack])
spike_hornet3 = Nanovor("Spike Hornet 3.0", 125, 5, 70, 125, 315, "Hexite", [knock_knock, ventriloquist, pun_ish, riddle])

gigastriker1 = Nanovor("Gigastriker 1.0", 90, 0, 45, 95, 180, "Hexite", [gigazap, meltdownv2, blue_spike])
gigastriker2 = Nanovor("Gigastriker 2.0", 105, 5, 60, 110, 250, "Hexite", [gigazap, psychic_drain, psi_strike])
gigastriker3 = Nanovor("Gigastriker 3.0", 120, 5, 65, 120, 305, "Hexite", [psychic_drain, psi_burst, mind_strike])

giga_wing1 = Nanovor("Giga Wing 1.0", 110, 5, 80, 125, 275, "Hexite", [gob_smack, obliterate, smackdown])

giga_tangler1 = Nanovor("Giga Tangler 1.0", 125, 5, 65, 120, 270, "Hexite", [face_plant, rust, whirlwind])
giga_tangler2 = Nanovor("Giga Tangler 2.0", 135, 10, 75, 130, 365, "Hexite", [dash_smash, corrode, blendo, gigadrain])

giga_siren1 = Nanovor("Giga Siren 1.0", 120, 10, 70, 115, 280, "Hexite", [incinerate, siren_sphere, sonic_strike])

circuit_flyer1 = Nanovor("Circuit Flyer 1.0", 90, 0, 50, 90, 190, "Hexite", [pierce, power_surge, blue_spike])
circuit_flyer2 = Nanovor("Circuit Flyer 2.0", 100, 0, 55, 100, 270, "Hexite", [pierce, power_surge, dodge])
circuit_flyer3 = Nanovor("Circuit Flyer 3.0", 115, 5, 65, 110, 300, "Hexite", [short_circuit, power_surge, dodge])

battle_kraken1 = Nanovor("Battle Kraken 1.0", 95, 0, 55, 100, 175, "Hexite", [crunch, tangler, blue_spike])
battle_kraken2 = Nanovor("Battle Kraken 2.0", 115, 5, 65, 110, 230, "Hexite", [kraken_smack, tentacle_zap, fathom_blast])
battle_kraken3 = Nanovor("Battle Kraken 3.0", 130, 10, 70, 125, 275, "Hexite", [poison_darts, hack_zap, blue_blast])

mega_spike1 = Nanovor("Megaspike 1.0", 110, 5, 50, 125, 260, "Hexite", [zapper, zoomer, zinger])

phase_spiker1 = Nanovor("Phase Spiker 1.0", 105, 5, 55, 130, 265, "Hexite", [asp_kiss, energy_drain, flying_fang])

##### WAVE 2 #####

#MAGNAMODS
hyper_ripper1 = Nanovor("Hyper Ripper 1.0", 105, 5, 15, 110, 180, "Magnamod", [fireplow, hardshell, red_spike])
hyper_ripper2 = Nanovor("Hyper Ripper 2.0", 120, 5, 20, 120, 265, "Magnamod", [fireplow, dodge, lockdown])
hyper_ripper3 = Nanovor("Hyper Ripper 3.0", 135, 10, 25, 125, 275, "Magnamod", [torch, energy_bite, hyperburrow])

hyper_tusk1 = Nanovor("Hypertusk 1.0", 125, 10, 25, 125, 265, "Magnamod", [infection, hyperspeed, belch])
hyper_tusk2 = Nanovor("Hypertusk 2.0", 125, 10, 30, 140, 275, "Magnamod", [hyperbelch, poison_stench, tusk_tunnel])

hyperblade1 = Nanovor("Hyperblade 1.0", 140, 10, 30, 135, 275, "Magnamod", [frost, obliterate, hyperslash])

rumble_hound1 = Nanovor("Rumble Hound 1.0", 100, 5, 10, 105, 170, "Magnamod", [swipe, growl, red_spike])
rumble_hound2 = Nanovor("Rumble Hound 2.0", 120, 10, 15, 115, 275, "Magnamod", [breakthrough, howl, defense])

rumble_squid1 = Nanovor("Rumble Squid 1.0", 145, 10, 35, 140, 375, "Magnamod", [rumbler, blocker, eraser, stronger])

thunderpoid1 = Nanovor("Thunderpoid 1.0", 120, 5, 15, 100, 180, "Magnamod", [tangler, swat, red_spike])
thunderpoid2 = Nanovor("Thunderpoid 2.0", 130, 10, 20, 110, 245, "Magnamod", [entangle, thunderpower, swarm_shot])
thunderpoid3 = Nanovor("Thunderpoid 3.0", 140, 10, 25, 125, 275, "Magnamod", [grab, dodge, fireswarm])

thundercrab1 = Nanovor("Thundercrab 1.0", 105, 10, 10, 115, 245, "Magnamod", [pinch, clamp, hardshell])
thundercrab2 = Nanovor("Thundercrab 2.0", 115, 15, 15, 125, 290, "Magnamod", [whip, pincer, power_play, stunner])

psi_blaster1 = Nanovor("Psi Blaster 1.0", 120, 5, 20, 110, 210, "Magnamod", [psi_zap, think_fast, red_spike])
psi_blaster2 = Nanovor("Psi Blaster 2.0", 135, 10, 30, 130, 255, "Magnamod", [brain_freeze, obliterate, brain_storm, red_spike])

shock_rumbler1 = Nanovor("Shock Rumbler 1.0", 145, 5, 35, 110, 295, "Magnamod", [kickoff, shocker, rumble_pulse, static_boom])

war_thunderer1 = Nanovor("War Thunderer 1.0", 100, 5, 55, 70, 290, "Magnamod", [thunder, lightning, wardog, flash])

#VELOCITRONS
scarab_roller1 = Nanovor("Scarab Roller 1.0", 105, 0, 30, 90, 165, "Velocitron", [run_down, exhaust, yellow_spike])
scarab_roller2 = Nanovor("Scarab Roller 2.0", 115, 0, 40, 100, 225, "Velocitron", [run_down, backspin, spin_out])
scarab_roller3 = Nanovor("Scarab Roller 3.0", 130, 0, 45, 115, 245, "Velocitron", [run_over, eat_my_dust, ready_set_go])

scarab_spear1 = Nanovor("Scarab Spear 1.0", 125, 0, 40, 110, 250, "Velocitron", [spear, fireball, wise_up])
scarab_spear2 = Nanovor("Scarab Spear 2.0", 135, 0, 50, 120, 290, "Velocitron", [spazzle, electrospear, power_pulse, distract])

blaze_dragon1 = Nanovor("Blaze Dragon 1.0", 105, 0, 35, 90, 155, "Velocitron", [dragonfire, obliterate, yellow_spike])
blaze_dragon2 = Nanovor("Blaze Dragon 2.0", 110, 0, 35, 105, 240, "Velocitron", [scorchv2, flame_up, inferno])

blaze_hydra1 = Nanovor("Blaze Hydra 1.0", 125, 0, 40, 115, 235, "Velocitron", [frostbite, blazeburn, meditate])
blaze_hydra2 = Nanovor("Blaze Hydra 2.0", 135, 0, 50, 120, 305, "Velocitron", [fireclap, hypnotize, tantrum, hydra_slap])

turbo_cannon1 = Nanovor("Turbo Cannon 1.0", 110, 0, 30, 85, 165, "Velocitron", [avalanche, icicle_storm, yellow_spike])
turbo_cannon2 = Nanovor("Turbo Cannon 2.0", 120, 0, 40, 100, 245, "Velocitron", [poison_spray, stinkbomb, faster])
turbo_cannon3 = Nanovor("Turbo Cannon 3.0", 130, 0, 50, 110, 245, "Velocitron", [burn_down, hot_air, heat_wave])

turbo_jumper1 = Nanovor("Turbo Jumper 1.0", 110, 0, 45, 105, 240, "Velocitron", [bound, snapshot, crystal_maul, yellow_spike])

turbo_master1 = Nanovor("Turbo Master 1.0", 115, 0, 40, 110, 235, "Velocitron", [turbo_kick, speed_trade, fightspeed])

shock_hornet1 = Nanovor("Shock Hornet 1.0", 120, 0, 25, 90, 165, "Velocitron", [slow_down, shock_sting, yellow_spike])
shock_hornet2 = Nanovor("Shock Hornet 2.0", 130, 0, 30, 100, 230, "Velocitron", [poison_sting, poison_mist, shock_and_awe])

psi_scarab1 = Nanovor("Psi Scarab 1.0", 115, 10, 35, 120, 255, "Velocitron", [scarab_slash, tonguestrike, psi_cannon])

warblaze1 = Nanovor("Warblaze 1.0", 135, 5, 50, 115, 325, "Velocitron", [claw_smash, whiplash, crystal_flash, fire_splash])

#HEXITES
triton_manta1 = Nanovor("Triton Manta 1.0", 95, 0, 45, 95, 165, "Hexite", [triton_chomp, spitball, blue_spike])
triton_manta2 = Nanovor("Triton Manta 2.0", 105, 0, 50, 105, 235, "Hexite", [sting, spark_siphon, paralyze])
triton_manta3 = Nanovor("Triton Manta 3.0", 115, 5, 60, 115, 285, "Hexite", [sting, shockback, triton_strike])

triton_spider1 = Nanovor("Triton Spider 1.0", 100, 5, 45, 95, 240, "Hexite", [obliterate, fang_blast, snare])
triton_spider2 = Nanovor("Triton Spider 2.0", 120, 5, 55, 100, 260, "Hexite", [spiderbite, fang_blast, triton_tumble])

shard_slider1 = Nanovor("Shard Slider 1.0", 110, 0, 50, 100, 195, "Hexite", [shard_slice, jumpstart, blue_spike])
shard_slider2 = Nanovor("Shard Slider 2.0", 125, 5, 55, 110, 250, "Hexite", [slider, burn, weaken])
shard_slider3 = Nanovor("Shard Slider 3.0", 140, 10, 65, 125, 330, "Hexite", [shard_slice, blue_thunder, slide_by, shutdown])

shard_runner1 = Nanovor("Shard Runner 1.0", 115, 5, 60, 120, 210, "Hexite", [shard_smash, pummel, shard_blast, blue_spike])
shard_runner2 = Nanovor("Shard Runner 2.0", 130, 10, 70, 130, 370, "Hexite", [fire_smash, jumpstart, dodge, shard_shatter])

cyber_slicer1 = Nanovor("Cyber Slicer 1.0", 120, 0, 50, 110, 215, "Hexite", [crunchv2, random_jack, blue_spike])
cyber_slicer2 = Nanovor("Cyber Slicer 2.0", 130, 5, 55, 115, 240, "Hexite", [acid_burn, crashoverride, phreak])
cyber_slicer3 = Nanovor("Cyber Slicer 3.0", 140, 10, 65, 120, 315, "Hexite", [rip, dodge, whopper])

cyber_shark1 = Nanovor("Cyber Shark 1.0", 135, 5, 60, 120, 315, "Hexite", [thrash, cyber_shock, depth_charge])

war_charger1 = Nanovor("War Charger 1.0", 110, 10, 50, 100, 190, "Hexite", [battle_rush, war_dance, blue_spike])
war_charger2 = Nanovor("War Charger 2.0", 120, 10, 65, 115, 260, "Hexite", [pounce, chop_drop, battle_dance])

psi_shard1 = Nanovor("Psi Shard 1.0", 135, 5, 40, 110, 265, "Hexite", [psi_drain, breakthrough, driller])

shock_triton1 = Nanovor("Shock Triton 1.0", 135, 0, 45, 115, 300, "Hexite", [collider, whirlpool, triton_blast, shock_drain])

# FIXED: Change the apply_hacks and apply_spike_combo functions to be split into 2 functions each.
# One function for each will contain effects on self, the other will have effects on enemy
# This way, if an attack is dodged, the effects to self (such as stun or SPD decrease) will still be applied
# However, because the attack was dodged, the effect to the enemy is not applied. 

# FIXED: the swap functionality, make it set the defenders next nanovor to their
# current one if the swap effect is used, that way they won't be switched on
# that same turn.

#FIXED: THE DETERMINE ORDER FUNCTION!

#Solid Strike mechanics look good
#Mag Hunter mechanics look good
#Battle Kraken 3.0 Poison Darts mechanics look good
#Punchline mechanics look good
#Additional armor-piercing base damage mechanics (Doom Mantis 2.0, Tank Walker 3.0) look good
#Gutbuster mechanics look good 
#Incinerate, Giga Siren 1.0 mechanics look good
#Circuit Flyer 3.0 Short Circuit mechanics look good
#Phase Spiker 1.0 Flying Fang mechanics look good
#Doom Blade takes recoil if it attacks and its attack is dodged - looks good. 
#Triton Manta 3.0 Shockback mechanics look good
#Eraser Rumble Squid mechanics look good
#PowerPlay ThunderCrab 2.0 mechanics look good
#Shock Rumbler 1.0 Kickoff mechanics look good
#Scarab Spear 1.0's Wise Up mechanics look good 
#Spike Hornet 2.0's Wisecrack mechanics look good
#War Thunderer Lightning mechanics look good
#Psi Shard 1.0's Driller mechanics look good
#Cyber Slicer 1.0's Random Jack mechanics look good
#Shard Runner 1.0's Pummel mechanics look good
# - Is there an attack that ignores armor, but then with a spike combo, does higher damage that doesn't ignore armor?
#Shard Runner 2.0's Shard Shatter mechanics look good 
#Hyper Blade 1.0's Hyper Slash mechanics look good
# Battle Kraken 3.0's Hack Zap mechanics look good


### Testing Area ###

#NOTE: using copy.deepcopy to make a copy of the variable whenever a nanovor is used more than once in a match! 
# That way, when damage is done to one nanovor, it does not affect all the nanovor that have the same name

# CUSTOM NANOVOR
omni_spike = Attack("Omni Spike", 2, "Places an Override that allows your swarm to make either a Red, Blue, or Yellow Spiked attack. ", override=[True, {"SPIKE":"Spike"}])
spear_dash = Attack("Spear Dash", 2, "A damage attack that ignores armor", damage = [True, [25]],armorpiercing=True)
fierce_tempest = Attack("Fierce Tempest", 4 , "A ranged ice damage attack that also swap-blocks the opponent for this and the next round; With a Blue Spike override, the target is also stunned for 2 rounds.", damage = [True, [35]], hack=[True, {"SWAP":2}], combo=[True, {"STUN":2}], consumes=True)

gale_serpent1 = Nanovor("Gale Serpent 1.0", 115, 5, 60, 110, 235,"Hexite", [omni_spike,spear_dash,fierce_tempest])

socket_smack = Attack("Socket Smack", 1, "A damage attack.", damage = [True,[30]])
flash_shield = Attack("Flash Shield", 4, "Places a +5 ARM Override that also gives your Nanovor a 20% chance of dodging an enemy attack.", override=[True,{"DODGE":20,"ARM":5}])
voltage_charge = Attack("Voltage Charge", 3, "A damage attack that also removes the target's override", damage=[True,[30]], hack=[True, {"OBLIT":0}])

surge_protector1 = Nanovor("Surge Protector 1.0", 130,10,20,120,240,"Magnamod", [socket_smack,flash_shield,voltage_charge])

thunder2 = Attack("Thunder", 2, "A damage attack, with a Blue Spike Override the opponent loses 3 Energy", damage = [True, [30]], combo = [True, {"ENSAP":3}], consumes=True)
lightning2 = Attack("Lightning", 3, "A damage attack; with a Red Spike override, gain a 15 Strength Override", damage = [True, [50]], combo = [True, {"SETNEW": {"STR":15}}])
wardog2 = Attack("Wardog", 4, "An energy damage attack and the target Nanovor loses 5 Armor", damage = [True, [50]], hack = [True, {"ARM":5}])
flash2 = Attack("Flash", 4, "An attack that swap-blocks the target for this and the next 2 rounds and takes away 15 Strength", hack = [True, {"SWAP":3, "STR":15}])

war_thunderer1_v2 = Nanovor("War Thunderer 1.0v2",125,10,35,130,300,"Magnamod", [thunder2, lightning2, wardog2, flash2])


MAGNAMOD_LIST = [electropod1,electropod2,electropod3,electrobull1,electrobull2,electro_shield1,tank_walker1,tank_walker2,tank_walker3,tank_strider1,tank_strider2,
                 gamma_stalker1,gamma_stalker2,gamma_stalker3,gamma_fury1,gamma_fury2,mega_scorpion1,mega_scorpion2,phase_tank1,circuit_tank1,hyper_ripper1,
                 hyper_ripper2,hyper_ripper3,hyper_tusk1,hyper_tusk2,hyperblade1,rumble_hound1,rumble_hound2,rumble_squid1,thunderpoid1,thunderpoid2,thunderpoid3,
                 thundercrab1,thundercrab2,psi_blaster1,psi_blaster2,shock_rumbler1,war_thunderer1]
VELOCITRON_LIST = [plasma_lash1,plasma_lash2,plasma_lash3,plasma_locust1,plasma_locust2,plasma_locust3,plasma_lancer1,doom_blade1,doom_blade2,doom_blade3,doom_mantis1,
                   doom_mantis2,doom_bringer1,phase_stormer1,phase_stormer2,phase_stormer3,storm_spinner1,storm_spinner2,storm_spinner3,storm_hunter1,megadoom1,battle_phaser1,
                   scarab_roller1,scarab_roller2,scarab_roller3,scarab_spear1,scarab_spear2,blaze_dragon1,blaze_dragon2,blaze_hydra1,blaze_hydra2,turbo_cannon1,turbo_cannon2,
                   turbo_cannon3,turbo_jumper1,turbo_master1,shock_hornet1,shock_hornet2,psi_scarab1,warblaze1]
HEXITE_LIST = [spike_spine1,spike_spine2,spike_spine3,spike_hornet1,spike_hornet2,spike_hornet3,gigastriker1,gigastriker2,gigastriker3,giga_wing1,giga_tangler1,giga_tangler2,
              giga_siren1,circuit_flyer1,circuit_flyer2,circuit_flyer3,battle_kraken1,battle_kraken2,battle_kraken3,mega_spike1,phase_spiker1,triton_manta1,triton_manta2,
              triton_manta3,triton_spider1,triton_spider2,shard_slider1,shard_slider2,shard_slider3,shard_runner1,shard_runner2,cyber_slicer1,cyber_slicer2,cyber_slicer3,
              cyber_shark1,war_charger1,war_charger2,psi_shard1,shock_triton1]
CUSTOM_LIST = [gale_serpent1, surge_protector1, war_thunderer1_v2]

COMPLETE_LIST = MAGNAMOD_LIST+VELOCITRON_LIST+HEXITE_LIST+CUSTOM_LIST