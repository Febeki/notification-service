### Mailings

#### List Mailings

- **Endpoint**: `/api/mailing/`
- **Method**: GET
- **Description**: Show a list of all mailings.
- **Authentication**: Required

#### Create Mailing

- **Endpoint**: `/api/mailing/`
- **Method**: POST
- **Description**: Create a new mailing.
- **Authentication**: Required
- **Parameters**:
  - `start_time` **required**: (datetime) The start time of the mailing.
  - `end_time` **required**: (datetime) The end time of the mailing.
  - `message_text` **required**: (string) The text of the message.
  - `client_filter`: (string, optional) Filter clients by tag and mobile operator code.

#### Retrieve Mailing

- **Endpoint**: `/api/mailing/{mailing_id}/`
- **Method**: GET
- **Description**: Retrieve details of a specific mailing.
- **Authentication**: Required

#### Update Mailing

- **Endpoint**: `/api/mailing/{mailing_id}/`
- **Method**: PUT
- **Description**: Update details of a specific mailing.
- **Authentication**: Required
- **Parameters**:
  - `start_time`: (datetime) The start time of the mailing.
  - `end_time`: (datetime) The end time of the mailing.
  - `message_text`: (string) The text of the message.
  - `client_filter`: (string, optional) Filter clients by tag and mobile operator code.

#### Delete Mailing

- **Endpoint**: `/api/mailing/{mailing_id}/`
- **Method**: DELETE
- **Description**: Delete a specific mailing.
- **Authentication**: Required

#### Detail Mailing

- **Endpoint**: `/api/mailing-detail/{mailing_id}/`
- **Method**: GET
- **Description**: Retrieve details of a specific mailing, including associated messages.
- **Authentication**: Required