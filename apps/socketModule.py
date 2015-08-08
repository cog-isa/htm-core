__author__ = 'gmdidro'
import pickle
import socket

class socketModule:

    def openLocalPort(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', port)
        self.sock.bind(server_address)
        self.sock.listen(1)

    def waitForRqst(self, handle):
        connection, client_address = self.sock.accept()
        data = bytes()
        data += connection.recv(512)
        answer=handle(data)

        end_message = "[THIS_IS_THE_END_HOLD_YOUR_BREATH_AND_COUNT_TO_TEN]"
        connection.sendall(answer)
        connection.sendall(bytes(end_message, 'UTF-8'))
        connection.close()

    def sendRqst(self,hostname, port, cmd):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((hostname, port))

        self.sock.sendall(cmd)
        end_message = "[THIS_IS_THE_END_HOLD_YOUR_BREATH_AND_COUNT_TO_TEN]"

        data = bytes()

        while True:
            q = self.sock.recv(1024)
            try:
                if q.decode('utf-8').find(end_message) == -1:
                    break
            except UnicodeDecodeError:
                pass
            data += q

        self.sock.close()
        obj = pickle.loads(data)
        return obj