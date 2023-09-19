import { useState } from 'react';
import { Container, Row, Col, Form, Button } from 'react-bootstrap';
import axios from 'axios';

const Login = ({ setToken, getSavedImages }) => {
  const [loginForm, setloginForm] = useState({
    email: '',
    password: '',
  });

  function logMeIn(event) {
    axios({
      method: 'POST',
      url: 'http://localhost:5000/token',
      data: {
        email: loginForm.email,
        password: loginForm.password,
      },
    })
      .then((response) => {
        setToken(response.data.access_token);
        getSavedImages(response.data.access_token);
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });

    setloginForm({
      email: '',
      password: '',
    });

    event.preventDefault();
  }

  function handleChange(event) {
    const { value, name } = event.target;
    setloginForm((prevNote) => ({
      ...prevNote,
      [name]: value,
    }));
  }

  return (
    <Container className="mt-4">
      <Row className="justify-content-center">
        <h1>Login</h1>
      </Row>
      <Row className="justify-content-center">
        <Form onSubmit={logMeIn}>
          <Form.Row>
            <Col>
              <Form.Control
                onChange={handleChange}
                type="email"
                text={loginForm.email}
                name="email"
                placeholder="Email"
                value={loginForm.email}
              />
            </Col>
            <Col>
              <Form.Control
                onChange={handleChange}
                type="password"
                text={loginForm.password}
                name="password"
                placeholder="Password"
                value={loginForm.password}
              />
            </Col>
            <Col>
              <Button variant="primary" type="submit">
                Submit
              </Button>
            </Col>
          </Form.Row>
        </Form>
      </Row>
    </Container>
  );
};

export default Login;
