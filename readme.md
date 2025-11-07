# KCLOFT

> The purpose of developing this web project is to meet the practice questions requirement and improve my coding skills.

## Tech Stack

> I want to develop the MVP version first.

### Front end

> Vue

- Routing: Vue Router
- API requests: Axios
- Auth: MSAL.js for Entra ID login

### Back end

> FastAPI

- Auth middleware validating Entra ID JWT tokens
- File upload endpoint (Excel → question DB)
- Export endpoint (generate Excel/PDF)
- REST API for CRUD questions + practice flow

### Database

> PostgreSQL

- questions (text, type, choices JSON, answer, tags JSON, explanation)
- sources (optional: exam, chapter etc.)

### Storage

> OneDrive

- Store uploaded original Excel files OR exported files
- Access through Microsoft Graph API

## Features

### Admin / Teacher side

- Upload questions from Excel
- View, edit, delete questions
- Export selected questions to Excel or PDF

### Student side

- Login via Azure Entra ID
- Practice mode: select topic → receive random questions → see score + explanations

### Not included (yet)

- Word export
- Full exam/timing system
- Analytics
- Tag management UI (tags stored automatically for now)