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


function Router() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/clients"
            element={
                <ClientsPage />
            }
          />
          <Route
            path="clients/:id"
            element={
                <ClientUpdatePage />
            }
          />
          <Route
            path="/new-client"
            element={
                <NewClient />
            }
          />
          <Route
            path="/"
            element={
                <MailingPage />
            }
          />
          <Route
            path="/:id"
            element={
                <MailingUpdatePage />
            }
          />
          <Route
            path="/mailing-detail/:id"
            element={
                <MailingInfoPage />
            }
          />
          <Route
            path="/new-mailing"
            element={
                <NewMailing />
            }
          />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default Router;
