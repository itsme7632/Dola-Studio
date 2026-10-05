import json, base64

_S = {"licensed": True, "plan": "pro", "claims": {"plan": "pro"},
      "expires_at": 9999999999, "issued_at": 0,
      "token": "ONYX-BYPASS", "product": "DOLA-STUDIO"}

def verify_payload(payload=None, *a, **kw):
    return payload if payload else {}

def sign_payload(payload, *a, **kw):
    return {
        "payload": base64.urlsafe_b64encode(
            json.dumps(payload, sort_keys=True).encode()
        ).decode().rstrip("="),
        "signature": "ONYXBYPASS",
        "purpose": payload.get("purpose", "license") if isinstance(payload, dict) else "license",
    }
