import { useState } from 'react';
import { Container, Row, Form, Button, Modal } from 'react-bootstrap';
import axios from 'axios';

const LoginModal = ({ setToken, getSavedImages, showModal, setShowModal }) => {
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
        setShowModal(false);
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
    <Modal size="lg" show={showModal} onHide={() => setShowModal(false)}>
      <Modal.Header className="justify-content-center" closeButton>
        <Modal.Title>Login</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Container>
          <Row className="justify-content-center">
            <Form onSubmit={logMeIn}>
              <Form.Group className="mb-3" controlId="formEmail">
                <Form.Label>Email Address</Form.Label>
                <Form.Control
                  onChange={handleChange}
                  type="email"
                  text={loginForm.email}
                  name="email"
                  placeholder="Enter email"
                  value={loginForm.email}
                />
              </Form.Group>
              <Form.Group className="mb-3" controlId="formPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control
                  onChange={handleChange}
                  type="password"
                  text={loginForm.password}
                  name="password"
                  placeholder="Enter password"
                  value={loginForm.password}
                />
              </Form.Group>
              <Button variant="primary" type="submit">
                Submit
              </Button>
            </Form>
          </Row>
        </Container>
      </Modal.Body>
    </Modal>
  );
};

export default LoginModal;
