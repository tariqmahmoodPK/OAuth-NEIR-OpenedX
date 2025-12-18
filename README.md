# NEIR OAuth Plugin for Open edX

**NEIR OAuth Plugin** provides **Single Sign-On (SSO)** integration between the **NEIR Authentication System** and **Open edX LMS** using **OAuth 2.0 Authorization Code Flow** with **OpenID Connect (OIDC)**.

This plugin allows Open edX users to authenticate via NEIR in the same way as Google or Facebook login—without exposing user credentials to the LMS.

---

## ✨ Features

- OAuth 2.0 Authorization Code Flow
- OpenID Connect (OIDC) compliant
- Secure browser-based authentication
- Automatic user provisioning in Open edX
- Tutor plugin compatible
- No Open edX core code changes required
- Works like built-in social authentication providers

---

## 🧩 Architecture Overview

| Component | Role |
|---------|------|
| NEIR | OAuth 2.0 Authorization Server & OpenID Provider |
| Open edX LMS | OAuth 2.0 Client (Relying Party) |
| User Browser | Authentication Agent |

---

## 🔐 Supported Authentication Flow

### ✅ Supported
- OAuth 2.0 Authorization Code Grant
- OpenID Connect UserInfo endpoint

### ❌ Not Supported
- Resource Owner Password Grant (`grant_type=password`)
- API-only authentication
- Direct credential exchange with Open edX

> ⚠️ Password-based OAuth is deprecated and **not supported** by Open edX SSO.


---



## 🔄 OAuth Flow

1. User clicks **Login with NEIR** on Open edX
2. Browser redirects to NEIR `/oauth/authorize`
3. User authenticates on NEIR
4. NEIR redirects back with an authorization code
5. Open edX exchanges the code for an access token
6. Open edX retrieves user details via `/oauth/userinfo`
7. User is logged into Open edX


---



## 🌐 Required NEIR Endpoints

### 1️⃣ Authorization Endpoint
GET /oauth/authorize

**Required Parameters**
- `response_type=code`
- `client_id`
- `redirect_uri`
- `scope=openid email profile`
- `state`


---



### 2️⃣ Token Endpoint

**Body (x-www-form-urlencoded)**
grant_type=authorization_code
code=AUTH_CODE
client_id=CLIENT_ID
client_secret=CLIENT_SECRET
redirect_uri=REDIRECT_URI

---



### 3️⃣ UserInfo Endpoint (Mandatory)

**Required JSON Fields**
```json
{
  "sub": "unique_user_id",
  "email": "user@example.com",
  "email_verified": true,
  "name": "User Name"
}


---

##Installation (Tutor)
tutor plugins install git+https://github.com/<your-org>/neir-oauth.git
tutor plugins enable neir-oauth
tutor images build openedx
tutor local launch


Open edX Configuration
AUTHENTICATION_BACKENDS += (
    "neir_auth.backend.NEIROAuth2",
)

SOCIAL_AUTH_NEIR_KEY = "LMSEDX"
SOCIAL_AUTH_NEIR_SECRET = "NEIR_SECRET"

SOCIAL_AUTH_NEIR_AUTHORIZATION_URL = "https://URL/oauth/authorize"
SOCIAL_AUTH_NEIR_ACCESS_TOKEN_URL = "https://URL/oauth/token"
SOCIAL_AUTH_NEIR_USERINFO_URL = "https://URL/oauth/userinfo"

SOCIAL_AUTH_NEIR_SCOPE = ["openid", "email", "profile"]


###🔒 Security Requirements

HTTPS only
Short-lived access tokens
Exact redirect URI matching
CSRF protection via state
Secure storage of client secrets
No password transmission to Open edX


❗ Troubleshooting
Issue	Possible Cause
Wrong state parameter	Session or proxy misconfiguration
Redirect loop	Redirect URI mismatch
Login denied	Missing user claims
Token works but login fails	Invalid UserInfo response


View LMS logs:

tutor local logs lms



✅ Compatibility

Open edX (Tutor ≥ 20, Teak and above)

OAuth 2.0 (RFC 6749)

OpenID Connect Core



📄 License

MIT License

👥 Maintainers

OPM LMS Team



