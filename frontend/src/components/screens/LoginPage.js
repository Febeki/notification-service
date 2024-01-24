import { useContext } from "react";

import AuthContext from "../../context/AuthContext";
import { BACKEND_URL, URLs } from "../../config/constants";

const LoginPage = () => {
  const { loginUser } = useContext(AuthContext);

  const handleGoogleLogin = () => {
    window.location.href = `${BACKEND_URL}${URLs.OAUTH_LOGIN}`;
  };

  return (
    <div className="container mt-5 w-50 mx-auto border border-dark rounded p-3 border-2">
      <form
        onSubmit={loginUser}
      >
        <div className="form-group mb-3">
          <input
            type="email"
            className="form-control"
            name="email"
            placeholder="Введите email"
          />
        </div>
        <div className="form-group mb-3">
          <input
            type="password"
            className="form-control"
            name="password"
            placeholder="Введите пароль"
          />
        </div>
        <button type="submit" className="btn btn-dark w-100">
          Войти
        </button>
      </form>
      <div className="text-center mt-3">
        <button
          onClick={handleGoogleLogin}
          className="btn btn-light border w-50"
          style={{ backgroundColor: '#f5f5f5' }}
        >
          <img
            src="https://img.icons8.com/color/30/000000/google-logo.png"
            alt="Google sign-in"
            style={{ marginRight: '10px' }}
          />
          Продолжить с Google
        </button>
      </div>
    </div>
  );
};

export default LoginPage;
