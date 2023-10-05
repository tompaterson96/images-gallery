import os
from unittest import mock
import pytest

import unsplash_client


class WithAsyncContextManager:
    async def __aenter__(self, *args, **kwargs):
        return self

    async def __aexit__(self, *args, **kwargs):
        pass


def test_environment_variable_set():
    assert os.environ.get("UNSPLASH_KEY", "") is not None


@pytest.mark.asyncio
async def test_get_new_image_uses_word_as_query_param():
    mock_client_session = mock.AsyncMock(WithAsyncContextManager())
    mock_session = mock.AsyncMock()
    mock_get = mock.AsyncMock()
    mock_response = mock.AsyncMock()

    mock_client_session.__aenter__.return_value = mock_session
    mock_client_session.__aenter__.return_value.get = mock_get
    mock_client_session.__aenter__.return_value.get.return_value = mock_response

    with mock.patch(
        "unsplash_client.aiohttp.ClientSession", return_value=mock_client_session
    ):
        word = "test"
        await unsplash_client.get_new_image(word)
        mock_get.assert_called_with(
            unsplash_client.UNSPLASH_URL,
            headers={
                "Accept-Version": "v1",
                "Authorization": f"Client-ID {unsplash_client.UNSPLASH_KEY}",
            },
            params={"query": word},
            timeout=10,
        )


@pytest.mark.asyncio
@mock.patch("aiohttp.ClientSession")
async def test_get_new_image_returns_response_json(_):
    mock_client_session = mock.AsyncMock(WithAsyncContextManager())
    mock_session = mock.AsyncMock()
    mock_get = mock.AsyncMock()
    mock_response = mock.AsyncMock()
    mock_json = mock.Mock()

    mock_client_session.__aenter__.return_value = mock_session
    mock_client_session.__aenter__.return_value.get = mock_get
    mock_client_session.__aenter__.return_value.get.return_value = mock_response
    mock_client_session.__aenter__.return_value.get.return_value.json.return_value = (
        mock_json
    )

    with mock.patch(
        "unsplash_client.aiohttp.ClientSession", return_value=mock_client_session
    ):
        word = "test"
        response = await unsplash_client.get_new_image(word)
        assert response == mock_json
