# Front End Guide

## Install Guide

> Install the Core Tools
> Make sure you have:
> Node.js (LTS version recommended):
> https://nodejs.org/

Check versions after installation:

```bash
node -v
npm -v
```

Create a Vue Project with Vite

Run this command in a terminal:

```bash
npm create vite@latest kcloft-app -- --template vue
```

Then:

```bash
cd kcloft-app
npm install
npm run dev
```

> Note: When I process 'npm install' command. I got some error messages like below:
> *error 'patch-package' is not recognized as an internal or external command*
> The only solution is to install the 'patch-package' first `npm install -g patch-package`.
> Then process the `npm install` command.

Visit the local URL shown in the terminal (usually: [http://localhost:5173](http://localhost:5173)).

Congratulations — Vue is alive.

Recommended Extensions for VS Code
If you’re using Visual Studio Code:

• Vue Language Features (Volar)
• TypeScript Vue Plugin (if using TypeScript later)
• ESLint (for cleaner code)

Directory Structure (Vite + Vue)

```
kcloft-app
 ├─ src
 │   ├─ assets       # images, icons, etc.
 │   ├─ components   # reusable UI parts
 │   ├─ App.vue      # main app component
 │   └─ main.js      # entry file
 ├─ index.html
 ├─ package.json
 └─ vite.config.js
```

Clean. Simple. Tidy.

Install Vue Router (you’ll need it later)

```bash
npm install vue-router
```

Install Axios (for API calls)

```bash
npm install axios
```

Prepare for Azure Entra ID Login
We will later add:

```bash
npm install @azure/msal-browser
```