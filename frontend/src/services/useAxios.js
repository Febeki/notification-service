import { useContext } from "react";
import axios from "axios";
import dayjs from "dayjs";
import jwtDecode from "jwt-decode";

import { BACKEND_URL, URLs } from "../config/constants";
import AuthContext from "../context/AuthContext";

const useAxios = () => {
  const { authTokens, setUser, setAuthTokens } =
    useContext(AuthContext);

  const axiosInstance = axios.create({
    baseURL: BACKEND_URL,
    headers: {
      Authorization: `Bearer ${authTokens?.access}`,
    },
  });

  axiosInstance.interceptors.request.use(async (req) => {
    const user = jwtDecode(authTokens.access);
    const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;

    if (!isExpired) return req;

    const response = await axios.post(
      `${BACKEND_URL}${URLs.TOKEN_REFRESH}`,
      {
        refresh: authTokens.refresh,
      }
    );

    localStorage.setItem("authTokens", JSON.stringify(response.data));

    setAuthTokens(response.data);
    setUser(jwtDecode(response.data.access));

    req.headers.Authorization = `Bearer ${response.data.access}`;
    return req;
  });

  return axiosInstance;
};

export default useAxios;
