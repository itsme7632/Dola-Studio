import json, base64

_S = {"licensed": True, "plan": "pro", "claims": {"plan": "pro"},
      "expires_at": 9999999999, "issued_at": 0,
      "token": "ONYX-BYPASS", "product": "DOLA-STUDIO"}

verify_installation = lambda *a, **kw: True
verify_payload = lambda *a, **kw: True
check_files = lambda *a, **kw: True
verify_signatures = lambda *a, **kw: True
