"""Network client (run after server):  python client.py"""
import socket
from security import dh_keypair, dh_session_key, send_raw, recv_raw, send_msg, recv_msg
from server import HOST, PORT
import ui


class NetAPI:
    def __init__(self):
        self.sock = socket.create_connection((HOST, PORT))
        priv, pub = dh_keypair()
        server_pub = int(recv_raw(self.sock).decode())
        send_raw(self.sock, str(pub).encode())
        self.key = dh_session_key(priv, server_pub)
        self.shown = False

    def call(self, cmd, **kw):
        blob = send_msg(self.sock, self.key, {"cmd": cmd, **kw})
        if not self.shown:
            print(f"  [secure channel] first message on the wire (encrypted): {blob[:24].hex()}...")
            self.shown = True
        return recv_msg(self.sock, self.key)


if __name__ == "__main__":
    try:
        ui.run(NetAPI(), "Client (TCP + Diffie-Hellman + SHA-256)")
    except ConnectionRefusedError:
        print("Server not running. Start it first with:  python server.py")
