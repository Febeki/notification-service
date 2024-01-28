import axios from "axios";
import { BACKEND_URL } from "../config/constants";

const useAxios = () => {
  const axiosInstance = axios.create({
    baseURL: BACKEND_URL,
    withCredentials: true,
  });

  return axiosInstance;
};

export default useAxios;
