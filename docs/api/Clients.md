### Clients

#### List Clients

- **Endpoint**: `/api/clients/`
- **Method**: GET
- **Description**: Show a list of all clients.
- **Authentication**: Required

#### Create Client

- **Endpoint**: `/api/clients/`
- **Method**: POST
- **Description**: Create a new client.
- **Authentication**: Required
- **Parameters**:
  - `phone_number` **required**: (string) The client's phone number.
  - `mobile_operator_code` **required**: (string) The mobile operator code.
  - `tag` **required**: (string) The client's tag.
  - `timezone` **required**: (string) The client's timezone.

#### Retrieve Client

- **Endpoint**: `/api/clients/{client_id}/`
- **Method**: GET
- **Description**: Retrieve details of a specific client.
- **Authentication**: Required

#### Update Client

- **Endpoint**: `/api/clients/{client_id}/`
- **Method**: PATCH
- **Description**: Update details of a specific client.
- **Authentication**: Required
- **Parameters**:
  - `phone_number`: (string) The client's phone number.
  - `mobile_operator_code`: (string) The mobile operator code.
  - `tag`: (string) The client's tag.
  - `timezone`: (string) The client's timezone.

#### Delete Client

- **Endpoint**: `/api/clients/{client_id}/`
- **Method**: DELETE
- **Description**: Delete a specific client.
- **Authentication**: Required