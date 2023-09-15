import os
import unittest
from unittest import mock
import pytest

import unsplash_client


class TestUnsplashClient(unittest.TestCase):
    def test_environment_variable_set(self):
        assert os.environ.get("UNSPLASH_KEY", "") is not None

    @pytest.mark.asyncio
    @mock.patch("aiohttp.ClientSession")
    async def test_get_new_image_uses_word_as_query_param(self, client_session):
        word = "test"
        await unsplash_client.get_new_image(word)
        client_session.return_value.__enter__.get.assert_called_with(
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
    async def test_get_new_image_returns_response_json(self, client_session):
        word = "test"
        unsplash_response = mock.Mock()

        client_session.return_value.__enter__.get.return_value.__enter__.return_value = (
            unsplash_response
        )

        response = unsplash_client.get_new_image(word)

        assert response == unsplash_response.json()


if __name__ == "__main__":
    unittest.main()
