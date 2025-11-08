# Authentication and API Flow Documentation

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Authentication Flow](#authentication-flow)
4. [API Request Flow](#api-request-flow)
5. [Backend Token Validation](#backend-token-validation)
6. [Complete Request Cycle](#complete-request-cycle)
7. [Configuration](#configuration)
8. [Troubleshooting](#troubleshooting)

---

## Overview

This document describes the complete authentication and API calling flow in the KCLoft application. The system uses **Microsoft Azure AD (MSAL)** for frontend authentication and **JWT token validation** on the FastAPI backend.

### Key Components

- **Frontend**: Vue 3 + MSAL Browser
- **Backend**: FastAPI + JWT validation
- **Authentication Provider**: Microsoft Azure AD
- **Token Format**: JWT (JSON Web Tokens)

---

## Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   Vue Frontend  │────────▶│  Azure AD/MSAL   │────────▶│  FastAPI Backend│
│  (localhost:5173)│         │  (Microsoft)     │         │ (localhost:8000) │
└─────────────────┘         └──────────────────┘         └─────────────────┘
       │                              │                            │
       │                              │                            │
       │  1. Login Request            │                            │
       │─────────────────────────────▶│                            │
       │                              │                            │
       │  2. Redirect to Azure        │                            │
       │◀─────────────────────────────│                            │
       │                              │                            │
       │  3. User Authenticates        │                            │
       │─────────────────────────────▶│                            │
       │                              │                            │
       │  4. Token + Redirect          │                            │
       │◀─────────────────────────────│                            │
       │                              │                            │
       │  5. API Request + Token       │                            │
       │──────────────────────────────────────────────────────────▶│
       │                              │                            │
       │  6. Validated Response        │                            │
       │◀──────────────────────────────────────────────────────────│
```

---

## Authentication Flow

### Step-by-Step Process

#### 1. Application Initialization (`main.ts`)

**File**: `kcloft-app/src/main.ts`

When the Vue application starts:

```typescript
async function bootstrap() {
  // Step 1: Initialize MSAL first
  await ensureMsalInitialized();
  
  // Step 2: Handle redirect login before mounting the app
  const redirectResult = await msalInstance.handleRedirectPromise();
  
  // Step 3: Set active account if login was successful
  if (redirectResult) {
    msalInstance.setActiveAccount(redirectResult.account);
  } else {
    // Check for existing accounts
    const accounts = msalInstance.getAllAccounts();
    if (accounts.length > 0 && accounts[0]) {
      msalInstance.setActiveAccount(accounts[0]);
    }
  }
  
  // Step 4: Mount the Vue app
  const app = createApp(App);
  app.use(router);
  app.mount("#app");
  
  // Step 5: Navigate to home if just logged in
  if (redirectResult) {
    router.push({ name: "home" });
  }
}
```

**What happens:**
- MSAL is initialized with configuration from `authConfig.ts`
- Checks if user is returning from Azure AD login redirect
- Sets active account if login was successful
- Mounts the Vue application
- Redirects to home page if login just completed

#### 2. MSAL Configuration (`authConfig.ts`)

**File**: `kcloft-app/src/auth/authConfig.ts`

```typescript
export const msalConfig = {
  auth: {
    clientId: "d4552121-7ccf-4875-8b0a-c71a7f5c8c28",
    authority: "https://login.microsoftonline.com/109199d4-f7c0-4027-bcd7-9937e7fb177b",
    redirectUri: "http://localhost:5173/"
  }
};

export const loginRequest = {
  scopes: ["User.Read"]
};

export const apiRequest = {
  scopes: ["User.Read"]
};
```

**Configuration Details:**
- **clientId**: Azure AD Application (Client) ID
- **authority**: Azure AD Tenant ID
- **redirectUri**: Where Azure AD redirects after authentication
- **scopes**: Permissions requested (User.Read = Microsoft Graph basic profile)

#### 3. User Login Process

**File**: `kcloft-app/src/views/LoginView.vue`

**Option A: Manual Login Button**

```typescript
function handleLogin() {
  msalInstance.loginRedirect(loginRequest);
}
```

**What happens:**
1. User clicks "Login with Microsoft" button
2. `msalInstance.loginRedirect()` is called
3. Browser redirects to Microsoft login page
4. User enters credentials
5. Microsoft redirects back to `redirectUri` with token
6. `handleRedirectPromise()` in `main.ts` processes the result

**Option B: Automatic Redirect (Router Guard)**

**File**: `kcloft-app/src/router/index.ts`

```typescript
router.beforeEach(async (to, _from, next) => {
  await ensureMsalInitialized();
  const accounts = msalInstance.getAllAccounts();
  
  if (to.meta.requiresAuth && accounts.length === 0) {
    if (to.name !== "login") {
      await msalInstance.loginRedirect();
      return; // Don't call next() - loginRedirect will navigate away
    }
  }
  next();
});
```

**What happens:**
1. User tries to access protected route (e.g., `/`)
2. Router guard checks if user is authenticated
3. If not authenticated, automatically triggers `loginRedirect()`
4. User is redirected to Microsoft login
5. After login, user is redirected back and can access the route

#### 4. Token Acquisition (`authService.ts`)

**File**: `kcloft-app/src/auth/authService.ts`

```typescript
export async function getAccessToken(): Promise<string | null> {
  await ensureMsalInitialized();
  
  // Get active account
  const account = msalInstance.getActiveAccount();
  if (!account) {
    const accounts = msalInstance.getAllAccounts();
    if (accounts.length > 0 && accounts[0]) {
      msalInstance.setActiveAccount(accounts[0]);
    } else {
      return null; // No account available
    }
  }
  
  const activeAccount = msalInstance.getActiveAccount();
  if (!activeAccount) {
    return null;
  }
  
  // Request token silently (from cache or refresh)
  const request: SilentRequest = {
    ...apiRequest,
    account: activeAccount,
  };
  
  try {
    const response = await msalInstance.acquireTokenSilent(request);
    return response.accessToken;
  } catch (error) {
    console.error("Silent token acquisition failed:", error);
    return null; // Token acquisition failed
  }
}
```

**What happens:**
1. Ensures MSAL is initialized
2. Gets the active user account
3. Attempts to acquire token silently (from cache or refresh token)
4. Returns access token if successful
5. Returns `null` if token cannot be acquired

**Token Caching:**
- MSAL automatically caches tokens in browser storage
- Tokens are refreshed automatically when expired
- Silent acquisition avoids user interaction

---

## API Request Flow

### Step-by-Step Process

#### 1. API Client Setup (`api.ts`)

**File**: `kcloft-app/src/services/api.ts`

```typescript
const apiClient: AxiosInstance = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});
```

#### 2. Request Interceptor (Automatic Token Injection)

```typescript
apiClient.interceptors.request.use(
  async (config: InternalAxiosRequestConfig) => {
    // Get access token
    const token = await getAccessToken();
    
    // Add token to Authorization header
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  }
);
```

**What happens:**
1. Every API request goes through this interceptor
2. `getAccessToken()` is called to get current token
3. Token is added to `Authorization: Bearer {token}` header
4. Request proceeds with authentication header

#### 3. Making API Calls

**File**: `kcloft-app/src/views/HomeView.vue`

```typescript
async function fetchQuestions() {
  loading.value = true;
  error.value = null;
  try {
    // API call - token is automatically added by interceptor
    const response = await apiClient.get("/questions/");
    questions.value = response.data;
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.message;
  } finally {
    loading.value = false;
  }
}
```

**What happens:**
1. Component calls `apiClient.get("/questions/")`
2. Request interceptor adds `Authorization: Bearer {token}` header
3. Request is sent to `http://localhost:8000/questions/`
4. Backend validates token and processes request
5. Response is returned to component

#### 4. Response Interceptor (Token Refresh on 401)

```typescript
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token might be expired, try to get a new one
      const retryCount = error.config?.__retryCount || 0;
      if (retryCount < 1) {
        const token = await getAccessToken();
        if (token && error.config) {
          error.config.__retryCount = retryCount + 1;
          error.config.headers.Authorization = `Bearer ${token}`;
          return apiClient.request(error.config); // Retry with new token
        }
      }
    }
    return Promise.reject(error);
  }
);
```

**What happens:**
1. If backend returns 401 (Unauthorized)
2. Interceptor attempts to get a fresh token
3. Retries the request with new token (max 1 retry)
4. If retry fails, error is returned to component

---

## Backend Token Validation

### Step-by-Step Process

#### 1. Request Arrives at FastAPI

**File**: `kcloft-backend/app/routers/question.py`

```python
@router.get("/", response_model=list[QuestionOut], dependencies=[Depends(verify_token)])
def read_questions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_question.get_questions(db, skip, limit)
```

**What happens:**
1. Request arrives at `/questions/` endpoint
2. FastAPI dependency system calls `verify_token()` first
3. If token is valid, request proceeds to handler
4. If token is invalid, 401 error is returned

#### 2. Token Extraction (`auth.py`)

**File**: `kcloft-backend/app/auth.py`

```python
bearer_scheme = HTTPBearer()

def verify_token(credentials=Depends(bearer_scheme)):
    token = credentials.credentials  # Extracts token from "Bearer {token}" header
```

**What happens:**
1. `HTTPBearer()` extracts `Authorization` header
2. Parses `Bearer {token}` format
3. Extracts the token string

#### 3. JWT Decoding

```python
def decode_jwt_payload(token: str) -> dict:
    # JWT format: header.payload.signature
    parts = token.split('.')
    
    # Decode payload (second part)
    payload_b64 = parts[1]
    # Add padding if needed
    padding = 4 - len(payload_b64) % 4
    if padding != 4:
        payload_b64 += '=' * padding
    
    payload_bytes = base64.urlsafe_b64decode(payload_b64)
    payload = json.loads(payload_bytes.decode('utf-8'))
    return payload
```

**What happens:**
1. Token is split into 3 parts (header.payload.signature)
2. Payload (middle part) is base64 decoded
3. JSON is parsed to get token claims

#### 4. Token Validation

```python
# Verify issuer matches expected tenant
valid_issuers = [
    f"https://login.microsoftonline.com/{TENANT_ID}/v2.0",
    f"https://login.microsoftonline.com/{TENANT_ID}/",
    f"https://sts.windows.net/{TENANT_ID}/",
]

if token_issuer not in valid_issuers and TENANT_ID not in token_issuer:
    raise HTTPException(status_code=401, detail="Invalid token issuer")

# Check expiration
exp = payload.get("exp")
if exp:
    current_time = time.time()
    if exp < current_time:
        raise HTTPException(status_code=401, detail="Token has expired")
```

**Validation Checks:**
1. **Issuer Validation**: Token must be from correct Azure AD tenant
2. **Expiration Check**: Token must not be expired
3. **Format Validation**: Token must be valid JWT format

**Accepted Issuer Formats:**
- `https://login.microsoftonline.com/{TENANT_ID}/v2.0`
- `https://login.microsoftonline.com/{TENANT_ID}/`
- `https://sts.windows.net/{TENANT_ID}/`

#### 5. Token Validation Success

```python
# Token is valid - return payload
print("DEBUG: Token validation successful")
return payload  # Returns decoded JWT payload
```

**What happens:**
1. If all validations pass, token payload is returned
2. Request handler receives validated token data
3. API endpoint processes the request
4. Response is returned to frontend

---

## Complete Request Cycle

### Example: Fetching Questions

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. USER ACTION                                                 │
│    User clicks "Refresh Questions" button                       │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. FRONTEND: Component Call                                     │
│    HomeView.vue: fetchQuestions()                              │
│    → apiClient.get("/questions/")                              │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. FRONTEND: Request Interceptor                                │
│    api.ts: Request Interceptor                                       │
│    → getAccessToken()                                          │
│    → Adds: Authorization: Bearer {token}                       │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. FRONTEND: Token Acquisition                                  │
│    authService.ts: getAccessToken()                            │
│    → msalInstance.acquireTokenSilent()                         │
│    → Returns: Access Token (JWT)                                │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. NETWORK: HTTP Request                                        │
│    GET http://localhost:8000/questions/                         │
│    Headers:                                                     │
│      Authorization: Bearer eyJhbGciOiJSUzI1NiIs...             │
│      Content-Type: application/json                             │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. BACKEND: CORS Middleware                                    │
│    main.py: CORSMiddleware                                      │
│    → Validates origin                                          │
│    → Adds CORS headers                                          │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. BACKEND: Token Validation                                   │
│    routers/question.py: verify_token dependency                 │
│    → auth.py: verify_token()                                    │
│    → Extracts token from Authorization header                   │
│    → Decodes JWT payload                                        │
│    → Validates issuer (tenant ID)                               │
│    → Validates expiration                                       │
│    → Returns payload if valid                                   │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 8. BACKEND: Request Handler                                     │
│    routers/question.py: read_questions()                        │
│    → crud/question.py: get_questions()                          │
│    → Database query                                             │
│    → Returns: List of questions                                 │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 9. NETWORK: HTTP Response                                       │
│    Status: 200 OK                                               │
│    Body: [{"id": 1, "question_text": "...", ...}]              │
│    Headers:                                                     │
│      Access-Control-Allow-Origin: http://localhost:5173         │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 10. FRONTEND: Response Handling                                 │
│     api.ts: Response Interceptor                               │
│     → Returns response to component                             │
│     → HomeView.vue: Updates questions state                     │
│     → UI updates with data                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Configuration

### Frontend Configuration

**File**: `kcloft-app/src/auth/authConfig.ts`

```typescript
export const msalConfig = {
  auth: {
    clientId: "d4552121-7ccf-4875-8b0a-c71a7f5c8c28",  // Azure AD App ID
    authority: "https://login.microsoftonline.com/109199d4-f7c0-4027-bcd7-9937e7fb177b",  // Tenant ID
    redirectUri: "http://localhost:5173/"  // Frontend URL
  }
};
```

**Environment Variables:**
- Can be moved to `.env` file:
  ```
  VITE_AZURE_CLIENT_ID=...
  VITE_AZURE_TENANT_ID=...
  VITE_API_BASE_URL=http://localhost:8000
  ```

### Backend Configuration

**File**: `kcloft-backend/app/auth.py`

```python
TENANT_ID = os.getenv("TENANT_ID", "109199d4-f7c0-4027-bcd7-9937e7fb177b")
AUDIENCE = os.getenv("CLIENT_ID", "d4552121-7ccf-4875-8b0a-c71a7f5c8c28")
```

**Environment Variables:**
- Create `.env` file in `kcloft-backend/`:
  ```
  TENANT_ID=109199d4-f7c0-4027-bcd7-9937e7fb177b
  CLIENT_ID=d4552121-7ccf-4875-8b0a-c71a7f5c8c28
  DATABASE_URL=postgresql://user:password@localhost/dbname
  ```

### CORS Configuration

**File**: `kcloft-backend/app/main.py`

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**For Production:**
- Replace `localhost:5173` with your production frontend URL
- Restrict `allow_methods` to only needed methods
- Restrict `allow_headers` to only needed headers

---

## Troubleshooting

### Common Issues

#### 1. "interaction_in_progress" Error

**Symptom**: Error when trying to login or get token

**Cause**: MSAL is already