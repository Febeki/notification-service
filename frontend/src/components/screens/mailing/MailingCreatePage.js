import React, { useState } from "react";
import useAxios from "../../../services/useAxios";
import { URLs } from "../../../config/constants";
import { useNavigate } from "react-router-dom";

import { Form, Button } from "react-bootstrap";

const NewMailing = () => {
  const api = useAxios();
  const navigate = useNavigate();
  const [mailingData, setMailingData] = useState({});

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setMailingData({
      ...mailingData,
      [name]: value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await api.post(URLs.MAILING, mailingData);
      if (response.status === 201) {
        navigate("/");
      }
    } catch (error) {
      console.error("Error creating mailing:", error);
    }
  };

  return (
    <div className="mt-5">
      <h1 className="text-center">Добавить новую рассылку</h1>
      <Form className="container" onSubmit={handleSubmit}>
        {[
          {
            label: "Дата и время начала",
            name: "start_time",
            placeholder: "2010-10-10T10:10:10Z",
          },
          {
            label: "Дата и время окончания",
            name: "end_time",
            placeholder: "2010-10-10T11:10:10Z",
          },
          {
            label: "Текст сообщения",
            name: "message_text",
            placeholder: "...",
          },
          {
            label: "Фильтр",
            name: "client_filter",
            placeholder: "Тег Код",
          },
        ].map(({ label, name, placeholder }) => (
          <Form.Group key={name}>
            <Form.Label>{label}</Form.Label>
            <Form.Control
              type="text"
              name={name}
              value={mailingData[name]}
              onChange={handleInputChange}
              placeholder={placeholder}
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
          <Button variant="primary" className="mt-3" type="submit">
            Создать
          </Button>
        </div>
      </Form>
    </div>
  );
};

export default NewMailing;
