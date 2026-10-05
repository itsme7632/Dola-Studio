_S = {"licensed": True, "plan": "pro", "claims": {"plan": "pro"},
      "expires_at": 9999999999, "issued_at": 0,
      "token": "ONYX-BYPASS", "product": "DOLA-STUDIO"}

check_online_license = lambda *a, **kw: dict(_S)
refresh_online_license = lambda *a, **kw: dict(_S)
verify_online_license = lambda *a, **kw: True

class OnlineLicenseStore:
    def __init__(self, *a, **kw): pass
    def status(self, *a, **kw): return dict(_S)
    def activate(self, *a, **kw): return dict(_S)
    def refresh(self, *a, **kw): return dict(_S)
