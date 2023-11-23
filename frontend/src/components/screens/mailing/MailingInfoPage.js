import { useState, useEffect } from "react";
import useAxios from "../../../services/useAxios";
import { URLs } from "../../../config/constants";
import { useParams } from "react-router-dom";

const MailinginfoPage = () => {
  const { id } = useParams();
  const api = useAxios();
  const [mailingData, setMailingData] = useState({});

  useEffect(() => {
    getMailingDetails();
  }, []);

  const getMailingDetails = async () => {
    try {
      const response = await api.get(`${URLs.MAILING}${id}/`);
      if (response.status === 200) {
        setMailingData(response.data);
      }
    } catch (error) {
      console.error("Error fetching mailing details:", error);
    }
  };

  return (
    <div className="mt-5">
      {mailingData ? (
        <div className="text-center">
          <h1>Информация о рассылке</h1>
          <p>Время начала: {mailingData.start_time}</p>
          <p>Время окончания: {mailingData.end_time}</p>
          <p>Текст сообщения: {mailingData.message_text}</p>
          <p>Фильтр: {mailingData.client_filter}</p>

          <h2>Сообщения</h2>
          <table className="table table-bordered table-dark">
            <thead>
              <tr>
                <th>Дата создания</th>
                <th>Статус</th>
                <th>Номер телефона клиента</th>
                <th>Часовой пояс клиента</th>
              </tr>
            </thead>
            {mailingData.messages ? (
              <tbody>
                {mailingData.messages.map((message) => (
                  <tr key={message.id}>
                    <td>{message.created_at}</td>
                    <td>{message.status}</td>
                    <td>{message.client.phone_number}</td>
                    <td>{message.client.timezone}</td>
                  </tr>
                ))}
              </tbody>
            ) : (
              <tbody>
                <tr>
                  <td colSpan="2">No messages available</td>
                </tr>
              </tbody>
            )}
          </table>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default MailinginfoPage;
