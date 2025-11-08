import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import router from "./router";
import { msalInstance, ensureMsalInitialized } from "./auth/authService";

async function bootstrap() {
  // Step 1: Initialize MSAL first
  await ensureMsalInitialized();
  
  // Step 2: Handle redirect login before mounting the app
  const redirectResult = await msalInstance.handleRedirectPromise();

  if (redirectResult) {
    msalInstance.setActiveAccount(redirectResult.account);
  } else {
    // If no redirect happened, pick first account if available
    const accounts = msalInstance.getAllAccounts();
    if (accounts.length > 0 && accounts[0]) {
      msalInstance.setActiveAccount(accounts[0]);
    }
  }

  const app = createApp(App);
  app.use(router);
  app.mount("#app");

  // Step 2: Navigate programmatically to home if just logged in
  if (redirectResult) {
    router.push({ name: "home" });
  }
}

bootstrap();
