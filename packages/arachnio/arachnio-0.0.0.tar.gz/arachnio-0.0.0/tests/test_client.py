from os import getenv
from unittest import TestCase

from arachnio import ArachnioClient

ARACHNIO_BASE_URL = getenv("ARACHNIO_BASE_URL")
ARACHNIO_API_KEY = getenv("ARACHNIO_API_KEY")


class ArachnioClientTests(TestCase):
    def test(self):
        self.assertIsNotNone(ARACHNIO_BASE_URL, "Missing required environment variable ARACHNIO_BASE_URL")
        self.assertIsNotNone(ARACHNIO_API_KEY, "Missing required environment variable ARACHNIO_API_KEY")

        client = ArachnioClient(ARACHNIO_BASE_URL, ARACHNIO_API_KEY)
        
        print(client.parse_domain("www.arachn.io"))
        print(client.parse_link("https://www.arachn.io/post/what-is-web-scraping"))
        print(client.unwind_link("https://bit.ly/3ZxLPEX"))
        print(client.extract_link("https://www.arachn.io/post/what-is-web-scraping"))

        # Our smoke tests are run against a low-level plan without batch endpoint access
        # print(client.parse_domain_batch(["www.arachn.io"]))
        # print(client.parse_link_batch(["https://www.arachn.io/post/what-is-web-scraping"]))
        # print(client.unwind_link_batch(["https://bit.ly/3ZxLPEX"]))
        
