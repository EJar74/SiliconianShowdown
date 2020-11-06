'''
                        Computer
                A       B       C       PASS
            A [30,30   30,20    30,80  30,10]
            B |10,30   10,20    10,80  10,10|
Player 1    C |50,30   50,20    50,80  50,10|
            D |25,30   25,20    25,80  25,10|
         PASS [10,30   10,20    10,80  10,10]

    Where A,B,C,D on the rows represent 4 attacks that Player 1 can choose to use, or the PASS option, all of which provide a certain amount of value.
    Likewise, the computer can choose to use one of A,B,C, or PASS, all of which provide different values.
    I am going to be using the maximin strategy for the computer, so that it gets the best out of the worst possible outcome. Lets examine that here.

    I may have to revise the way I set up the matrices, because the way this one was set up was simply by getting the value that each attack would
    provide to each player and adding that value to the entire row or column. What I should maybe do though, is subtract the values from each other in each
    index to get a sum value for each player. For instance, if both players pass, both receive a value of 0 instead of 10. If The computer chooses to pass and
    Player 1 uses attack C, then perhaps the computers value for pass should be -40 instead of 10. This would truly take into account each individual attack.

    Or, we could just measure the positive impact of the opponent using a certain attack to determine which one would be most debilitating to us.

    So, lets try applying the maximin strategy here for the computer. The computer looks and sees that Attack C would be the most beneficial for Player 1, because
    it provides a value of 50. In turn, this means that Attack C would provide the worst outcome for the Computer. The Computer recognizes this, and says, "Ok,
    let's assume this player is rational and is going to go with Attack C, how can I maximize my value with that in mind? The Computer checks out the column values in
    row C, and finds that attack C would give it the best outcome, one of 80. It just so happens that this attack would give it the most value anyways. Thus, the Computer
    goes with attack C. Player 1 may figure that the Computer will use attack C and elects to take the damage and pass. We end up at a value of (10,80) at (PASS,C).

    The issue I see here is that the attacks and their values are independent across each player, what if we try rewriting the matrix with the values of each attack as
    the result from taking the difference of the two?

                            Computer
               A       B       C      PASS
            A [0,0     10,-10  -50,50  20,-20]
            B |-20,20  -10,10  -70,70     0,0|
Player 1    C |20,-20  30,-30  -30,30  40,-40|
            D |-5,5     5,-5   -55,55  15,-15|
         PASS [-20,20  -10,10  -70,70     0,0]

    Here, the worst case scenario still occurs when Player 1 opts to use Attack C, yielding the Computer a lowest value of -40 if the Computer opts to pass. The Computer assumes
    that the player will go with Attack C, so to maximize its own value, the Computer opts to use attack C as well, and we would get the same exact outcome as we did in the
    original one. I think this is because in the original one, we do take into account the opponent's attacks when the computer examines the players best value output and makes
    a decision based on that.
'''
# from NanovorCollection import *
# from PlayerClass import Player
# import copy
import random

def pick_swarm():
    swarm1 = ["Plasma Lash 2.0", "Doom Blade 3.0", "Doom Blade 3.0", "Doom Blade 3.0"]
    swarm2 = ["Plasma Lash 1.0", "Electropod 2.0", "Tank Walker 3.0", "Cyber Shark 1.0"]
    swarm3 = ["Electropod 3.0", "Electropod 3.0", "Tank Strider 2.0"]
    swarm4 = ["Blaze Dragon 1.0", "Plasma Locust 3.0", "Megadoom 1.0", "Doom Mantis 2.0"]
    swarm5 = ["Spike Spine 3.0", "Rumble Squid 1.0", "Blaze Hydra 2.0"]
    swarm6 = ["Electropod 1.0", "Psi Blaster 2.0", "Phase Tank 1.0", "Phase Tank 1.0"]

    all_swarms = [swarm1] + [swarm2] + [swarm3] + [swarm4] + [swarm5] + [swarm6]

    return random.choice(all_swarms)

def calculate_value(attack,player,target):
    value = 0
    STR_MULT = player.get_current_nanovor().get_strength() / 100
    EN_BONUS = 30

    if attack.get_damage():
        value += ((attack.get_damage()[0] * STR_MULT - target.get_current_nanovor().get_armor()) / target.get_current_nanovor().get_health() * 100)
        value = 100 + (EN_BONUS / attack.get_cost()) if value >= 100 else (100 if value >= 50 else value)
        value = 0 if attack.get_cost() > player.get_energy() else value

    return value

def fill_matrix(player,computer):
    enemy_active = player.get_current_nanovor()
    cpu_active = computer.get_current_nanovor()
    matrix = []

    for attack in enemy_active.get_attacks():
        matrix.append([])
        for atk in cpu_active.get_attacks():
            matrix[-1].append([calculate_value(attack,player,computer), calculate_value(atk,computer,player)])

    # print(matrix)
    return matrix

def decide(matrix):
    decision = 0
    max = 0
    enemy_dec = 0
    for i, row in enumerate(matrix):
        for col in row:
            if col[0] > max:
                max = col[0]
                enemy_dec = i
    # print(enemy_dec, max)
    max = 0
    for i, col in enumerate(matrix[enemy_dec]):
        if col[1] > max:
            max = col[1]
            decision = i
    # print(decision, max)
    return decision
