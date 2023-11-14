### Authentication

#### Obtain Token

- **Endpoint**: `/api/token/`
- **Method**: POST
- **Description**: Obtain a JSON Web Token for authentication.
- **Parameters**:
  - `username` **required**: (string) User's username.
  - `password` **required**: (string) User's password.

#### Refresh Token

- **Endpoint**: `/api/token/refresh/`
- **Method**: POST
- **Description**: Refresh an expired JSON Web Token.
- **Parameters**:
  - `refresh` **required**: (string) The refresh token.