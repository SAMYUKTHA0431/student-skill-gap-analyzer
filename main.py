"""Stand-alone mode (no network needed):  python main.py"""
from service import process, Session
import ui


class LocalAPI:
    def __init__(self): self.session = Session()
    def call(self, cmd, **kw): return process({"cmd": cmd, **kw}, self.session)


if __name__ == "__main__":
    ui.run(LocalAPI(), "Stand-alone mode")
