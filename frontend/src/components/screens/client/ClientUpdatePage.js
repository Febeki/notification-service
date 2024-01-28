import { useState, useEffect } from "react";
import useAxios from "../../../services/useAxios";

import { URLs } from "../../../config/constants";

import { useParams, useNavigate } from "react-router-dom";

import { Form, Button } from "react-bootstrap";

const ClientUpdatePage = () => {
  const { id } = useParams();
  const api = useAxios();
  const navigate = useNavigate();
  const [client, setClient] = useState({});
  const [error, setError] = useState("");
  const [showError, setShowError] = useState(false);

  useEffect(() => {
    getClientDetails();
  }, []);

  const getClientDetails = async () => {
    try {
      const response = await api.get(`${URLs.CLIENTS}${id}/`);
      if (response.status === 200) {
        setClient(response.data);
      }
    } catch (error) {
      console.error("Error fetching client details:", error);
      if (error.response && error.response.status === 401)
        navigate("/login");
    }
  };

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setClient({
      ...client,
      [name]: value,
    });
  };

  const handleSave = async (event) => {
    event.preventDefault();

    try {
      const response = await api.patch(
        `${URLs.CLIENTS}${id}/`,
        client
      );
      if (response.status === 200) {
        navigate("/clients");
      }
    } catch (error) {
      setError("Ошибка при сохранении данных клиента");
      setShowError(true);
      setTimeout(() => {
        setShowError(false);
      }, 5000);
      console.error("Error saving client:", error);
    }
  };

  return (
    <div className="mt-5">
      <h1 className="text-center">Данные клиента</h1>
      {showError && <div className="alert alert-danger">{error}</div>}
      <Form className="container" onSubmit={handleSave}>
        {[
          { label: "Номер телефона", name: "phone_number" },
          {
            label: "Код мобильного оператора",
            name: "mobile_operator_code",
          },
          { label: "Тег", name: "tag" },
          { label: "Часовой пояс", name: "timezone" },
        ].map(({ label, name }) => (
          <Form.Group key={name}>
            <Form.Label>{label}</Form.Label>
            <Form.Control
              type="text"
              name={name}
              value={client[name]}
              onChange={handleInputChange}
              className="form-control form-control-lg mb-3"
            />
          </Form.Group>
        ))}
        <div className="text-center">
          <Button
            variant="secondary"
            className="mt-3"
            onClick={() => navigate("/clients")}
          >
            Назад
          </Button>
          <Button variant="primary" type="submit" className="mt-3">
            Сохранить
          </Button>
        </div>
      </Form>
    </div>
  );
};

export default ClientUpdatePage;
