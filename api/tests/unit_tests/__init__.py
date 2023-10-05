import pytest
import main
import images_db
import mongomock


@pytest.fixture
def client():
    """Configures the app for testing

    Sets app config variable ``TESTING`` to ``True``

    :return: App for testing
    """

    # app.config['TESTING'] = True
    test_client = main.app.test_client()

    yield test_client
