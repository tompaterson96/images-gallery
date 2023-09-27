import { useEffect, useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Header from './components/Header';
import Search from './components/Search';
import ImageCard from './components/ImageCard';
import Welcome from './components/Welcome';
import useToken from './components/useToken';
import LoginModal from './components/LoginModal';
import { Container, Row, Col } from 'react-bootstrap';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const App = () => {
  const { setToken, token, removeToken } = useToken();

  const [word, setWord] = useState('');
  const [images, setImages] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [currentUser, setCurrentUser] = useState({});

  function getCurrentUser() {
    if (!token) {
      return null;
    }
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace('-', '+').replace('_', '/');
    const jwt = JSON.parse(window.atob(base64));
    return jwt['sub'];
  }

  useEffect(() => setCurrentUser(getCurrentUser()), [token]);

  const getSavedImages = async (access_token) => {
    if (access_token) {
      const config = {
        headers: { Authorization: `Bearer ${access_token}` },
      };

      try {
        const res = await axios.get(`${API_URL}/images`, config);
        res.access_token && setToken(res.access_token);

        const all_images = [...res.data, ...images];
        const all_ids = all_images.map((item) => item.id);
        const unique_ids = all_ids.filter(
          (id, index) => all_ids.indexOf(id) === index,
        );
        const unique_images = [];
        unique_ids.forEach((id) =>
          unique_images.push(all_images.find((image) => image.id === id)),
        );
        setImages(unique_images);

        toast.success('Downloaded stored images');
      } catch (error) {
        console.log(error);
        toast.error(`Error occurred during stored images download: ${error}`);
      }
    }
  };

  useEffect(() => {
    getSavedImages(token);
  }, []);

  const handleSearchSubmit = async (ev) => {
    ev.preventDefault();

    try {
      const res = await axios.get(`${API_URL}/new-image?query=${word}`);
      setImages([{ ...res.data, title: word }, ...images]);
      toast.info(`Image ${word.toUpperCase()} found`);
    } catch (error) {
      console.log(error);
      toast.error(`Error occurred during image search: ${error}`);
    }

    setWord('');
  };

  const handleDeleteSubmit = async (id) => {
    try {
      const imageToBeDeleted = images.find((image) => image.id === id);
      if (!imageToBeDeleted.saved) {
        setImages(images.filter((image) => image.id !== id));
        toast.warn(`Image ${imageToBeDeleted.title.toUpperCase()} deleted`);
      } else {
        const config = {
          headers: { Authorization: `Bearer ${token}` },
        };
        const res = await axios.delete(`${API_URL}/images/${id}`, config);
        if (res.data?.deleted_id) {
          setImages(images.filter((image) => image.id !== id));
          toast.warn(`Image ${imageToBeDeleted.title.toUpperCase()} deleted`);
        }
      }
    } catch (error) {
      console.log(error);
      toast.error(`Error occurred during deleting image: ${error}`);
    }
  };

  const handleSaveSubmit = async (id) => {
    try {
      const imageToBeSaved = images.find((image) => image.id === id);
      imageToBeSaved.saved = true;

      const config = {
        headers: { Authorization: `Bearer ${token}` },
      };
      const res = await axios.post(`${API_URL}/images`, imageToBeSaved, config);
      if (res.data?.inserted_id) {
        setImages(
          images.map((image) =>
            image.id === id ? { ...image, saved: true } : image,
          ),
        );
        toast.info(`Image ${imageToBeSaved.title} saved`);
      }
    } catch (error) {
      console.log(error);
      toast.error(`Error occurred during saving image: ${error}`);
    }
  };

  return (
    <div className="App">
      <Header
        title="Images Gallery"
        currentUser={currentUser}
        token={token}
        removeToken={removeToken}
        setShowModal={setShowModal}
        notifier={toast}
        images={images}
        setImages={setImages}
      />

      <LoginModal
        setToken={setToken}
        getSavedImages={getSavedImages}
        showModal={showModal}
        setShowModal={setShowModal}
        notifier={toast}
      />

      <Search word={word} setWord={setWord} handleSubmit={handleSearchSubmit} />

      <Container className="mt-4">
        {images.length ? (
          <Row xs={1} md={2} lg={3}>
            {images.map((image, i) => (
              <Col key={i} className="pb-3">
                <ImageCard
                  image={image}
                  deleteImage={handleDeleteSubmit}
                  saveImage={handleSaveSubmit}
                  token={token}
                />
              </Col>
            ))}
          </Row>
        ) : (
          <Welcome />
        )}
      </Container>
      <ToastContainer position="bottom-right" />
    </div>
  );
};

export default App;
