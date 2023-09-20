import { React } from 'react';
import { Navbar, Container, Button, Dropdown } from 'react-bootstrap';
import { ReactComponent as Logo } from '../images/logo.svg';
import axios from 'axios';

const navbarStyle = {
  backgroundColor: '#FAD',
  textColor: '#F08',
};

const Header = ({
  title,
  currentUser,
  removeToken,
  setShowModal,
  notifier,
  images,
  setImages,
}) => {
  function logMeOut() {
    axios({
      method: 'POST',
      url: 'http://localhost:5000/logout',
    })
      .then((_) => {
        removeToken();
        notifier('Logged out');
        setImages(
          images.map((image) =>
            image.saved ? { ...image, saved: false } : image,
          ),
        );
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
        }
      });
  }

  return (
    <>
      <Navbar style={navbarStyle}>
        <Container>
          <Logo alt={title} style={{ maxWidth: '12rem', maxHeight: '2rem' }} />
          {currentUser ? (
            <>
              <Dropdown>
                <Dropdown.Toggle variant="primary" id="dropdown-basic">
                  {currentUser['name']}
                </Dropdown.Toggle>

                <Dropdown.Menu>
                  <Dropdown.Item onClick={logMeOut}>Logout</Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            </>
          ) : (
            <>
              <Button onClick={() => setShowModal(true)}>Login</Button>
            </>
          )}
        </Container>
      </Navbar>
    </>
  );
};

export default Header;
