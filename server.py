import socket, json, time, threading;

class GameServer:

    def __init__(self, port_no):
        self.port_no = port_no;
        self.user_list = {};
    


    def start_server(self):

        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        self.sock = socket.socket(type=socket.SOCK_DGRAM);
        self.sock.bind((ip_address, self.port_no));
        print(f"Listening on port {self.sock.getsockname()[1]}, on address {ip_address}")


        # Begin timer thread now

        while(True):
            msg, addr = self.sock.recvfrom(64000);
            size = int(msg.decode()[0:16]);
            payload = json.loads(msg.decode()[16:(16+size)]);

            # Probably check for proper formatting here or something


            if(payload["method"] == "connect"):
                print(payload["args"]["username"]);
                response = None;
                #if(payload["args"]["username"] not in self.user_listAAAAA):
                if(True):
                    # Do some authentication or something here! 
                    self.user_list[payload["args"]["username"]] = {"status": "loading", "address": addr, "last_heard_from": time.time(), "position": {"x": 0, "y": 0}};

                    #response = {"method": "accept_connection", "args": None};
                    response = {"x": 0, "y": 0};
                else:
                    response = {"method": "reject_connection", "args": None};

                self.sock.sendto(f"{len(json.dumps(response)):>16}{json.dumps(response)}".encode(), addr);

            elif(payload["method"] == "initialized"):
                pass;

            elif(payload["method"] == "disconnect"):
                pass;

            elif(payload["method"] == "send_player_update"):
                print(payload["args"]);
                self.update_player_position(payload["args"]);

                response = self.user_list[payload["args"]["username"]]["position"];

                self.sock.sendto(json.dumps(response).encode(), addr);

            else:
                print("error", payload);


            print(self.user_list);
            




    def update_player_position(self, args):
        try:
            username = args["username"];
            input_val = args["input"];
            if(input_val == "up"):
                self.user_list[username]["position"]["y"] += 5;
            elif(input_val == "down"):
                self.user_list[username]["position"]["y"] -= 5;
            elif(input_val == "left"):
                self.user_list[username]["position"]["x"] -= 5;
            elif(input_val == "right"):
                self.user_list[username]["position"]["x"] += 5;
            print(self.user_list[username]["position"]);
        except:
            pass;










if __name__ == "__main__":
    server = GameServer(6969);
    server.start_server(); 