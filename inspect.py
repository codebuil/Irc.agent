
import socket
import threading

class IRCBot:
    def __init__(self, server, port):
        self.server = server
        self.port = port
        self.nick = "BOTinspect"
        self.password = "inspect"
        self.channel = "#home"
        self.in_bot_mode = False

        # Lista de palavras proibidas
        self.palavras_proibidas = ["xpto", "XPTO"]

        self._index = 0
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server, self.port))
        self.send_message(f"USER {self.nick} 0 * :{self.nick}\r\n")
        self.send_message(f"NICK {self.nick}\r\n")
        self.send_message(f"JOIN {self.channel}\r\n")

    def send_message(self, message):
        self.sock.send(message.encode("utf-8"))

   
    def receive_messages(self):
        while True:
            data = self.sock.recv(4096).decode("utf-8")
            if not data:
                break
            

            for palavra_proibida in self.palavras_proibidas:
                if palavra_proibida in data:
                    self.send_message(f"PRIVMSG {self.channel} :Palavra proibida!\r\n")

    def start(self):
        try:
            #self.nick = input("Enter your nickname: ")
            #self.password = input("Enter your password: ")
            self.connect()

            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()

            while True:
                if not self.in_bot_mode:
                    message = input()
                    if not message:
                        break
                    self.send_message(f"PRIVMSG {self.channel} :{message}\r\n")

        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            self.sock.close()


print("\x1bc\x1b[43;30mstart application:")

if __name__ == "__main__":
    server_ip = "192.168.1.4"
    server_port = 6667

    irc_bot = IRCBot(server_ip, server_port)
    irc_bot.start()