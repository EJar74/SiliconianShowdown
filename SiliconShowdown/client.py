from tkinter import *
import tkinter.messagebox
import time
from collections import defaultdict
import threading
import random
import socket
import pickle


class Network:

    def __init__(self):
        self.port = 50500
        self.server =  socket.gethostbyname(socket.gethostname())
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Lobbynum will be a str digit corresponding to the button the user pressed for the lobby they wish to enter
    def enterLobby(self, lobbynum,username):
        self.client.connect((self.server,self.port))
        self.client.send(pickle.dumps((lobbynum, username)))
        entrance_message = pickle.loads(self.client.recv(4096))
        print(entrance_message)

    def send_message(self, msg):
        self.client.send(pickle.dumps(msg))
        return pickle.loads(self.client.recv(4096*8))


class TurnTimer:
    def __init__(self, GUI):
        self.running = True
        self.GUI = GUI
        self.timer = threading.Thread(target=self.run, daemon=True)

    def run(self):
        countdown = 180
        while countdown > 0:
            if not self.running:
                return
            time.sleep(1)
            countdown -= 1
            self.GUI.timer.configure(text=f"Select Attack in: {countdown//60}:{countdown%60:02}")

        else:
            self.GUI.active = 0 if self.GUI.active is None else self.GUI.active
            self.GUI.next = self.GUI.active
            self.GUI.attack = "PASS"
            self.GUI.target = None
            self.GUI.send_selections()

    def start(self):
        self.timer.start()

    def stop(self):
        self.running = False


class ClientGUI:

    def __init__(self, root):

        self.window = root

        self.connection = Network()

        self.complete_list = []

        self.starting_swarm = []

        self.username = ''

        self.timer = tkinter.Label(self.window, bg="gold", font="Sans 12 bold")

        #Dict with strings of carnage report, and player's nanovor stats
        self.round_summary = {}
        #Dict with Stats and ActiveIDX as keys
        self.active_nanovor = {}
        # {Index:String, ...}
        self.swarm = {}
        #{Index:{String AttackName: String AttackDesc}}
        self.attacks = {}
        #{Index:[String Enemy Name, String Active Nanovor Stats]}
        self.enemies = {}
        #Dict containing EN and Overrides for all players: {Index: {EN:Int, Override:String}}
        self.energy_overrides = {}
        #{Index: [String NanoHP]}
        self.all_swarms = {}
        #Dict, {Index: [ (AttkName, AttkDesc) ]}, with AttName having EN Cost and DMG if applicable
        self.enemy_attacks = {}

        #Ints that will be sent back to the server, specifying player's choices as indexes
        self.active = None
        self.next = None
        #String sent back to the server, specifying what attack the player chose (the name of the attack)
        self.attack = ''
        #Int that will be sent back to the server, specifying index of target in the opponent list
        self.target = None
        #Toggled so that the default swap is "No Swap"
        self.toggle_swap = False
        self.toggle_var = IntVar()

        self.onlineBattle()

    def elimination_screen(self):
        self.refresh_window(self.window)
        message_frame = tkinter.Frame(self.window, bg="silver")
        message_frame.pack(pady=30)
        message = tkinter.Label(self.window, text="You were eliminated from the game! Better luck next time!\n There is currently no feature to allow spectators for the rest of the match, but there are plans for that in the future.\n For now, press the button below to return to the main menu!",
                                bg="black", fg="white")
        message.pack(padx=2,pady=2)
        returnhome = Button(self.window, text= "<== Main Menu", command= lambda: self.__init__(self.window))
        returnhome.pack(ipadx=5,ipady=5)

    def onlineBattle(self):

        self.refresh_window(self.window)

        announce_frame = tkinter.Frame(self.window, bg="dark goldenrod")
        announce_frame.pack(pady=30)

        announce = tkinter.Label(announce_frame,
                                 text="Welcome to the lobby of Vor: Siliconian Showdown\'s online battle feature!\nThis app is still experimental, so if you run into any issues, please report them in detail so that they can be patched up ASAP.\nChoose an option below for multiplayer!",
                                 fg="white", bg = "black")
        announce.pack(padx=2,pady=2)

        name_frame = tkinter.Frame(self.window, bg="silver")
        name_frame.pack(pady=15)

        name_message = tkinter.Label(name_frame, text="Please enter your username: ",bg="black", fg="white")
        name_message.pack(pady=2,padx=2)

        username = Entry(self.window, width=10)
        username.pack(pady=5, padx=5)

        sel_frame = tkinter.Frame(self.window, bg="silver")
        sel_frame.pack(pady=5)

        player_selection = tkinter.Label(sel_frame, text="Please select match size (players): ", bg="black", fg="white")
        player_selection.pack(padx=2,pady=2)

        spin = Spinbox(self.window, from_=1, to=4, width=5, state='readonly')
        spin.pack(padx=5, pady=5)

        conf_players = Button(self.window, text="Confirm",command = lambda:self.confirmGame(spin.get(), username.get()))
        conf_players.pack(pady=10,ipadx=5,ipady=5)

        how_to = tkinter.Button(self.window, text="How to Play",width=10,height=2, command = self.instructions)
        how_to.pack(pady=50)

        tkinter.Label(self.window, text="(Version 1.0 Beta)", bg="black", fg="white").pack()

        credit_frame = tkinter.Frame(self.window, bg="dark goldenrod")
        credit_frame.pack(side=BOTTOM,fill=X)

        credit = tkinter.Label(credit_frame,text="Siliconian Showdown was created and developed by Felneus, and does not claim to own any of the intellectual property belonging to Smith & Tinker.\n\
                               For questions, comments or concerns, you can reach me at Felneus#1101 on Discord.\n\
                               Be sure to join our Nanovor 2.0 community to stay up to date on the latest progress of the revival of the original game!\n\
                               You can join our Discord at https://discord.gg/HZ3GmdM or check out r/NanovorFans or the Nanovor Wikia!\n\
                               Happy Splatting!", bg="black", fg="white")
        credit.pack(padx=2,pady=2,fill=X)

    def instructions(self):
        self.refresh_window(self.window)

        scroll = Scrollbar(self.window)
        scroll.pack(side=RIGHT,fill=Y)

        report = Text(self.window,wrap=WORD,yscrollcommand=scroll.set)
        report.pack(fill=BOTH)

        scroll.config(command=report.yview)

        report.insert(END, INSTRUCTIONS)
        report.config(bd=2, state=DISABLED, relief=SOLID, bg="SteelBlue3", font="Sans 12 bold", highlightbackground="dark goldenrod")

        back = tkinter.Button(self.window, text="OK", width =10,command=self.onlineBattle)
        back.pack()

    def all_children(self, window):
        _list = window.winfo_children()

        for item in _list:
            if item.winfo_children():
                _list.extend(item.winfo_children())

        return _list

    def refresh_window(self, window):
        widget_list = self.all_children(window)
        for item in widget_list:
            if item is self.timer:
                continue
            item.destroy()

    def confirmGame(self, num, username):
        if username == '':
            tkinter.messagebox.showwarning("Notification", "Please enter a username")
        elif len(username) > 20:
            tkinter.messagebox.showwarning("Notification", "Username cannot be longer than 20 characters")
        elif num == '':
            tkinter.messagebox.showwarning("Notification", "Please select a lobby size to join")
        else:
            answer = tkinter.messagebox.askquestion("Confirmation",
                                                    "Are you sure you want to join a {} player battle?".format(num))
            if answer == "yes":
                self.username = username
                self.connection.enterLobby(num, username)
                self.checkStatus()

    def checkStatus(self):
        waiting = True
        while waiting:
            #Send a check request every 5 seconds
            time.sleep(1)
            checked = self.connection.send_message("Check Status")
            if checked == "Waiting on more players":
                print("Match still hasn't been found.")
            elif checked == "Match is starting!":
                print("Match found!")
                break
        self.swarmSelection()

    def swarmSelection(self):
        self.refresh_window(self.window)
        mag_list = self.connection.send_message("GetMags")
        vel_list = self.connection.send_message("GetVels")
        hex_list = self.connection.send_message("GetHexs")
        cust_list = self.connection.send_message("GetCust")

        self.complete_list += (mag_list + vel_list + hex_list + cust_list)

        selection = tkinter.Label(self.window,height=5,font="Sans 15 bold", bg ="dark goldenrod", bd=5,relief=RAISED,
                          text="Please build your swarm from the following drop-down menus. Nanovor are categorized by their class, and you can have a swarm with a maximum value of 1000.")
        selection.pack(pady=50)

        main_frame = Frame(self.window)
        main_frame.pack()

        magnamod_names = ["{}     (SV: {})".format(nano[0], nano[1]) for nano in mag_list]
        velocitron_names = ["{}     (SV: {})".format(nano[0], nano[1]) for nano in vel_list]
        hexite_names = ["{}     (SV: {})".format(nano[0], nano[1]) for nano in hex_list]
        custom_names = ["{}     (SV: {})".format(nano[0], nano[1]) for nano in cust_list]

        sel_list = [StringVar(self.window),StringVar(self.window),StringVar(self.window), StringVar(self.window)]
        nanovor_names = [magnamod_names, velocitron_names, hexite_names, custom_names]
        for i,var in enumerate(sel_list):
            var.set(nanovor_names[i][0] if nanovor_names[i] else '')
        class_names = ["Magnamods", "Velocitrons", "Hexites", "Custom"]
        colors = ["firebrick3", "goldenrod", "royal blue", "MediumPurple3"]
        quad_list,nameLabels,optionMenus,addButtons = [],[],[],[]

        for i in range(4 if cust_list else 3):
            quad_list.append(tkinter.Frame(main_frame,borderwidth=5,relief=SOLID,bg=colors[i]))
            quad_list[i].pack(pady=5,padx=10,side=LEFT)

            nameLabels.append(tkinter.Label(quad_list[i], text=class_names[i], bg="black",fg=colors[i],font="Sans 14 bold italic",borderwidth=2, relief=SUNKEN))
            nameLabels[i].pack(padx=5, pady=15)
            #Drop Down Menu
            optionMenus.append(OptionMenu(quad_list[i], sel_list[i], *nanovor_names[i]))
            optionMenus[i].pack(padx=5, pady=5)

            addButtons.append(tkinter.Button(quad_list[i], text="Add to Swarm", foreground="green",
                                     command=lambda i=i: self.add_to_Swarm(sel_list[i].get())))
            addButtons[i].pack(padx=5, pady=5,ipadx=3,ipady=3)

        # Confirm button to go on to the next player
        finalize = Button(self.window, text="Finalize Swarm", height=2, command = self.finalizeSwarm)
        finalize.pack(pady=20)

        tracker_frame = tkinter.Frame(self.window, background="dark goldenrod")
        tracker_frame.pack(pady=10)

        tracker = tkinter.Label(tracker_frame, text= "Current Swarm",font="Sans 14", bg="black", fg="white")
        tracker.pack(pady=2,padx=2)

        randomize = tkinter.Button(self.window, text="Randomize", command = self.randomSwarmGenerator)
        randomize.pack(pady=10,ipadx=3,ipady=3)

        self.swarm_frame = tkinter.Frame(self.window, bg="black")
        self.swarm_frame.pack()

        swarm_status = tkinter.Frame(self.window, bg="dark goldenrod")
        swarm_status.pack(pady=10)

        self.swarm_status = tkinter.Label(swarm_status,text=f"Current Swarm Value: 0 / 1000", font="Sans 14", bg="black", fg="white")
        self.swarm_status.pack(pady=2,padx=2)

        self.player_sv = 0

    def add_to_Swarm(self, chosen):
        idx = [nanovor[0] for nanovor in self.complete_list].index(chosen.split("     ")[0])
        if self.complete_list[idx][1] + self.player_sv <= 1000:
            self.starting_swarm.append(chosen.split("     ")[0])
            self.player_sv += self.complete_list[idx][1]

            nano_frame = tkinter.Frame(self.swarm_frame, bg="dark goldenrod", bd=2, relief=SOLID)
            nano_frame.pack(side=LEFT)

            nano_name = tkinter.Label(nano_frame, text=chosen.split("     ")[0], width=15)
            nano_name.pack(padx=2, pady=2)

            remove = tkinter.Button(nano_frame, text="X", fg="red", width=3, command=lambda idx=idx: [nano_frame.destroy(), self.remove_from_Swarm(idx)])
            remove.pack()
        else:
            return

        self.swarm_status.configure(text=f"Current Swarm Value: {self.player_sv} / 1000")

    def remove_from_Swarm(self, chosen):
        self.starting_swarm.remove(self.complete_list[chosen][0])
        self.player_sv -= self.complete_list[chosen][1]

        self.swarm_status.configure(text=f"Current Swarm Value: {self.player_sv} / 1000")

    def randomSwarmGenerator(self):
        MAX = 1000
        swarm, sv = [], []
        curr = 0

        while curr != MAX:
            base = random.randint(0, len(self.complete_list) - 1)
            chosen = self.complete_list[base]
            swarm.append(chosen[0])
            sv.append(chosen[1])
            curr += chosen[1]

            if (curr > MAX or curr < MAX) and curr > 380:
                curr -= sv[1]
                swarm.pop(1)
                sv.pop(1)

            if MAX - curr >= 155:
                options = [nanovor for nanovor in self.complete_list if nanovor[1] <= (MAX - curr)]
                picked = options[random.randint(0, len(options) - 1)]
                swarm.append(picked[0])
                sv.append(picked[1])
                curr += picked[1]

        for widget in self.all_children(self.swarm_frame):
            widget.destroy()
        if self.starting_swarm:
            for nano in self.starting_swarm[:]:
                self.remove_from_Swarm([nanovor[0] for nanovor in self.complete_list].index(nano))
        for nano in swarm:
            self.add_to_Swarm(nano)

    def finalizeSwarm(self):
        answer = tkinter.messagebox.askquestion("Swarm Confirmation",
                                                "Are you sure you want to finalize your swarm? You will not be able to make changes to it later.")
        if answer == "yes":
            # Make sure the player has selected at least one Nanovor. If not,the message will close but changes will not have been made. Will repeat until @ least 1 'vor is added
            if len(self.starting_swarm) > 0:
                self.connection.send_message(["SwarmSelected", self.starting_swarm])
                self.readyUp()
            else:
                tkinter.messagebox.showwarning("Notification", "You must have at least one Nanovor in your Swarm")

    def readyUp(self):
        while True:
            time.sleep(1)
            ready = self.connection.send_message("Match Status")
            if ready:
                break
            print("Not ready")
        #Is returned a method, so it receives that method and then calls it.
        self.gameLoop()()

    def gameLoop(self):
        game_over = self.connection.send_message("Game Ongoing")
        #For games with more than 2 players, check if you were eliminated, and if so, leave game (No spectating available for now)
        #If the message is not you were eliminated, its because the game was over anyways, and that takes precedence server-side
        #So even if you were eliminated and the game is over as a result, you will receive a message other than "You were eliminated"
        if game_over == "You were eliminated!":
            return self.elimination_screen
        #If False, continue to next round. If game_over is a string or dict returned from game, game is finished.
        elif not game_over:

            self.active_nanovor = self.connection.send_message("Get Active Nanovor")
            self.swarm = self.connection.send_message("Get Player Swarm")
            self.attacks = self.connection.send_message("Get Player Attacks")
            self.enemies = self.connection.send_message("Get Opponent Active")
            self.energy_overrides = self.connection.send_message("Energy & Overrides")
            self.all_swarms = self.connection.send_message("Get All Swarms")
            self.enemy_attacks = self.connection.send_message("Get Opponent Attacks")
            print("Received all messages")
            #Reset these because it's a new round (you're going to run into issues where the CPU remembers last rounds choices otherwise)
            #Set active to the index of the active nanovor to keep track of what happened (see if your swap worked or was blocked)
            self.target,self.attack = None,''
            self.active = self.active_nanovor["ActiveIDX"]
            self.next = self.active if self.toggle_swap and self.active != '' else None

            self.t = TurnTimer(self)
            self.t.start()

            return self.battle_screen

        else:
            return lambda:self.display_gameOver(game_over)

    def squad_screen(self, choose_active = False):
        self.refresh_window(self.window)
        swarm_frames, nano_labels = [], []
        attack_frames, descriptions = defaultdict(list), defaultdict(list)

        self.timer.place(rely=0, relx=0.86)

        height = self.window.winfo_height()
        width = self.window.winfo_width()
        player_width = (width - 40 - 20 * len(self.swarm) * 2) // len(self.swarm)

        tkinter.Frame(self.window, bg="dark goldenrod", height=height, width=20).pack(side=LEFT, fill=Y)
        tkinter.Frame(self.window, bg="dark goldenrod", height=height, width=20).pack(side=RIGHT, fill=Y)

        def swapper(index):
            for i, label in enumerate(nano_labels):
                if i == index:
                    label.configure(bg="gold")
                    # If choose_active is False, it means the player is neither starting their first turn nor had their active nanovor last turn get splatted.
                    #player.set_next_nanovor(player.get_swarm()[index]) if not choose_active else player.set_current_nanovor(player.get_swarm()[index])
                    if choose_active:
                        self.active = index
                        self.active_nanovor["Stats"] = self.swarm[index]
                        self.next = self.active if self.toggle_swap else self.next
                    else:
                        self.next = index
                else:
                    label.configure(bg="#2a6570")

        #Sort the dict so that the keys are in order (since they are indices). Might want to change this to a list as a result since a list keeps its order.
        #It seems that the dict actually maintains the key insertion order now though? Since Python 3.6 in fact, huh.
        for i, nano in self.swarm.items():
            swarm_frames.append(tkinter.Frame(self.window))
            swarm_frames[i].pack(side=LEFT, anchor=N, padx=12, pady=30, expand=True, fill=X)

            nano_frame = tkinter.LabelFrame(swarm_frames[i],
                                            text="CURRENTLY ACTIVE" if i == self.active else ' ',
                                            bg="gold", font="Sans 12 bold")
            nano_frame.pack(fill=X)

            nano_labels.append(tkinter.Label(nano_frame, text=nano,
                                             bg="gold" if i == self.next else "#2a6570",
                                             font="Sans 12 bold", bd=2, relief=SOLID))
            nano_labels[i].pack(fill=X)
            nano_labels[i].bind("<Button-1>", lambda e, i=i: swapper(i))

            for j, (att_name, att_desc) in enumerate(self.attacks[i]):
                name, dmg = att_name.split("EN")[0] + " EN", att_name.split("EN")[1] if len(att_name.split("EN")) > 1 else ''
                attack_frames[i].append(
                    tkinter.LabelFrame(swarm_frames[i], text= name, bg="SteelBlue3", font="Sans 12 bold", width=player_width, height=130))
                attack_frames[i][j].pack(expand=True, fill=X)
                attack_frames[i][j].pack_propagate(0)

                descriptions[i].append(tkinter.Label(attack_frames[i][j], text=att_desc + dmg, wraplength=175, bg="SteelBlue3"))
                descriptions[i][j].pack()

        instructions = tkinter.Label(self.window,
                                     text=f"{self.username}, please select a Nanovor to be your active Nanovor." if choose_active else f"{self.username}, please select a Nanovor to swap in next turn.",
                                     font="Sans 12 bold")
        instructions.place(relx=.35)

        confirm = tkinter.Button(self.window, text="Confirm", height=2, command=self.battle_screen)
        confirm.place(rely=.9, relx=.5)

    def battle_screen(self):

        if "SV" not in self.active_nanovor["Stats"]:
            self.squad_screen(choose_active=True)
            return

        self.refresh_window(self.window)
        num = len(self.enemies) + 1
        #Add on the enemy active Nanovor attacks to the clients active Nanovor attacks. Keys are indexes, values are another dict with attkname as keys and desc as values
        curr_list = {0: self.attacks[self.active]}
        curr_list.update(self.enemy_attacks)
        #Need to fix self.enemies to make it less nasty, but this is grabbing the indeces from there and also the nanovor stats (the value, key is the username, we dont need it)
        curr_nanos = {0: self.active_nanovor["Stats"]}
        curr_nanos.update({idx: nanoStats[1] for idx, nanoStats in self.enemies.items()})
        #Set the next nanovor index to the same as the current nanovor index if the client is swap blocked or if they're down to their last Nanovor. Else, set it to itself (no change)
        self.next = self.active if len(self.swarm) == 1 or "Swap Blocked" in self.active_nanovor["Stats"] else self.next
        #Save the list of pure overrides to this variable to make our lives easier later on (shorter notation)
        pure_overrides = self.energy_overrides[0]['Pure'][self.active]

        height = self.window.winfo_height()
        width = self.window.winfo_width()
        player_width = (width - 40 - 20 * num * 2) // num

        player_frames, player_headers, usernames, energy, swarm, override, stats_frames, stats = [],[],[],[],[],[],[],[]
        move_butts, attackDict, swarm_dict = defaultdict(list), defaultdict(list), defaultdict(list)

        tkinter.Frame(self.window, bg="dark goldenrod", height=height, width=20).pack(side=LEFT, fill=Y)
        tkinter.Frame(self.window, bg="dark goldenrod", height=height, width=20).pack(side=RIGHT, fill=Y)

        for i in range(num):
            player_frames.append(tkinter.Frame(self.window, height=height, width=player_width, bg="black"))
            player_frames[i].pack(side=LEFT, anchor=N, padx=20, pady=40, expand=True, fill=X)

            player_headers.append(tkinter.Frame(player_frames[i], bg="white"))
            player_headers[i].pack(fill=X, expand=True)

            #First element in self.enemies is the username of that opponent, with the second element, index 1, being their active Nanovor's stats
            usernames.append(tkinter.Label(player_headers[i], text=f"{self.username if i == 0 else self.enemies[i][0]}",font="Sans 12 bold", bg="black", fg="white", bd=2))
            usernames[i].pack(fill=X, anchor=NW, padx=3, pady=3)

            left_header = tkinter.Frame(player_headers[i], bd=2, relief=SOLID)
            left_header.pack(side=LEFT, expand=True, fill=X)

            right_header = tkinter.Frame(player_headers[i], bd=2, relief=SOLID)
            right_header.pack(side=RIGHT, expand=True, fill=X)

            override.append(tkinter.Label(left_header, text=f"OVERRIDE\n{self.energy_overrides[i]['Override']}", bg="gray69", font="Sans 12 bold"))
            override[i].pack(fill=X)

            energy.append(tkinter.Label(right_header, text=f"ENERGY\n{self.energy_overrides[i]['EN']}", bg="gold", font="Sans 12 bold"))
            energy[i].pack(fill=X)

            swarm.append(tkinter.Frame(player_frames[i],bg="#2a6570"))
            swarm[i].pack(expand=True, fill=X)

            #Nano has already been handled in onlineGame where it is either a ? if not revealed or name/HP otherwise. Also sorted, ? left-most.
            for j, nano in enumerate(self.all_swarms[i]):
                swarm_dict[i].append(tkinter.Label(swarm[i], bg="#2a6570", bd=2, relief=SOLID))
                swarm_dict[i][j].pack(side=LEFT, fill=X, expand=True)
                swarm_dict[i][j].bind("<Enter>", lambda e, i=i, j=j, nano=nano: swarm_dict[i][j].configure(text=nano,fg="white"))
                swarm_dict[i][j].bind("<Leave>", lambda e, i=i, j=j, nano=nano: swarm_dict[i][j].configure(text=''))
                # swarm_dict[i][j].bind("<Enter>", lambda e, i=i, j=j: tkinter.Label(self._window, text="War Thunderer 1.0\nHP:50/105").place(x = swarm_dict[i][j].winfo_rootx() - 10, y= swarm_dict[i][j].winfo_rooty()-20))
                # swarm_dict[i][j].bind("<Leave>", lambda e, i=i, j=j: print([widget for widget in self.all_children(self._window) if isinstance(widget, tkinter.Label)]))

        def move(player,index,att_name):
            if player != 0:
                return

            for idx, attackFrame in enumerate(attackDict[player]):
                if idx == index:
                    attackFrame.configure(bg="gold")
                    #Make sure it's not the last frame in the list, i.e., the "Skip Turn" frame. If not, set the appropriate attack. Else, set to PASS.
                    if attackFrame is not attackDict[player][-1]:
                        self.attack = att_name.split("        ")[0]
                        stats[0].configure(bg="white")
                    else:
                        self.attack = "PASS"
                    #If the attack chosen is a pure override, or if player chose to PASS, no target needed, all backgrounds become white.
                    if self.attack in pure_overrides + ["PASS"]:
                        self.target = None
                        for pos,label in enumerate(stats):
                            stats[pos].configure(bg="white")
                        stats[0].configure(bg="sky blue" if self.attack != "PASS" else "white")
                else:
                    attackFrame.configure(bg="#126b94")

        def target(index):
            if self.attack in pure_overrides + ["PASS"]:
                return
            for i in curr_list.keys():
                if i == index:
                    stats[i].configure(bg="pink")
                    self.target = index
                else:
                    stats[i].configure(bg="white")

        def checker():
            if self.next is None:
                tkinter.messagebox.showwarning("Notice", "Please queue a Nanovor for swapping (select the currently active one for no swap)")
            elif self.attack == '':
                tkinter.messagebox.showwarning("Notice", "Please select an attack, or \"Skip Turn\"")
            elif self.target is None and self.attack != "PASS" and self.attack not in pure_overrides:
                tkinter.messagebox.showwarning("Notice", "Please select an opponent to attack (or select an override as your move).")
            else:
                self.t.stop()
                confirm.configure(state=DISABLED)
                swapper.configure(state=DISABLED)
                report_screen.configure(state=DISABLED)
                sender = threading.Thread(target=self.send_selections)
                sender.start()

        for i, att_pairs in curr_list.items():
            vheight = ((height + 16) / 9 * 4) / len(att_pairs)
            for index, (att_name, att_desc) in enumerate(att_pairs):

                attackDict[i].append(tkinter.Frame(player_frames[i], bg="#7f0002" if i != 0 else ("gold" if self.attack == att_name.split("        ")[0] else "#126b94"), bd=2,height=vheight, width=player_width,relief=SOLID))
                attackDict[i][index].pack(expand=True, fill=X)
                attackDict[i][index].pack_propagate(0)

                move_butts[i].append(tkinter.Button(attackDict[i][index], text=att_name,height=2, width=18,command=lambda index=index, i=i, att_name=att_name: move(i,index, att_name)))
                move_butts[i][index].pack(anchor=W,ipady=4)
                # place(rely=.85 if len(attackDict[i]) > 4 else .70,anchor=W)
                move_butts[i][index].bind("<Enter>", lambda e, index=index, i=i, att_desc=att_desc: tkinter.Label(attackDict[i][index],text=att_desc,font = f"Times {20 // len(curr_list) + 6}", wraplength=attackDict[i][index].winfo_width()-4, justify=LEFT).pack(side=LEFT, pady=1))
                move_butts[i][index].bind("<Leave>", lambda e, index=index, i=i:[widget for widget in self.all_children(attackDict[i][index]) if widget.winfo_class() == "Label"][0].destroy())

            if i == 0:
                attackDict[i].append(tkinter.Frame(player_frames[i], bg="#126b94" if self.attack != 'PASS' else "gold", bd=2, relief=SOLID, height = height // 8))
                attackDict[i][-1].pack(expand=True, fill=X)
                attackDict[i][-1].pack_propagate(0)

                pass_turn = tkinter.Button(attackDict[i][-1], text="Skip Turn", height=2, command= lambda i=i: move(i,len(attackDict[i]) - 1, "PASS"))
                pass_turn.pack(anchor=W)

                swap_holder = tkinter.Frame(attackDict[i][-1], bg="#126b94")
                swap_holder.pack(expand=True, fill=BOTH)

                swapper = tkinter.Button(swap_holder, text=" Swap ", height = 2, state = DISABLED if "Swap Blocked" in self.active_nanovor["Stats"] or len(self.swarm) == 1 else NORMAL, command= self.squad_screen)
                swapper.pack(side=LEFT)

                #Grabbing the nano_stats value in the self.swarm dict (self.next is the index of that nanovor), then splitting at the parentheses (Nanovor's class), and grabbing the name itself
                #lstrip to get rid of the leading newline before we split, that way it goes to the right of the Queued string.
                chosen = tkinter.Label(swap_holder, height = 2, text= "Queued: {}".format('' if self.next is None else (self.swarm[self.next].lstrip('\n').split('(')[0] if self.active != self.next else 'No Swap')))
                chosen.pack(side=LEFT,padx=15)

                def change_toggle(): self.toggle_swap = True if self.toggle_var.get() else False
                toggle_swap = Checkbutton(swap_holder, text = "Default No-Swap",variable=self.toggle_var, height=2, width=15,command=change_toggle)
                toggle_swap.pack(side=RIGHT)

            else:
                attackDict[i].append(tkinter.Frame(player_frames[i], bg = "#7f0002", bd=2, relief=SOLID, height= height // 8))
                attackDict[i][-1].pack(expand=True,fill=X)
                attackDict[i][-1].pack_propagate(0)

            stats_frames.append(tkinter.Frame(player_frames[i], bd=2, relief=SOLID, bg="dark goldenrod"))
            stats_frames[i].pack(expand=True, fill=X)

            #Do not allow the client's background to turn pink (they cant select themselves, this only happens when the client
            #chooses skip turn, opens the squad screen, then returns). However, in the future, maybe make this possible when
            #setting self overrides to make it more intuitive to the user about what is going on.
            stats.append(tkinter.Label(stats_frames[i], bg = "pink" if self.target == i and i != 0 else ("sky blue" if self.attack in pure_overrides and i == 0 else None), text=curr_nanos[i]))
            stats[i].pack(fill=X, padx=3,pady=3)

            if i != 0:
                stats[i].bind("<Button-1>", lambda e, i=i: target(i))

        confirm = tkinter.Button(self.window, text="Confirm", height=2, command = checker)
        confirm.place(rely = .95, relx=.5)

        report_screen = tkinter.Button(self.window, text="Back", height=2,state=NORMAL if self.round_summary else DISABLED, command=lambda: self.display_summary(self.battle_screen))
        report_screen.place(rely=0, relx=.03)

    def send_selections(self):
        #Information that is going to be sent every round from client to server
        self.connection.send_message({"Active":self.active, "Next":self.next, "Attack":self.attack, "Target":self.target})

        self.round_summary = self.connection.send_message("Get Round Summary")

        while self.round_summary == "Waiting":
            time.sleep(1)
            self.round_summary = self.connection.send_message("Get Round Summary")

        #GameLoop is called to receive info for the next round, then the corresponding method call is saved
        #This allows for players to read through the Carnage Report Screen at their own pace, AND also, now they will be able to go BACK
        #to the Carnage Report and read the events that happened! In case they want to check for whatever reason.
        method_to_call = self.gameLoop()
        self.display_summary(screen=method_to_call)

    def display_summary(self,screen):
        self.refresh_window(self.window)

        report = Text(self.window,width=150,wrap=WORD)
        report.pack(pady=20)

        report.insert(END, self.round_summary["Round Summary"])
        report.config(bd=2, state=DISABLED, relief=SOLID, bg="SteelBlue3", font="Sans 12 bold", highlightbackground="dark goldenrod")
        report.tag_configure("center", justify='center')
        report.tag_add("center", 1.0, "end")

        continue_on = Button(self.window, text="Continue", command =screen)
        continue_on.pack(pady=10, ipady=5, ipadx=5)

        quad_list,label_list = [],[]

        height = self.window.winfo_height()
        width = self.window.winfo_width()

        summary_frame = tkinter.Frame(self.window, bg="black")
        summary_frame.pack()

        for index, (plyrname,nanostats) in enumerate(self.round_summary["Players"]):
            quad_list.append(
                tkinter.LabelFrame(summary_frame, text=plyrname,bg="dark goldenrod",font="Sans 14 bold", height=height // 2,
                           width=width // len(self.round_summary["Players"])))
            quad_list[index].pack(side=LEFT, padx=10)

            label_list.append(Label(quad_list[index], text=nanostats, width=30))
            label_list[index].pack(side=TOP, padx=10)

    def display_gameOver(self, finale):
        self.timer.destroy()
        self.refresh_window(self.window)

        if type(finale) == dict:
            message = "{}, {}".format(self.username, finale["Results"])
            del finale["Results"]
        else:
            message = finale

        return_home = tkinter.Button(self.window, text="<== Main Menu", height=2, command=lambda:[return_home.destroy(), self.__init__(self.window)])
        return_home.place(relx=0,rely=0)

        over_frame = tkinter.Frame(self.window, bg=f"{'green' if 'Won' in message else ('red' if 'Lost' in message else 'white')}")
        over_frame.pack(pady=20)

        over = tkinter.Label(over_frame, text=message, font="Sans 16", borderwidth=2, relief=SOLID, bg=f"{'pale green' if 'Won' in message else ('pink' if 'Lost' in message else 'gray69')}")
        over.pack(padx=2,pady=2)

        winning_swarm = tkinter.LabelFrame(self.window, text=f"{'Winning' if 'Won' in message else 'Your'} Swarm", bg="dark goldenrod", font="Sans 14 bold")
        winning_swarm.pack(pady=20)

        swarm = Label(winning_swarm, text="\n".join(self.starting_swarm))
        swarm.pack()

        if type(finale) == dict:

            survivor_frame = tkinter.Frame(self.window, bg="silver")
            survivor_frame.pack(pady=20)

            survivors = tkinter.Label(survivor_frame, text="Nanovor Left Standing", font="Sans 16")
            survivors.pack(padx=2, pady=2)

            quad_list,label_list = [],[]
            height = self.window.winfo_height()
            width = self.window.winfo_width()

            holder = tkinter.Frame(self.window, bg="black")
            holder.pack()

            for index,nanostats in finale.items():
                quad_list.append(tkinter.LabelFrame(holder, bg="dark goldenrod", height=height // 2, width=width // len(finale)))
                quad_list[index].pack(side=LEFT, padx=40 / len(finale))

                label_list.append(Label(quad_list[index], text=nanostats))
                label_list[index].pack(side=TOP, padx=10)


INSTRUCTIONS = """TERMINOLOGY

HP: Health Points
ARM: Armor
SPD: Speed
STR: Strength
SV: Swarm Value
EN: Energy 

-Health Points reflect how much damage a Nanovor can effectively take before being “splatted” (ie, eliminated). A Nanovor is considered to be eliminated once their HP hits 0 or lower, and may not be revived or used for the remainder of the game. Any swarm effects , such as overrides, remain in play.

-Armor is applied every single time a Nanovor takes damage, except in the case where the attacking Nanovor uses an attack that is armor-piercing (ignores armor). The armor amount is subtracted from the damage that the defending Nanovor would otherwise take. For example, if the defending Nanovor has 10 ARM, and takes a 60 damage attack from an enemy, the total damage that the defending Nanovor will actually receive is 50. 

-Speed, simply put, is how fast a Nanovor is. The SPD of every active Nanovor is taken into account every turn when deciding which Nanovor gets to attack first, second, etc. However, order of attack is not exclusively dependent on absolute SPD. Instead, there is a “Speed Raffle”, where the chances of any particular Nanovor attacking first are that Nanovor’s SPD divided by the sum of the SPD’s of all Nanovor out on the field, multiplied by 100. For example, if two Nanovor are out on the field, with one having 70 SPD, and the other 30 SPD, the 70 SPD Nanovor has a 70% chance of attacking first, while the latter has a 30% chance. Obviously, you are not guaranteed to always go first if you have a high-SPD team as a result, but you still have better odds. 

-Strength can be thought of as a multiplier to the base damage of an attack of a Nanovor. For any attack that does damage, that attack has a base damage amount, which is then multiplied by the Nanovor’s STR divided by 100. For instance, if an attack has a base damage of 35, and a Nanovor that is going to use that attack has STR of 120, then you get 35 * 1.2, giving you 42 total damage (before taking into account enemy ARM). One Nanovor having higher STR than another does not necessarily mean that it will deal more damage, it is more dependent on the base damage of the attacks. However, a higher STR will of course result in more overall damage output for a Nanovor’s attacks. 

-Swarm Value reflects how much space a Nanovor will take up on your swarm (ie team). A standard match will allow you to have 1000 SV worth of Nanovor on your swarm. Generally speaking, stronger Nanovor will have a higher SV. Nanovor who have useful abilities or versatile movesets will tend to have higher SV’s. 

-Energy is the “currency” for using attacks. Every attack will cost a certain amount of EN, and if you try to use an attack that costs more EN than you currently have, you will “fizzle” out , meaning your attack will fail. If you fizzle out, you will retain the EN that you would have otherwise used. For example , if you try to use a 4 EN move while only having 3 EN, you will still have 3 EN. Additionally, every turn, each player in the game receives an additional 2 EN, so in that example you would have 5 EN by the next turn. 

GAMEPLAY

Overrides
-Overrides are special buffs that can be applied to your swarm as a whole, more specifically, they are applied to the current Nanovor you have out on the field. If you set an override with one Nanovor, and then switch out that Nanovor for another, the override will remain in play and any effects will be applied to the incoming Nanovor. You cannot stack overrides, meaning if you have an override in play and use a move that sets up another override, the current override will be overridden, funny enough. If your current override is removed or overridden, any effects from that override are removed from every Nanovor in your swarm. There are moves that can erase overrides. 

Spike Combos
-Spikes are a type of override that are used to set up stronger-than- normal combo plays. Currently in the game there exist Yellow, Red, and Blue Spikes, for each class of Nanovor (Velocitrons, Magnamods, and Hexites, respectively). These Spike overrides do nothing more than set up a finishing move that has bonus effects if a particular Spike override is in play. UNLESS OTHERWISE STATED IN THE ATTACK DESCRIPTION, USING A SPIKE OVERRIDE TO COMPLETE A COMBO PLAY WILL IN TURN CONSUME THE SPIKE OVERRIDE. This means you will have to set up another Spike override in order to perform another Spike combo play. 

Hacks
-Hacks are special effects that come with performing certain attacks. They can have a variety of effects, including stat buffs, stat debuffs, swap-blocks, stuns, override removal, or even EN removal. Attack descriptions will note if the attack causes any additional effects.

Swapping
-Every turn, each player has the option of queueing a Nanovor in their swarm to be swapped into the active slot on the next turn. Each player can choose to stay with their currently active Nanovor for the next turn. However, if a player is swap-blocked, or has only 1 Nanovor remaining, then they do not have the option of queueing up a Nanovor to swap in. If your active Nanovor gets splatted, then your queued Nanovor is disregarded and you are given the option to directly choose which Nanovor to play in the active spot on the following turn. 

Stun
-If a Nanovor becomes stunned, then any attack that Nanovor tries to use will fail. That Nanovor can only pass, and the stun will remain in effect until the specified amount of turns has passed by. If you switch out a stunned Nanovor, their turn stun length remains intact, i.e., the only way for a Nanovor to become un-stunned is to have them as your active Nanovor for that amount of turns, or use an attack that removes all status effects.

INTERFACE

To join a game, or create a game and wait for opponents to join, simply choose a username to don for the match, and select the type of battle you want. The screen will freeze and you will be waiting to find a match, and upon doing so, you will be taken to the swarm-building screen, where you can construct your team for the match.

Use the “Add to Swarm” buttons and drop-down menus to build your team, and “Finalize Swarm” when you are done. You will see your current swarm under the “Current Swarm” label in boxes and can remove Nanovor by clicking the red “X” buttons. You also have the option of creating a randomly-generated swarm by clicking the “Randomize” button. 

Once the match has begun, you will have 3 minutes each turn to make your selections and press the final “Confirm” button to submit your selections for the round. At the start, you will be prompted with a screen to select your starting Nanovor. Click on the yellow-bordered boxes at the top to select which Nanovor you would like to set as your active, and then press “Confirm” to lock it in. From there, press on an attack button and the background will turn gold, indicating that the attack is selected, choose an opponent if the attack is not an override (your current Nanovor’s background will turn light blue if that is the case), and upon clicking on an opponent’s active Nanovor stat box, that box will turn pink, indicating that it has been selected. You can select the “Skip Turn” button if you would rather pass and conserve your EN.
Click on the “Swap” button to be taken to the swap screen where you can queue up a Nanovor to be swapped in on the following turn. Your current Nanovor will be noted by “Currently Active” on that screen. Should you forget to do any required decisions, the game will notify you and not allow you to press the final “Confirm” until you have made all required selections. To see the description for each attack, simply hover over its button (you can do this for enemy Nanovor as well). The blue-green boxes below player overrides and energy provide quick HP summaries for Nanovor in each player’s swarm, and also note how many Nanovor each player has remaining. You can view the names and HP of each Nanovor in each player’s swarm by simply hovering over the boxes. Enemy Nanovor that have not been revealed will have “?” marks. 

After each round, you will be taken to a “Carnage Report” screen, which details all of the events and decisions from the turn you just completed. It will note which Nanovor attacked which other one, which Nanovor took damage, any Nanovor that were splatted, any swap-blocks or stun effects, how much damage each attack dealt, and finally any substitutions that were made. Press “Continue” from this screen to then be sent to either the swarm screen or the main battle screen. You can go back to review the previous round’s Carnage Report by clicking the “Back” button on the top-left of the main battle screen. The game ends when all but one player’s Nanovor are eliminated, or if every Nanovor on every team has been eliminated (resulting in a draw).
In any case and for any result, you will be sent to a final Carnage Report screen, whereby after clicking continue, you will be shown a concluding screen and given the option to return to the main menu to potentially join another match.

CREDIT

This project and all of the code behind it was developed thoroughly solely by Felneus (I also wrote this quick guide on how to play).
It was done out of passion to be able to experience a small bit of what Nanovor once was, and I say small bit, because a big part of Nanovor’s lure was the animations and gore that came along with it (which are obviously not seen in this battle simulator).
I hope that through this app, members of the community can enjoy simulating battles and see how they would play out in the actual game. In addition , I hope this sparks bits of creativity for new Nanovor that we could bring to life in the future, and have the simulator be a testing ground for those innovative ideas. Lastly, I want to give a thank you to Berberborscing for keeping the Nanovor Wikia up-to-date (that is where I obtained all the stats and information I needed to code the Nanovor into the program), and answering random and oddly specific questions I had about the game mechanics (questions I wanted answered to be able to mirror the original game’s combat system).
I also want to thank ShuShaeShen, a close friend of mine for helping me play-test the program and being my guinea pig for testing out different swarms and strategies. He was also generous about giving feedback on the overall look and feel of the interface. Happy Splatting!"""

window = Tk()
window.title("\'Vor: Siliconian Showdown")
window.geometry('1300x750')
window.configure(background='black')


ClientGUI(window)


window.mainloop()



