import React, { useState } from "react";
import useAxios from "../../../services/useAxios";
import { URLs } from "../../../config/constants";
import { useNavigate } from "react-router-dom";

import { Form, Button } from "react-bootstrap";

const NewClient = () => {
  const api = useAxios();
  const navigate = useNavigate();
  const [clientData, setClientData] = useState({});

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setClientData({
      ...clientData,
      [name]: value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await api.post(URLs.CLIENTS, clientData);
      if (response.status === 201) {
        navigate("/clients");
      }
    } catch (error) {
      console.error("Error creating client:", error);
    }
  };

  return (
    <div className="mt-5">
      <h1 className="text-center">Добавить нового клиента</h1>
      <Form className="container" onSubmit={handleSubmit}>
        {[
          {
            label: "Номер телефона",
            name: "phone_number",
            placeholder: "7XXXXXXXXXX",
          },
          {
            label: "Код мобильного оператора",
            name: "mobile_operator_code",
            placeholder: "912",
          },
          { label: "Тег", name: "tag", placeholder: "Python" },
          {
            label: "Часовой пояс",
            name: "timezone",
            placeholder: "Europe/Moscow",
          },
        ].map(({ label, name, placeholder }) => (
          <Form.Group key={name}>
            <Form.Label>{label}</Form.Label>
            <Form.Control
              type="text"
              name={name}
              value={clientData[name] || ""}
              onChange={handleInputChange}
              className="form-control form-control-lg mb-3"
              placeholder={placeholder}
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
            Создать
          </Button>
        </div>
      </Form>
    </div>
  );
};

export default NewClient;
