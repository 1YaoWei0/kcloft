import { PublicClientApplication } from "@azure/msal-browser";
import type { SilentRequest } from "@azure/msal-browser";
import { msalConfig, apiRequest } from "./authConfig";

export const msalInstance = new PublicClientApplication(msalConfig);

let isMsalInitialized = false;

export async function ensureMsalInitialized() {
  if (!isMsalInitialized) {
    await msalInstance.initialize(); // Ensure this is the correct initialization method
    isMsalInitialized = true;
  }
}

/**
 * Get an access token for API calls
 * @returns The access token string, or null if unable to get token
 */
export async function getAccessToken(): Promise<string | null> {
  await ensureMsalInitialized();
  
  const account = msalInstance.getActiveAccount();
  if (!account) {
    const accounts = msalInstance.getAllAccounts();
    if (accounts.length > 0 && accounts[0]) {
      msalInstance.setActiveAccount(accounts[0]);
    } else {
      return null;
    }
  }

  const activeAccount = msalInstance.getActiveAccount();
  if (!activeAccount) {
    return null;
  }

  const request: SilentRequest = {
    ...apiRequest,
    account: activeAccount,
  };

  try {
    const response = await msalInstance.acquireTokenSilent(request);
    console.log("Token acquired successfully");
    return response.accessToken;
  } catch (error: any) {
    console.error("Silent token acquisition failed:", error);
    // If it's an interaction required error, we might need to login again
    if (error.errorCode === "interaction_required" || error.errorCode === "consent_required") {
      console.warn("User interaction required - token cannot be acquired silently");
    }
    // If silent token acquisition fails, return null
    // The user will need to login again or we can trigger interactive login
    return null;
  }
}