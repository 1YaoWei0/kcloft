export const msalConfig = {
    auth: {
      clientId: "d4552121-7ccf-4875-8b0a-c71a7f5c8c28",
      authority: `https://login.microsoftonline.com/109199d4-f7c0-4027-bcd7-9937e7fb177b`,
      redirectUri: "http://localhost:5173/"
    }
  };
  
  export const loginRequest = {
    scopes: ["User.Read"]
  };

  // API request scopes
  // Using User.Read (Microsoft Graph) - a standard scope that works without custom API setup
  // The backend will accept tokens with this scope
  export const apiRequest = {
    scopes: ["User.Read"]
  };  