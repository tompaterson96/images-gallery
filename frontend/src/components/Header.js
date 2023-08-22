import React from 'react';
import { Navbar, Container } from 'react-bootstrap';
import { ReactComponent as Logo } from '../images/logo.svg';

const navbarStyle = {
  backgroundColor: '#FAD',
  textColor: '#F08',
};

const Header = ({ title }) => {
  return (
    <Navbar style={navbarStyle}>
      <Container>
        <Logo style={{ maxWidth: '12rem', maxHeight: '2rem' }} />
      </Container>
    </Navbar>
  );
};

export default Header;
