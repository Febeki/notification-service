import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import useAxios from "../../../services/useAxios";

import { URLs } from "../../../config/constants";

import { Link } from "react-router-dom";

const ClientsPage = () => {
  const navigate = useNavigate();
  const [clients, setClients] = useState([]);
  const api = useAxios();

  useEffect(() => {
    getClients();
  }, []);

  const getClients = async () => {
    await api
      .get(URLs.CLIENTS)
      .then((response) => {
        if (response.status === 200) {
          setClients(response.data);
        }
      })
      .catch((error) => {
        console.error("Error fetching clients:", error);
        if (error.response && error.response.status === 401)
          navigate("/login");
      });
  };

  const handleDeleteClient = async (clientId) => {
    try {
      await api.delete(`${URLs.CLIENTS}${clientId}`);
      setClients(clients.filter((client) => client.id !== clientId));
    } catch (error) {
      console.error("Error deleting client:", error);
    }
  };

  return (
    <div className="mt-5">
      <h1 className="text-center">Список клиентов</h1>
      <Link to={`/`} className="btn btn-dark mb-3">
        Перейти к рассылкам
      </Link>
      <Link to="/new-client" className="btn btn-success mb-3">
        Добавить клиента
      </Link>
      <table className="table table-bordered table-dark">
        <thead>
          <tr>
            <th className="text-center">Номер телефона</th>
            <th className="text-center">Код мобильного оператора</th>
            <th className="text-center">Тег</th>
            <th className="text-center">Часовой пояс</th>
            <th className="text-center">Действия</th>
          </tr>
        </thead>
        <tbody>
          {clients.map((cl) => (
            <tr key={cl.id}>
              <td className="text-center">{cl.phone_number}</td>
              <td className="text-center">
                {cl.mobile_operator_code}
              </td>
              <td className="text-center">{cl.tag}</td>
              <td className="text-center">{cl.timezone}</td>
              <td className="text-center">
                <button
                  className="btn btn-danger"
                  onClick={() => handleDeleteClient(cl.id)}
                >
                  Удалить
                </button>
                <Link to={`/clients/${cl.id}`}>
                  <button className="btn btn-warning">
                    Изменить
                  </button>
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ClientsPage;
