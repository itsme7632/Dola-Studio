"""license_client.py â€” v5 with LicenseError + is_online"""
import hashlib, platform

LOG = r"C:\Users\SAAHA\AppData\Local\Programs\DolaStudio\bypass\calls.log"
def _log(msg):
    try:
        with open(LOG, "a") as f: f.write(msg + "\n")
    except: pass

_log("=== license_client.py LOADED (v5) ===")

def _device_id():
    try:
        import winreg
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography",
                           0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        guid, _ = winreg.QueryValueEx(k, "MachineGuid")
        winreg.CloseKey(k)
        return hashlib.sha256(guid.encode()).hexdigest()
    except:
        return hashlib.sha256(platform.node().encode()).hexdigest()

def device_id():
    return _device_id()

normalize_device = lambda d: d.strip().lower()
verify_license = lambda *a, **kw: True

class LicenseError(Exception):
    pass

_S = {"licensed": True, "plan": "pro", "active": True,
      "claims": {"plan": "pro", "licensed": True},
      "expires_at": 9999999999, "issued_at": 0,
      "token": "ONYX-BYPASS", "product": "DOLA-STUDIO",
      "is_online": True, "online": True}

class LicenseStore:
    def __init__(self, *a, **kw):
        self._d = _device_id()
        _log("LicenseStore.__init__")
    def _save(self, *a, **kw): pass
    def activate(self, *a, **kw): return dict(_S, device=self._d)
    def status(self, *a, **kw):
        _log("LicenseStore.status() -> dict")
        return dict(_S, device=self._d)
    def verify(self, *a, **kw): return True
    def refresh(self, *a, **kw): return dict(_S, device=self._d)
    @property
    def is_online(self): return True
    def __getattr__(self, n):
        _log(f"LicenseStore.{n}")
        if n == 'is_online': return True
        return lambda *a, **k: dict(_S, device=self._d)
