import os
import unittest
from unittest import mock

import unsplash_client


class TestUnsplashClient(unittest.TestCase):
    def test_environment_variable_set(self):
        assert os.environ.get("UNSPLASH_KEY", "") is not None

    @mock.patch("unsplash_client.requests")
    def test_get_new_image_uses_word_as_query_param(self, requests):
        word = "test"
        unsplash_client.get_new_image(word)
        requests.get.assert_called_with(
            unsplash_client.UNSPLASH_URL,
            headers={
                "Accept-Version": "v1",
                "Authorization": f"Client-ID {unsplash_client.UNSPLASH_KEY}",
            },
            params={"query": word},
            timeout=10,
        )

    @mock.patch("unsplash_client.requests")
    def test_get_new_image_returns_response_json(self, requests):
        word = "test"
        unsplash_response = mock.Mock()
        requests.get.return_value = unsplash_response
        response = unsplash_client.get_new_image(word)

        assert response == unsplash_response.json()
