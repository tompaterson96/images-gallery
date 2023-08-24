import { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Header from './components/Header';
import Search from './components/Search';
import ImageCard from './components/ImageCard';
import Welcome from './components/Welcome';
import { Container, Row, Col } from 'react-bootstrap';

const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000';

const App = () => {
  const [word, setWord] = useState('');
  const [images, setImages] = useState([]);

  console.log(images);

  const handleSearchSubmit = (ev) => {
    ev.preventDefault();
    fetch(`${API_URL}/new-image?query=${word}`)
      .then((result) => result.json())
      .then((data) => {
        setImages([{ ...data, title: word }, ...images]);
      })
      .catch((error) => {
        console.log(error);
      });
    setWord('');
  };

  const handleDeleteSubmit = (id) => {
    setImages(images.filter((image) => image.id !== id));
  };

  return (
    <div className="App">
      <Header title="Images Gallery" />
      <Search word={word} setWord={setWord} handleSubmit={handleSearchSubmit} />
      <Container className="mt-4">
        {images.length ? (
          <Row xs={1} md={2} lg={3}>
            {images.map((image, i) => (
              <Col key={i} className="pb-3">
                <ImageCard image={image} deleteImage={handleDeleteSubmit} />
              </Col>
            ))}
          </Row>
        ) : (
          <Welcome />
        )}
      </Container>
    </div>
  );
};

export default App;
