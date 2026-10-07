"""Multi-client TCP server (run first):  python server.py"""
import socket, threading
from security import dh_keypair, dh_session_key, send_raw, recv_raw, send_msg, recv_msg
from service import process, Session

HOST, PORT = "127.0.0.1", 5050


def handle(conn, addr):
    print(f"[+] Connected: {addr}")
    try:
        priv, pub = dh_keypair()                       # Diffie-Hellman handshake
        send_raw(conn, str(pub).encode())
        key = dh_session_key(priv, int(recv_raw(conn).decode()))
        print(f"[{addr[1]}] Secure session key established (SHA-256 of DH secret)")
        session = Session()
        while True:
            req = recv_msg(conn, key)                  # decrypt + verify HMAC
            print(f"[{addr[1]}] request: {req.get('cmd')} (user={session.user})")
            send_msg(conn, key, process(req, session))
    except (ConnectionError, ValueError, OSError):
        pass
    finally:
        conn.close()
        print(f"[-] Disconnected: {addr}")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT)); s.listen(5)
        print(f"Skill Gap Analyser server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
