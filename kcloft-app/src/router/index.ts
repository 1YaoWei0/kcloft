import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";
import LoginView from "../views/LoginView.vue";
import HomeView from "../views/HomeView.vue";
import { msalInstance, ensureMsalInitialized } from "../auth/authService";

const routes: Array<RouteRecordRaw> = [
  { path: "/", name: "home", component: HomeView, meta: { requiresAuth: true } },
  { path: "/login", name: "login", component: LoginView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, _from, next) => {
  try {
    await ensureMsalInitialized(); // Ensure MSAL is initialized

    const accounts = msalInstance.getAllAccounts();

    if (to.meta.requiresAuth && accounts.length === 0) {
      // Only redirect if we're not already on the login page
      if (to.name !== "login") {
        await msalInstance.loginRedirect();
        return; // Don't call next() - loginRedirect will navigate away
      }
    }
    next();
  } catch (error) {
    console.error("Error during MSAL initialization or navigation:", error);
    // If it's an interaction_in_progress error, the redirect is already in progress
    // Just allow the navigation to proceed - MSAL will handle it
    if (error instanceof Error && error.message.includes("interaction_in_progress")) {
      return; // Don't call next() - let MSAL handle the redirect
    }
    next(false); // Cancel navigation on error
  }
});

export default router;
