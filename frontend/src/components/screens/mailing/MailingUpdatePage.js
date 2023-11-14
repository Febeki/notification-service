import { useState, useEffect } from "react";
import useAxios from "../../../services/useAxios";

import { URLs } from "../../../config/constants";

import { useParams, useNavigate } from "react-router-dom";

import { Form, Button } from "react-bootstrap";

const MailingUpdatePage = () => {
  const { id } = useParams();
  const api = useAxios();
  const navigate = useNavigate();
  const [mailing, setMailing] = useState({});
  const [error, setError] = useState("");
  const [showError, setShowError] = useState(false);

  useEffect(() => {
    getMailingDetails();
  }, []);

  const getMailingDetails = async () => {
    try {
      const response = await api.get(`${URLs.MAILING}${id}/`);
      if (response.status === 200) {
        setMailing(response.data);
      }
    } catch (error) {
      console.error("Error fetching mailing details:", error);
    }
  };

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setMailing({
      ...mailing,
      [name]: value,
    });
  };

  const handleSave = async (event) => {
    event.preventDefault();

    try {
      const response = await api.patch(
        `${URLs.MAILING}${id}/`,
        mailing
      );
      if (response.status === 200) {
        navigate("/");
      }
    } catch (error) {
      setError("Ошибка при сохранении рассылки");
      setShowError(true);
      setTimeout(() => {
        setShowError(false);
      }, 5000);
      console.error("Error saving mailing:", error);
    }
  };

  return (
    <div className="mt-5">
      <h1 className="text-center">Данные рассылки</h1>
      {showError && <div className="alert alert-danger">{error}</div>}
      <Form className="container" onSubmit={handleSave}>
        {[
          { label: "Дата и время начала", name: "start_time" },
          { label: "Дата и время окончания", name: "end_time" },
          { label: "Текст сообщения", name: "message_text" },
          { label: "Фильтр", name: "client_filter" },
        ].map(({ label, name }) => (
          <Form.Group key={name}>
            <Form.Label>{label}</Form.Label>
            <Form.Control
              type="text"
              name={name}
              value={mailing[name]}
              onChange={handleInputChange}
              className="form-control form-control-lg mb-3"
            />
          </Form.Group>
        ))}
        <div className="text-center">
          <Button
            variant="secondary"
            className="mt-3"
            onClick={() => navigate("/")}
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

export default MailingUpdatePage;
