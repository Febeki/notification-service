import { BrowserRouter, Route, Routes } from "react-router-dom";

import "bootstrap/dist/css/bootstrap.css";

import { AuthProvider } from "../../context/AuthContext.js";
import MailingPage from "../screens/mailing/MailingPage.js";
import ClientsPage from "../screens/client/ClientsPage.js";
import ClientUpdatePage from "../screens/client/ClientUpdatePage.js";
import MailingUpdatePage from "../screens/mailing/MailingUpdatePage.js";
import MailingInfoPage from "../screens/mailing/MailingInfoPage.js";
import NewMailing from "../screens/mailing/MailingCreatePage.js";
import NewClient from "../screens/client/ClientCreatePage.js";
import LoginPage from "../screens/LoginPage.js";
import PrivateRoute from "../routers/PrivateRoute.js";

import GoogleAuthCallback from "../../services/GoogleAuthCallback.js";

function Router() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/google-auth-callback" element={<GoogleAuthCallback />} />
          <Route
            path="/clients"
            element={
              <PrivateRoute>
                <ClientsPage />
              </PrivateRoute>
            }
          />
          <Route
            path="clients/:id"
            element={
              <PrivateRoute>
                <ClientUpdatePage />
              </PrivateRoute>
            }
          />
          <Route
            path="/new-client"
            element={
              <PrivateRoute>
                <NewClient />
              </PrivateRoute>
            }
          />
          <Route
            path="/"
            element={
              <PrivateRoute>
                <MailingPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/:id"
            element={
              <PrivateRoute>
                <MailingUpdatePage />
              </PrivateRoute>
            }
          />
          <Route
            path="/mailing-detail/:id"
            element={
              <PrivateRoute>
                <MailingInfoPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/new-mailing"
            element={
              <PrivateRoute>
                <NewMailing />
              </PrivateRoute>
            }
          />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default Router;
