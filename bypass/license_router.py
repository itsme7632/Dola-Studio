"""license_router.py â€” v3 with RoutedLicenseStore + is_online"""

LOG = r"C:\Users\SAAHA\AppData\Local\Programs\DolaStudio\bypass\calls.log"
def _log(msg):
    try:
        with open(LOG, "a") as f: f.write(msg + "\n")
    except: pass

_log("=== license_router.py LOADED (v3) ===")

_S = {"licensed": True, "plan": "pro", "active": True,
      "claims": {"plan": "pro", "licensed": True},
      "expires_at": 9999999999, "issued_at": 0,
      "token": "ONYX-BYPASS", "product": "DOLA-STUDIO",
      "is_online": True, "online": True}

check_license = lambda *a, **kw: True
get_license_status = lambda *a, **kw: dict(_S)
verify = lambda *a, **kw: True

class RoutedLicenseStore:
    def __init__(self, *a, **kw):
        _log("RoutedLicenseStore.__init__")
    def status(self, *a, **kw):
        _log("RoutedLicenseStore.status() -> dict")
        return dict(_S)
    def activate(self, *a, **kw):
        _log("RoutedLicenseStore.activate()")
        return dict(_S)
    def refresh(self, *a, **kw):
        _log("RoutedLicenseStore.refresh()")
        return dict(_S)
    def check(self, *a, **kw): return True
    def verify(self, *a, **kw): return True
    @property
    def is_online(self):
        _log("RoutedLicenseStore.is_online -> True")
        return True
    def __getattr__(self, n):
        _log(f"RoutedLicenseStore.{n}")
        if n == 'is_online': return True
        return lambda *a, **k: dict(_S)

# Also export as LicenseRouter for compatibility
LicenseRouter = RoutedLicenseStore
