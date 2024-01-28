import { createContext } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { BACKEND_URL, URLs } from "../config/constants";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const navigate = useNavigate();

  let loginUser = async (e) => {
    e.preventDefault();
    await axios
      .post(`${BACKEND_URL}${URLs.TOKEN}`, {
        email: e.target.email.value,
        password: e.target.password.value,
      }, { withCredentials: true } )
      .then((response) => {
        navigate("/");
        })
      .catch((error) => {
        alert("Неправильные данные!");
      });
  };

  const checkUserLoggedIn = async () => {
    try {
      await axios.get(`${BACKEND_URL}${URLs.CHECK_AUTH}`, { withCredentials: true });
    } catch (error) {
      if (error.response && error.response.status === 401) {
        navigate("/login");
      }
    }
  };

  let contextData = {
    loginUser,
    checkUserLoggedIn,
  };

  return (
    <AuthContext.Provider value={contextData}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;