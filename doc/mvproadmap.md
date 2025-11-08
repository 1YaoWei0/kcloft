Here’s a recommended **MVP roadmap**, aligned with your product goals:

---

## ✅ 🔥 Next Focus: Authentication

Right now your login page is UI only.
Users need to log in **securely** with Azure Entra ID (what used to be Azure AD).

### Suggested next tasks

1. Implement Azure Entra login from Vue using OAuth2/OpenID Connect
2. Backend validates and manages user identity (access tokens)
3. Protect API routes (only authenticated users can access questions)

Once this is working:
→ Users can log in and stay logged in
→ Frontend knows **who** the user is
→ Backend validates requests with a **token**

This foundation is essential before building admin tools.

---

## ✅ After Authentication: Admin Features (Excel Import MVP)

Your app’s unique value is **importing / editing / managing questions**.

Admin Portal:

* Upload Excel (.xlsx) → parse → save to DB
* Display question list with pagination + CRUD
* Validate duplicate questions / missing fields

This enables teachers/admins to build the question bank.

---

## ✅ Then: Practice & Exam Mode

Student Interface:

* Fetch random or categorized questions
* Track answers and score
* Show results + explanations

This is the visible “value” for learners.

---

### 🧩 Full MVP Feature Roadmap

| Phase | Feature                        | Purpose                 |
| ----- | ------------------------------ | ----------------------- |
| 1     | ✅ Login UI, FastAPI, PosgreSQL | foundation              |
| 2     | 🔐 Azure Entra ID Auth         | secure users + sessions |
| 3     | 🛠 Admin: Excel Import + CRUD  | build question bank     |
| 4     | 🧪 Practice Mode               | let users do exercises  |
| 5     | 📄 Export Questions (Word/PDF) | optional MVP stretch    |

---

### Technical Plans for each phase

**Authentication**

* Vue → MSAL.js (Microsoft Authentication Library)
* FastAPI → validate JWT tokens
* Store limited user profile in DB (roles: admin / student)

**Excel Parsing**

* Backend: `pandas` / `openpyxl` / `fastapi-upload`
* File validation + database insert

**UI for Admin**

* Question table (Vue + Data Table)
* Edit modal
* Tags / filtering

**Practice/Exam**

* Timed / untimed
* Single/multiple-choice
* Store answers for analytics later

---

## ✅ Recommendation for your next concrete task

➡️ **Integrate Azure Entra ID login** (Phase 2)
I will set this up cleanly and securely.

We’ll:

1. Register your Vue app in Azure Entra
2. Install MSAL.js in your front end
3. Implement redirect login flow
4. Add a route guard (block pages if not logged in)
5. Add FastAPI middleware to validate access tokens

Once this step is done → you’ll have a *real* authenticated application.

---

If you’re ready, I will start by preparing:

✅ Azure App Registration instructions
✅ Required Redirect URIs
✅ Recommended Entra settings
✅ Vue MSAL integration code
✅ Token validation in FastAPI

Would you like me to proceed with:

A) **Step-by-step Azure Portal setup screenshots + guidances**
or
B) **Jump directly into coding examples (because you already know Azure)**

Either choice — we keep building this awesome project 🚀
