import { useState, useEffect } from "react";
import useAxios from "../../../services/useAxios";
import { useNavigate } from "react-router-dom";
import { URLs } from "../../../config/constants";

import { Link } from "react-router-dom";

const MailingPage = () => {
  const [mailing, setMailing] = useState([]);
  const api = useAxios();
  const navigate = useNavigate();

  useEffect(() => {
    getMailing();
  }, []);

  const getMailing = async () => {
    await api
      .get(URLs.MAILING)
      .then((response) => {
        if (response.status === 200) {
          setMailing(response.data);
        }
      })
      .catch((error) => {
        console.error("Error fetching mailing:", error);
        if (error.response && error.response.status === 401)
          navigate("/login");
      });
  };

  const handleDeleteMailing = async (mailingId) => {
    try {
      await api.delete(`${URLs.MAILING}${mailingId}`);
      setMailing(mailing.filter((ml) => ml.id !== mailingId));
    } catch (error) {
      console.error("Error deleting mailing:", error);
    }
  };

  return (
    <div className="mt-5">
      <h1 className="text-center">Список рассылок</h1>
      <Link to={`/clients`} className="btn btn-dark mb-3">
        Перейти к клиентам
      </Link>
      <Link to="/new-mailing" className="btn btn-success mb-3">
        Добавить рассылку
      </Link>
      <table className="table table-bordered table-dark">
        <thead>
          <tr>
            <th className="text-center">Начало</th>
            <th className="text-center">Конец</th>
            <th className="text-center">Сообщение</th>
            <th className="text-center">Фильтр</th>
            <th className="text-center">Действия</th>
          </tr>
        </thead>
        <tbody>
          {mailing.map((ml) => (
            <tr key={ml.id}>
              <td className="text-center">{ml.start_time}</td>
              <td className="text-center">{ml.end_time}</td>
              <td className="text-center">{ml.message_text}</td>
              <td className="text-center">{ml.client_filter}</td>
              <td className="text-center">
                <button
                  className="btn btn-danger"
                  onClick={() => handleDeleteMailing(ml.id)}
                >
                  Удалить
                </button>
                <Link to={`${ml.id}`}>
                  <button className="btn btn-warning">
                    Изменить
                  </button>
                </Link>
                <Link to={`mailing-detail/${ml.id}`}>
                  <button className="btn btn-primary">Инфо</button>
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default MailingPage;
