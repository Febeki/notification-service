import { useEffect, useContext } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext';
import jwtDecode from "jwt-decode";

const GoogleAuthCallback = () => {
    const { setAuthTokens, setUser } = useContext(AuthContext);
    const location = useLocation();
    const navigate = useNavigate();

    useEffect(() => {
        const queryParams = new URLSearchParams(location.search);
        const accessToken = queryParams.get('access_token');
        const refreshToken = queryParams.get('refresh_token');

        if (accessToken && refreshToken) {
            const tokens = { access: accessToken, refresh: refreshToken };
            localStorage.setItem('authTokens', JSON.stringify({ access: accessToken, refresh: refreshToken }));
            console.log(jwtDecode(accessToken))
            setAuthTokens(tokens);  // Обновляем состояние токенов в контексте
            setUser(jwtDecode(accessToken));  // Обновляем пользователя в контексте

            // Перенаправляем на главную страницу
            navigate('/');
        } else {
            // Если токены не найдены, перенаправляем на страницу входа
            navigate('/');
        }
    }, [location, navigate, setAuthTokens, setUser]);

    return <div>Loading...</div>;
};

export default GoogleAuthCallback;