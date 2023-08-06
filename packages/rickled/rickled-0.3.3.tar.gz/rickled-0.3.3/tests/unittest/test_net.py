import unittest
import os
from rickled import Rickle
from rickled.net import serve_rickle_http, serve_rickle_https

class TestHttpHosting(unittest.TestCase):

    def test_host_http(self):
        definition = """
root:
    data:
        hello: world
        """

        rick = Rickle(definition)

        # serve_rickle_http(rick, port=8081)


    def test_host_https(self):
        definition = """
root:
    data:
        hello: world
        """

        rick = Rickle(definition)

        # serve_rickle_https(rick, path_to_private_key='./local.pem', path_to_certificate='./local.crt', port=8081)