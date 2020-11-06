import socket
import pickle
import threading
from NanovorCollection import*
from OnlineGame import OnlineGame
import sys, os


HOST = ""
PORT = 50500
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((HOST, PORT))

s.listen(5)

#Contains lists of ongoing games
gameID = 0
games = {}
#Contains each clients socket as a key, and the ID of the game they're in as a value
clients = {}

server_magnamod_list = MAGNAMOD_LIST
server_velocitron_list = VELOCITRON_LIST
server_hexite_list = HEXITE_LIST
server_custom_list = CUSTOM_LIST
server_complete_list = COMPLETE_LIST

#Whether or not to include custom nanovor in the games.
FANOVOR = True

def handle_client(conn, addr):
    try:
        global gameID
        global FANOVOR
        connected = True
        magnamod_list = server_magnamod_list[:]
        velocitron_list = server_velocitron_list[:]
        hexite_list = server_hexite_list[:]
        custom_list = server_custom_list[:]
        complete_list = server_complete_list[:]
        while connected:
            data = pickle.loads(conn.recv(4096*8))

            if data:
                if type(data) == dict and "SetFanovorSettings" in data:
                    FANOVOR = data["SetFanovorSettings"]
                    conn.send(pickle.dumps("Job completed"))

                elif type(data) == tuple:
                    if data[0].isdigit():
                        # data[0] has the number of players the user chose to play, data[1] is the users username
                        # (Players should have already entered the game, maybe..)
                        inGame = False
                        #Iterate through a copy so that if you add a new game, you don't iterate through the dict while changing it
                        for ID,game in games.copy().items():
                            if game.game_size() == int(data[0]):
                                if not(game.full()):
                                    games[ID].add_player((conn,data[1]))
                                    clients[conn] = ID
                                else:
                                    games[gameID] = OnlineGame(int(data[0]), complete_list)
                                    games[gameID].add_player((conn,data[1]))
                                    clients[conn] = gameID
                                    gameID += 1
                                inGame = True

                        if not inGame:
                            games[gameID] = OnlineGame(int(data[0]), complete_list)
                            games[gameID].add_player((conn,data[1]))
                            clients[conn] = gameID
                            gameID += 1

                        if games[clients[conn]].full():
                            conn.send(pickle.dumps("Match is starting!"))

                        else:
                            conn.send(pickle.dumps("Waiting on more players"))

                elif data == "Check Status":
                    if games[clients[conn]].full():
                        conn.send(pickle.dumps("Match is starting!"))
                    else:
                        conn.send(pickle.dumps("Waiting on more players"))

                elif data == "GetMags":
                    conn.sendall(pickle.dumps([(mag.get_name(), mag.get_sv()) for mag in magnamod_list]))
                elif data == "GetVels":
                    conn.sendall(pickle.dumps([(vel.get_name(), vel.get_sv()) for vel in velocitron_list]))
                elif data == "GetHexs":
                    conn.sendall(pickle.dumps([(hex.get_name(), hex.get_sv()) for hex in hexite_list]))
                elif data == "GetCust":
                    conn.sendall(pickle.dumps([(cust.get_name(), cust.get_sv()) for cust in custom_list] if FANOVOR else []))

                elif type(data) == list:
                    if data[0] == "SwarmSelected":
                        games[clients[conn]].set_swarm(conn,data[1])
                        conn.send(pickle.dumps("Swarm Confirmed"))
                    #data[1] gives the swarm of the player (each Nanovor is a string)

                elif data == "Match Status":
                    conn.send(pickle.dumps(games[clients[conn]].ready()))

                elif data == "Game Ongoing":
                    over = games[clients[conn]].gameOver(conn)
                    conn.send(pickle.dumps(over))
                    if over == "You were eliminated!":
                        break
                    #This will be True if over is anything except False, None, 0, or empty. If string or dict gets returned, it goes off as True
                    elif over:
                        break
                elif data == "Get Active Nanovor":
                    info = games[clients[conn]].gameInformation(conn)["Active Nanovor"]
                    conn.send(pickle.dumps(info))
                elif data == "Get Player Swarm":
                    info = games[clients[conn]].gameInformation(conn)["Player Swarm"]
                    conn.send(pickle.dumps(info))
                elif data == "Get Player Attacks":
                    info = games[clients[conn]].gameInformation(conn)["Player Attacks"]
                    conn.send(pickle.dumps(info))
                elif data == "Get Opponent Active":
                    info = games[clients[conn]].gameInformation(conn)["Opponent Active"]
                    conn.send(pickle.dumps(info))
                elif data == "Energy & Overrides":
                    info = games[clients[conn]].gameInformation(conn)["Energy & Overrides"]
                    conn.send(pickle.dumps(info))
                elif data == "Get All Swarms":
                    info = games[clients[conn]].gameInformation(conn)["All Swarms"]
                    conn.send(pickle.dumps(info))
                elif data == "Get Opponent Attacks":
                    info = games[clients[conn]].gameInformation(conn)["Opponent Attacks"]
                    conn.send(pickle.dumps(info))
                elif data == "Get Round Summary":
                    #Will be a function in game that returns the dict with the carnage report and updated stats for all nanovor in the game
                    #If waiting on other players, round summary will be "Waiting"
                    info = games[clients[conn]].get_round_summary()
                    conn.send(pickle.dumps(info))
                #If the data is a dict, it has to be the information received from the client about their decisions
                elif type(data) == dict:
                    #send it to a function that splits up all the information for each player, makes sure every player sent in their information, and
                    #then applies those decisions to the engine, which runs all the behind-the scenes work
                    games[clients[conn]].control_center(conn,data)
                    conn.send(pickle.dumps("Received"))

        #Close the client connection
        conn.close()

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

    finally:
        # Delete the game from the dict of games, if the client is in it and if the game hasn't been deleted
        # Iterate through a copy so it doesn't raise an error when dictionary
        for id, game in games.copy().items():
            if conn in game.get_players().keys() and not game.gameOver(conn):
                game.handle_quitters(conn)
            #If the client disconnected but it isn't due to them quitting, that means the game is over, so remove them from the game.
            else:
                game.remove_player(conn)
            if len(game.get_players()) == 0:
                del games[id]
        if conn in clients:
            del clients[conn]

while True:
    conn, addr = s.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print('Connected by', addr)
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

