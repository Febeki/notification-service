export const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000/';

export const URLs = {
  CHECK_AUTH: "api/check/login/",
  CLIENTS: "api/clients/",
  MAILING: "api/mailing/",
  TOKEN: "api/token/",
  TOKEN_REFRESH: "api/token/refresh/",
  OAUTH_LOGIN: "social-auth/login/google-oauth2/",
};
