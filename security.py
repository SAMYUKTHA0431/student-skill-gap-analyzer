"""Security layer built from the cryptography lab experiments:
 - Diffie-Hellman key exchange (Exp 8)  -> shared session key
 - SHA-256 hashing (Exp 9)              -> salted password storage, key derivation, HMAC
 - Symmetric stream cipher (Exp 5-7 idea) -> SHA-256 counter-mode keystream XOR
NOTE: educational implementation. Real systems should use TLS / AES-GCM."""
import hashlib, hmac, json, os, secrets, struct

P = 2 ** 127 - 1      # Mersenne prime (demo size; use 2048-bit groups in production)
G = 3


# ---------- Diffie-Hellman ----------
def dh_keypair():
    priv = secrets.randbelow(P - 3) + 2
    return priv, pow(G, priv, P)


def dh_session_key(priv, other_pub):
    shared = pow(other_pub, priv, P)
    return hashlib.sha256(str(shared).encode()).digest()      # 32-byte key


# ---------- Password hashing ----------
def hash_password(password, salt=None):
    salt = salt or os.urandom(16).hex()
    return salt, hashlib.sha256((salt + password).encode()).hexdigest()


def verify_password(password, salt, stored):
    return hmac.compare_digest(hash_password(password, salt)[1], stored)


# ---------- Stream cipher + HMAC ----------
def _keystream(key, nonce, n):
    out, counter = b"", 0
    while len(out) < n:
        out += hashlib.sha256(key + nonce + struct.pack(">Q", counter)).digest()
        counter += 1
    return out[:n]


def encrypt(key, data: bytes) -> bytes:
    nonce = os.urandom(8)
    ct = bytes(a ^ b for a, b in zip(data, _keystream(key, nonce, len(data))))
    tag = hmac.new(key, nonce + ct, hashlib.sha256).digest()
    return nonce + ct + tag


def decrypt(key, blob: bytes) -> bytes:
    nonce, ct, tag = blob[:8], blob[8:-32], blob[-32:]
    if not hmac.compare_digest(tag, hmac.new(key, nonce + ct, hashlib.sha256).digest()):
        raise ValueError("Integrity check failed (message tampered)")
    return bytes(a ^ b for a, b in zip(ct, _keystream(key, nonce, len(ct))))


# ---------- Framed socket I/O ----------
def _recv_exact(sock, n):
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Connection closed")
        buf += chunk
    return buf


def send_raw(sock, data: bytes):
    sock.sendall(struct.pack(">I", len(data)) + data)


def recv_raw(sock) -> bytes:
    (n,) = struct.unpack(">I", _recv_exact(sock, 4))
    return _recv_exact(sock, n)


def send_msg(sock, key, obj):
    blob = encrypt(key, json.dumps(obj).encode())
    send_raw(sock, blob)
    return blob


def recv_msg(sock, key):
    return json.loads(decrypt(key, recv_raw(sock)).decode())
