import { React } from 'react';
import { Navbar, Container, Button } from 'react-bootstrap';
import { ReactComponent as Logo } from '../images/logo.svg';
import axios from 'axios';

const navbarStyle = {
  backgroundColor: '#FAD',
  textColor: '#F08',
};

const Header = ({
  title,
  token,
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
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
  }

  return (
    <>
      <Navbar style={navbarStyle}>
        <Container>
          <Logo alt={title} style={{ maxWidth: '12rem', maxHeight: '2rem' }} />
          {!token && token !== '' && token !== undefined ? (
            <>
              <Button onClick={() => setShowModal(true)}>Login</Button>
            </>
          ) : (
            <>
              <Button variant="secondary" onClick={logMeOut}>
                Logout
              </Button>
            </>
          )}
        </Container>
      </Navbar>
    </>
  );
};

export default Header;
