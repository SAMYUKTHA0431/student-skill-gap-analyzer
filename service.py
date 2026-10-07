"""Business logic shared by the TCP server and the stand-alone mode."""
import json, os, threading, time
from analyser import analyse, rank_roles
from skills_db import ROLES
from security import hash_password, verify_password

BASE = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE, "data", "users.json")
HIST_FILE = os.path.join(BASE, "data", "history.json")
_lock = threading.Lock()


def _load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


class Session:
    user = None


def ok(**kw):  return {"ok": True, **kw}
def err(msg):  return {"ok": False, "error": msg}


def process(req, session):
    cmd = req.get("cmd")
    if cmd == "register":
        u, p = str(req.get("username", "")).strip(), str(req.get("password", ""))
        if not u.isalnum() or len(p) < 4:
            return err("Username must be alphanumeric and password >= 4 characters")
        with _lock:
            users = _load(USERS_FILE)
            if u in users:
                return err("Username already exists")
            salt, h = hash_password(p)
            users[u] = {"salt": salt, "hash": h}
            _save(USERS_FILE, users)
        return ok(message="Registered successfully")
    if cmd == "login":
        u, p = req.get("username", ""), req.get("password", "")
        rec = _load(USERS_FILE).get(u)
        if not rec or not verify_password(p, rec["salt"], rec["hash"]):
            return err("Invalid username or password")
        session.user = u
        return ok(message=f"Welcome, {u}!")
    if not session.user:
        return err("Please login first")
    if cmd == "roles":
        return ok(roles={r: {s: list(v) for s, v in sk.items()} for r, sk in ROLES.items()})
    if cmd == "analyse":
        try:
            res = analyse(req["role"], req.get("ratings", {}))
        except KeyError as e:
            return err(str(e))
        with _lock:
            hist = _load(HIST_FILE)
            hist.setdefault(session.user, []).append(
                {"time": time.strftime("%Y-%m-%d %H:%M"), "role": res["role"],
                 "readiness": res["readiness"], "level": res["level"]})
            _save(HIST_FILE, hist)
        return ok(result=res)
    if cmd == "rank":
        return ok(ranking=rank_roles(req.get("ratings", {})))
    if cmd == "history":
        return ok(history=_load(HIST_FILE).get(session.user, []))
    return err("Unknown command")
