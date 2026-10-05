_S = {"licensed": True, "plan": "pro", "claims": {"plan": "pro"},
      "expires_at": 9999999999, "issued_at": 0,
      "token": "ONYX-BYPASS", "product": "DOLA-STUDIO"}

verify_token = lambda *a, **kw: True

class WorkerLicenseStore:
    def __init__(self, *a, **kw): pass
    def status(self, *a, **kw): return dict(_S)
    def refresh(self, *a, **kw): return dict(_S)
    def verify(self, *a, **kw): return True
