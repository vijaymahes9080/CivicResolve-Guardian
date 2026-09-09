# Security Controls & Compliance: CivicResolve Guardian

## 1. HTTP Security Headers
All API responses automatically inject standard enterprise security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `X-Request-ID: <UUID>`

## 2. Cryptographic Audit Log Signatures
Every lifecycle event produces an immutable audit record signed using HMAC-SHA256:
```python
message = f"{case_id}|{action_type}|{actor_id}|{timestamp}|{details_json}".encode("utf-8")
signature = hmac.new(SECRET_KEY.encode("utf-8"), message, hashlib.sha256).hexdigest()
```
If an adversary mutates the database record directly, the signature verification fails.

## 3. Password Hashing
Passwords are salted and hashed using PBKDF2-SHA256 with 29,000 iterations via PassLib, eliminating GPU-accelerated dictionary attacks.

## 4. Rate Limiting & DoS Protection
Endpoints are protected with token-bucket rate limits:
- Grievance submission: 10 per minute per citizen token.
- General queries: 100 per minute per IP.
