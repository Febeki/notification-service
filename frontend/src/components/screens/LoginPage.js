import { useContext } from "react";

import AuthContext from "../../context/AuthContext";

const LoginPage = () => {
  const { loginUser } = useContext(AuthContext);

  return (
    <div className="container mt-5">
      <form
        onSubmit={loginUser}
        className="w-50 mx-auto d-grid gap-3 border border-dark rounded p-3 border-2"
      >
        <div className="form-group mb-3">
          <input
            type="text"
            className="form-control"
            name="username"
            placeholder="Введите имя пользователя"
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
    </div>
  );
};

export default LoginPage;
