import socket

# ( Make sure below ip address and port numbers are correct )
# ip = "192.168.1.118"
ip = input("Enter ip address: ")
port = 5002


class Client:
    def __init__(self):
        self.content = None
        self.ip = ip
        self.port = port

    def send_file(self, p_name):
        print("p_name : ", p_name)

        file = "testing_data/" + p_name
        print("file : ", file)

        with open(file, 'rb') as f:
            self.content = f.read()
        return self.content

    def connect(self):
        try:
            s = socket.socket()
            s.connect((ip, port))

            msg = s.recv(1024)
            msg = msg.decode("utf-8")
            print("[MESSAGE RECEIVED] ", msg)

            packet_name = input("Enter packet name : ")
            content = self.send_file(packet_name)
            s.send(content)

            msg = s.recv(2048)
            msg = msg.decode("utf-8")
            print("[MESSAGE RECEIVED] ", msg)

            filename = input("Type here >")
            s.send(filename.encode("utf-8"))
            print("")
            # print("[MESSAGE SENT] Message sent successfully")

            msg = s.recv(1024)
            msg = msg.decode("utf-8")
            print("[MESSAGE RECEIVED] ", msg)

            msg = input("Type here >")
            s.send(msg.encode("utf-8"))
            print("")
            # print("[MESSAGE SENT] Message sent successfully")

            msg = s.recv(1024)
            msg = msg.decode("utf-8")
            print("[MESSAGE RECEIVED] ", msg)

            s.close()

        except Exception as e:
            print("[ERROR] Opps something went wrong, check below error message")
            print("[ERROR MESSAGE] ", e)


if __name__ == '__main__':
    client = Client()
    client.connect()
