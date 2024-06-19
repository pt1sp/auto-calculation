from obswebsocket import obsws

class OBSConnection:
    def __init__(self, host="localhost", port=4455, password="UUx1XfyErHAXyEFu"):
        self.ws = obsws(host, port, password)
        self.ws.connect()

    def is_connected(self):
        return self.ws.ws.connected
    
    def disconnect(self):
        self.ws.disconnect()