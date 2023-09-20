import { useState } from 'react';
import { Container, Row, Col, Form, Button, Modal } from 'react-bootstrap';
import axios from 'axios';

const LoginModal = ({
  setToken,
  getSavedImages,
  showModal,
  setShowModal,
  notifier,
}) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
  });
  const [useSignup, setSignup] = useState(false);

  function login(event) {
    axios({
      method: 'POST',
      url: 'http://localhost:5000/token',
      data: {
        email: formData.email,
        password: formData.password,
      },
    })
      .then((response) => {
        setToken(response.data.access_token);
        setShowModal(false);
        notifier.success('Logged in');
        getSavedImages(response.data.access_token);

        setFormData({
          email: '',
          password: '',
          name: '',
        });
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          notifier.error(error.response.data['error']);

          setFormData({
            email: '',
            password: '',
            name: '',
          });
        }
      });

    event.preventDefault();
  }

  function signup(event) {
    axios({
      method: 'POST',
      url: 'http://localhost:5000/register',
      data: {
        email: formData.email,
        password: formData.password,
        name: formData.name,
      },
    })
      .then((response) => {
        setToken(response.data.access_token);
        setShowModal(false);
        notifier.success('Welcome, thanks for signing up');
        setSignup(false);
        setFormData({
          email: '',
          password: '',
          name: '',
        });
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          notifier.error(error.response.data['error']);

          setFormData({
            email: '',
            password: '',
            name: '',
          });
        }
      });

    event.preventDefault();
  }

  function handleChange(event) {
    const { value, name } = event.target;
    setFormData((prevNote) => ({
      ...prevNote,
      [name]: value,
    }));
  }

  return (
    <Modal
      size="lg"
      show={showModal}
      onHide={() => {
        setShowModal(false);
        setFormData({
          email: '',
          password: '',
          name: '',
        });
      }}
    >
      <Modal.Header className="justify-content-center" closeButton>
        <Modal.Title>{useSignup ? 'Sign Up' : 'Login'}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Container>
          <Row className="justify-content-center">
            <Form onSubmit={useSignup ? signup : login}>
              {useSignup && (
                <Form.Group className="mb-3" controlId="formName">
                  <Form.Label>Name</Form.Label>
                  <Form.Control
                    onChange={handleChange}
                    type="name"
                    text={formData.name}
                    name="name"
                    placeholder="Enter name"
                    value={formData.name}
                  />
                </Form.Group>
              )}
              <Form.Group className="mb-3" controlId="formEmail">
                <Form.Label>Email Address</Form.Label>
                <Form.Control
                  onChange={handleChange}
                  type="email"
                  text={formData.email}
                  name="email"
                  placeholder="Enter email"
                  value={formData.email}
                />
              </Form.Group>
              <Form.Group className="mb-3" controlId="formPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control
                  onChange={handleChange}
                  type="password"
                  text={formData.password}
                  name="password"
                  placeholder="Enter password"
                  value={formData.password}
                />
              </Form.Group>
              <Row className="align-items-center">
                <Col>
                  <Button variant="primary" type="submit">
                    Submit
                  </Button>
                  {useSignup ? (
                    <Button variant="light" onClick={() => setSignup(false)}>
                      Return to Login
                    </Button>
                  ) : (
                    <Button variant="light" onClick={() => setSignup(true)}>
                      Create account
                    </Button>
                  )}
                </Col>
              </Row>
            </Form>
          </Row>
        </Container>
      </Modal.Body>
    </Modal>
  );
};

export default LoginModal;
